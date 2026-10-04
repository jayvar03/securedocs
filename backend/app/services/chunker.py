"""Sentence-aware text chunking with rolling overlap."""
import re

CHUNK_SIZE = 800
OVERLAP = 150
_SENTENCE_END = re.compile(r"(?<=[.!?])\s+")


def split_sentences(text: str) -> list[str]:
    clean_text = text.strip()
    return [s for s in _SENTENCE_END.split(clean_text) if s] if clean_text else []


def hard_split(sentence: str, size: int, overlap: int) -> list[str]:
    """Split an abnormally large sentence into overlapping windows."""
    step = max(1, size - overlap)
    pieces: list[str] = []
    i = 0
    while True:
        pieces.append(sentence[i : i + size])
        if i + size >= len(sentence):
            break
        i += step
    return pieces


def chunk_text(text: str, size: int = CHUNK_SIZE, overlap: int = OVERLAP) -> list[str]:
    """Pack whole sentences into chunks of at most `size` characters with `overlap`."""
    if not text.strip():
        return []

    units: list[str] = []
    for sentence in split_sentences(text):
        if len(sentence) <= size:
            units.append(sentence)
        else:
            units.extend(hard_split(sentence, size, overlap))

    chunks: list[str] = []
    current_sentences: list[str] = []
    current_length = 0

    for unit in units:
        added_length = len(unit) + (1 if current_sentences else 0)

        if current_sentences and (current_length + added_length > size):
            chunks.append(" ".join(current_sentences))

            # Carry over trailing sentences up to overlap limit
            tail_sentences: list[str] = []
            tail_length = 0
            for prev_sentence in reversed(current_sentences):
                sentence_cost = len(prev_sentence) + (1 if tail_sentences else 0)
                if tail_length + sentence_cost > overlap:
                    break
                tail_sentences.insert(0, prev_sentence)
                tail_length += sentence_cost

            current_sentences, current_length = tail_sentences, tail_length
            added_length = len(unit) + (1 if current_sentences else 0)
            if current_sentences and (current_length + added_length > size):
                current_sentences, current_length, added_length = [], 0, len(unit)

        current_sentences.append(unit)
        current_length += added_length

    if current_sentences:
        chunks.append(" ".join(current_sentences))

    return chunks


