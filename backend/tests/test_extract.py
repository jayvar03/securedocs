import pytest

from app.services.extract import (
    EmptyDocument,
    ExtractionError,
    UnsupportedType,
    extract_text,
    normalize_text,
)


def test_txt_and_md():
    assert extract_text("a.txt", b"Hello   world\n\nagain") == "Hello world again"
    assert extract_text("a.md", b"# Title\n\nBody") == "# Title Body"


def test_nul_characters_removed():
    assert "\x00" not in normalize_text("ab\x00cd")
    assert extract_text("a.txt", b"ab\x00cd") == "abcd"


def test_unsupported_type():
    with pytest.raises(UnsupportedType):
        extract_text("a.exe", b"data")


def test_empty_file():
    with pytest.raises(EmptyDocument):
        extract_text("a.txt", b"   \n  ")


def test_corrupt_pdf():
    pytest.importorskip("pypdf")
    with pytest.raises(ExtractionError):
        extract_text("a.pdf", b"this is not a pdf")
