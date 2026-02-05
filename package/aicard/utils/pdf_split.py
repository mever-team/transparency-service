from typing import Optional, Union
from io import BytesIO
import PyPDF2


def pdf_to_chunks(
    pdf_path: Optional[str] = None,
    pdf_bytes: Optional[bytes] = None,
    char_per_chunk: int = -1 # 2000
) -> list[str]:

    if pdf_path is None and pdf_bytes is None:
        raise ValueError("Either pdf_path or pdf_bytes must be provided")
    if pdf_path is not None and pdf_bytes is not None:
        raise ValueError("Provide only one of pdf_path or pdf_bytes")
    if pdf_path is not None:
        pdf_source = open(pdf_path, "rb")
    else:
        pdf_source = BytesIO(pdf_bytes)
        
    try:
        reader = PyPDF2.PdfReader(pdf_source)

        # return full text
        if char_per_chunk == -1:
            full_text = ""
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
            return [full_text.strip()]

        # return chunks
        chunks = []
        current_chunk = ""
        for page in reader.pages:
            text = page.extract_text()
            if not text:
                continue
            for line in text.splitlines():
                if len(current_chunk) + len(line) > char_per_chunk:
                    last_period = current_chunk.rfind(".")
                    if last_period != -1:
                        chunks.append(current_chunk[: last_period + 1])
                        current_chunk = (current_chunk[last_period + 1 :].strip() + line + "\n")
                    else:
                        chunks.append(current_chunk.strip())
                        current_chunk = line + "\n"
                else:
                    current_chunk += line + "\n"
        if current_chunk.strip():
            last_period = current_chunk.rfind(".")
            if last_period != -1:
                chunks.append(current_chunk[: last_period + 1])
                remainder = current_chunk[last_period + 1 :].strip()
                if remainder:
                    chunks.append(remainder)
            else:
                chunks.append(current_chunk.strip())
        return chunks
    finally:
        if pdf_path is not None:
            pdf_source.close()
