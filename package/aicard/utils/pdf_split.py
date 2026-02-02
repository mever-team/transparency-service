import PyPDF2

def pdf_to_chunks(pdf_path: str, char_per_chunk: int = 2000):
    with open(pdf_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        # If char_per_chunk is -1, return the full text
        if char_per_chunk == -1:
            full_text = ""
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
            return full_text.strip()

        chunks = []
        # Otherwise, split into chunks
        current_chunk = ""
        for page in reader.pages:
            text = page.extract_text()
            for line in text.splitlines():
                if len(current_chunk) + len(line) > char_per_chunk:
                    # Ensure the chunk ends with a complete sentence
                    last_period = current_chunk.rfind(".")
                    if last_period != -1:
                        chunks.append(current_chunk[:last_period + 1])
                        current_chunk = current_chunk[last_period + 1:].strip() + line + "\n"
                    else:
                        chunks.append(current_chunk)
                        current_chunk = line + "\n"
                else:
                    current_chunk += line + "\n"
        if current_chunk.strip():
            last_period = current_chunk.rfind(".")
            if last_period != -1:
                chunks.append(current_chunk[:last_period + 1])
                remainder = current_chunk[last_period + 1:].strip()
                if remainder:
                    chunks.append(remainder)
            else:
                chunks.append(current_chunk.strip())
    return chunks