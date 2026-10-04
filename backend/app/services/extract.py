import io
import os
import re

ALLOWED_EXTENSIONS = {".pdf", ".txt", ".md"}


class UnsupportedType(Exception):
    pass


class EmptyDocument(Exception):
    pass


class ExtractionError(Exception):
    pass


def normalize_text(text: str) -> str:
    text = text.replace("\x00", "")
    return re.sub(r"\s+", " ", text).strip()


def extract_text(filename: str, data: bytes) -> str:
    ext = os.path.splitext(filename or "")[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise UnsupportedType(f"Unsupported file type '{ext or 'none'}'. Upload a PDF, TXT or MD file.")

    if ext == ".pdf":
        try:
            from pypdf import PdfReader

            reader = PdfReader(io.BytesIO(data))
            raw = "\n".join((page.extract_text() or "") for page in reader.pages)
        except Exception as exc:
            raise ExtractionError("This PDF could not be read. It may be corrupt or password-protected.") from exc
    else:
        raw = data.decode("utf-8", errors="replace")

    text = normalize_text(raw)
    if not text:
        raise EmptyDocument("No text could be found in this file. Scanned PDFs are not supported.")
    return text
