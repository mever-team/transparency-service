import PyPDF2

def pdf_to_chunks(pdf_path: str, char_per_chunk: int = 2000):
    chunks = []
    with open(pdf_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
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