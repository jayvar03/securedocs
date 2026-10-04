from app.services.retriever import build_tsquery, rrf


def test_tsquery_letters_and_digits_only():
    q = build_tsquery("What's the CEO's salary?! ' | & ! ( ) :* drop table")
    assert set(q) <= set("abcdefghijklmnopqrstuvwxyz0123456789 |")
    assert "ceo" in q and "salary" in q


def test_tsquery_dedupes_and_handles_empty():
    assert build_tsquery("Pay pay PAY") == "pay"
    assert build_tsquery("?!?") == ""


def test_rrf_prefers_items_in_both_lists():
    fused = rrf([[1, 2, 3], [3, 4, 1]])
    ids = [i for i, _ in fused]
    assert ids[0] == 1 and set(ids) == {1, 2, 3, 4}
    assert abs(dict(fused)[1] - (1 / 61 + 1 / 63)) < 1e-9


def test_rrf_empty():
    assert rrf([[], []]) == []
