from app.services.chunker import chunk_text, hard_split, split_sentences


def _text(n=40):
    return " ".join(f"This is sentence number {i} about the topic." for i in range(n))


def test_chunks_respect_size_limit():
    assert all(len(c) <= 800 for c in chunk_text(_text(200)))


def test_chunks_end_on_sentence_boundaries():
    for c in chunk_text(_text(100)):
        assert c.endswith(".")


def test_overlap_between_neighbours():
    chunks = chunk_text(_text(100))
    assert len(chunks) > 1
    last_sentence = split_sentences(chunks[0])[-1]
    assert last_sentence in chunks[1]


def test_no_content_lost():
    text = _text(120)
    joined = " ".join(chunk_text(text))
    for sentence in split_sentences(text):
        assert sentence in joined


def test_huge_sentence_is_hard_split():
    huge = "x" * 3000 + "."
    chunks = chunk_text(huge)
    assert len(chunks) > 1
    assert all(len(c) <= 800 for c in chunks)
    assert "".join(hard_split(huge, 800, 150))[:800] == huge[:800]


def test_short_text_single_chunk():
    assert chunk_text("Hello there. General Kenobi.") == ["Hello there. General Kenobi."]


def test_empty_text():
    assert chunk_text("   ") == []
