from aicard.card import ModelCard
from aicard.card.model_card import truncate
from aicard.service.assistants import Assistant, SemanticMatcher
from aicard.service.logger import Logger
from flask import abort
from threading import Lock, Thread
from werkzeug.exceptions import Forbidden, NotFound, Unauthorized
import traceback
import re
import time

class ModelCardEntry:
    def __init__(self, card: ModelCard, creator: str, conn):
        self.card = card
        self.creator = creator
        self.preview = card.to_html_card()
        self.lock = Lock()
        self._is_completing: bool = False
        self._completion_status: list[str] | None = None
        self._completion_start = 0
        self.__thread = None
        self.__chat_thread = None
        self.conn = conn
        self.card_id = None
        self.last_accessed = time.time()
        self.__questions = list()
        self.__num_answered = 0
        self.__extracted_sentences = dict()

    def history(self, k: int = 5):
        if self.card_id is None or k <= 0:
            return []

        cursor = self.conn.conn.cursor()
        visited = {self.card_id}
        frontier = {self.card_id}
        edges = set()
        for _ in range(k):
            if not frontier: break
            next_frontier = set()
            placeholders = ",".join("?" * len(frontier))
            cursor.execute(
                f"""
                SELECT parent_id, child_id, message
                FROM card_children
                WHERE parent_id IN ({placeholders}) OR child_id IN ({placeholders})
                """,
                tuple(frontier) * 2
            )
            for u, v, msg in cursor.fetchall():
                edges.add((u, v, msg or ""))
                if u not in visited:
                    visited.add(u)
                    next_frontier.add(u)
                if v not in visited:
                    visited.add(v)
                    next_frontier.add(v)
            frontier = next_frontier
        return list(edges)

    def touch(self):
        self.last_accessed = time.time()

    def commit_card(self, on_thread: bool = False, edit_message: str | None = "Edited"):
        self.__extracted_sentences = dict() # clear extracted sentences TODO: consider keeping those retained
        flattened = self.card.data.flatten()
        assert flattened, "Cannot commit an empty model card."
        assert self.card_id is not None, "Internal error: card_id has not been set for a cached card"

        def strip_html_tags(text: str) -> str:
            return re.sub(r'<[^>]*>', '', text)

        if self.card.overview.name:
            self.card.title = truncate(strip_html_tags(self.card.overview.name), 30)
        quality = self.card.quality()
        summary = self.card.summary()
        if summary:
            desc = summary  # create_progress_bar(quality)+" for "+summary
        else:
            desc = ""

        if edit_message:
            if edit_message == "Edited" and summary:
                edit_message = summary
            else:
                edit_message = edit_message + " " + summary
            # if desc: desc += f" [{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}]"

        timestamp = int(time.time())
        columns = list(flattened.keys())
        values = [flattened[key] for key in columns] + [desc, self.card.title, quality, timestamp]
        columns += ["desc", "title", "quality",
                    "timestamp"]  # do this after values uses columns, because its a db, not card field
        query = f'''
            UPDATE cards
            SET {", ".join(f'"{col}" = ?' for col in columns)}
            WHERE id = ?
        '''
        if on_thread:
            assert self.conn.db_path, "Database is stored on memory and cannot follow the independent thread connection model (this may be fine in testing)"
            import sqlite3
            # Open a short-lived connection just for this update
            # adjust db_path to wherever your database file lives.
            # It's fine to do this because on_thread=True is
            # reserved for agents where some ms of system operations
            # at worst are nothing in comparison.
            with sqlite3.connect(self.conn.db_path) as tmp_conn:
                if edit_message:
                    cursor = tmp_conn.execute(
                        "SELECT 1 FROM card_children WHERE parent_id = ? AND child_id = ?",
                        (self.card_id, self.card_id)
                    )
                    exists = cursor.fetchone() is not None
                    if exists:
                        tmp_conn.execute(
                            "UPDATE card_children SET message = ? WHERE parent_id = ? AND child_id = ?",
                            (edit_message, self.card_id, self.card_id)
                        )
                    else:
                        tmp_conn.execute(
                            "INSERT INTO card_children (parent_id, child_id, message) VALUES (?, ?, ?)",
                            (self.card_id, self.card_id, edit_message)
                        )
                    tmp_conn.commit()
                tmp_conn.execute(query, values + [self.card_id])
                tmp_conn.commit()
        else:
            if edit_message: self.conn.create_card_relation(parent_id=self.card_id, child_id=self.card_id,
                                                            message=edit_message)
            with self.conn.conn:
                cursor = self.conn.conn.cursor()
                cursor.execute(query, values + [self.card_id])

    def start_completion(self):
        self.lock.acquire()
        if self._is_completing:
            self.lock.release()
            abort(409, description="An AI assistant is already working on the model card")
        self._is_completing = True
        self._completion_status = ["An AI assistant is working on the model card"]
        self._completion_start = time.time()
        self.lock.release()

    def check_completion(self):
        ret = "An AI assistant is working on the model card"  # failsafe is to complain
        with self.lock:
            if not self._is_completing: ret = ""
            else: ret = "<br>".join(self._completion_status) + " (" + str(int(time.time() - self._completion_start)) + " sec)"
        return ret

    def end_completion(self):
        with self.lock:
            self._is_completing = False
            self._completion_status = None
            self._completion_start = time.time()

    def __enter__(self):
        self.lock.acquire()
        if self._is_completing:
            self.lock.release()
            abort(409, description="An AI assistant is working on the model card")
        return self.card

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.lock.release()

    def __autocomplete(self, data: dict, assistant: Assistant, logger: Logger):
        try:
            assistant.complete(self.card, data, logger, self._completion_status)
            self.commit_card(on_thread=True, edit_message=assistant.alias + " import")  # on_thread=True because we are on a heavyweight path either way
            logger.info(f"ended card {self.card_id} import", user=assistant.alias)
        except Exception as e:
            if not isinstance(e, Forbidden) and not isinstance(e, NotFound) and not isinstance(e, Unauthorized): traceback.print_exc()
            logger.error(f"aborted card{self.card_id} import with error {e}", user=assistant.alias)
        self.end_completion()

    def __autorefine(self, assistant: Assistant, logger: Logger):
        try:
            assistant.refine(self.card, logger, self._completion_status)
            self.commit_card(on_thread=True, edit_message=assistant.alias + " refinement")  # on_thread=True because we are on a heavyweight path either way
            logger.info(f"ended card {self.card_id} refinement", user=assistant.alias)
        except Exception as e:
            if not isinstance(e, Forbidden) and not isinstance(e, NotFound) and not isinstance(e,
                                                                                               Unauthorized): traceback.print_exc()
            logger.error(f"aborted card{self.card_id} refinement with error {e}", user=assistant.alias)
        self.end_completion()

    def autocomplete(self, data: dict, assistant: Assistant, logger: Logger):
        self.start_completion()
        self.__thread = Thread(target=self.__autocomplete, args=(data, assistant, logger))
        self.__thread.start()
        return "Autocompletion request was submitted successfully. Please wait while the assistant runs."

    def autorefine(self, assistant: Assistant, logger: Logger):
        self.start_completion()
        self.__thread = Thread(target=self.__autorefine, args=(assistant, logger))
        self.__thread.start()
        return "Refinement request was submitted successfully. Please wait while the assistant runs."

    def get_status(self):
        if self.check_completion(): return {"status": "locked", "message": "AI assistant is working on the model card"}
        return {"status": "editable", "message": "You can edit the model card"}

    def __answer_chats(self):
        # answers all pending chats while allowing new ones, but locking modifications to the card
        self.start_completion()
        while True:
            with self.lock:
                num_questions = len(self.__questions)
            if self.__num_answered>=num_questions:
                break
            question, feature_extractor, _, _ = self.__questions[self.__num_answered]
            try:
                need_to_recompute_embeddings = False
                with self.lock:
                    sentences = self.__extracted_sentences.get(feature_extractor, None)
                    if sentences is None:
                        sentences = dict()
                        need_to_recompute_embeddings = True
                if need_to_recompute_embeddings:
                    self.__extracted_sentences[feature_extractor] = sentences
                    for category, values in self.card.data.items():
                        if not isinstance(values, dict): continue
                        for field, value in values.items():
                            text_val = value.get().strip()
                            if not text_val or text_val=="unknown":
                                enriched = "passage:" + category + "/" + field + ":\n\n"+value.description+"\n\nunknown"
                                sentence = "Would have looked for an answer at " + field.lower() + " in " + category.lower() + ", but that is empty."
                                sentences[sentence] = feature_extractor.get_embeddings(enriched)
                                continue
                            if not " " in text_val:
                                enriched = "passage: " + category + "/" + field + ":\n\n"+value.description+"\n\n" + text_val
                                sentence = (field + " in " + category).capitalize() + " is: " + text_val
                                sentences[sentence] = feature_extractor.get_embeddings(enriched)
                                continue
                            text_val = text_val.replace("<br>",". ").replace("<div>", ". ").replace("<p>", ". ").replace("\n", ". ")
                            text_val = re.sub(r"<[^>]+>", " ", value.get()).strip() # html to fullstops
                            for sentence in text_val.split(". "):
                                sentence = sentence.strip()
                                #if not sentence: continue # redundant for next line
                                if not " " in sentence: continue
                                enriched = "passage: " + category + "/" + field + ":\n\n"+value.description+"\n\n" + sentence
                                sentence = "From " + field.lower() + " in " + category.lower() + ": \"" + sentence + "\""
                                sentences[sentence] = feature_extractor.get_embeddings(enriched)
                question_embeddings = feature_extractor.get_embeddings("question: "+question)
                reply = "I was unable to find relevant information."
                best_score = 0
                for sentence, embedding in sentences.items():
                    score = feature_extractor.embedding_similarity(question_embeddings, embedding)
                    if score <= best_score: continue
                    best_score = score
                    reply = sentence
            except Exception as e:
                reply = str(e)
            except:
                reply = "Something went wrong. Please try again."
            self.__questions[self.__num_answered] = question, feature_extractor, True, reply
            self.__num_answered += 1
        with self.lock:
            self.__chat_thread = None
        self.end_completion()

    def chat_ask(self, question: str, feature_extractor: SemanticMatcher|None):
        assert feature_extractor, "Chat capabilities are not available"
        self.__questions.append((question, feature_extractor, False, "..."))
        self.touch()
        if not self.__chat_thread:
            self.__chat_thread = Thread(target=self.__answer_chats)
            self.__chat_thread.start()
        return len(self.__questions)-1

    def chat_reply(self, question_id: int):
        assert 0<=question_id<len(self.__questions), "Invalid question index"
        self.touch()
        question, feature_extractor, status, reply = self.__questions[question_id]
        return status, reply