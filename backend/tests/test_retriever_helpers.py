from app.services.retriever import build_tsquery, filter_and_fuse, rrf


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


def test_filter_and_fuse_drops_low_similarity_keyword_and_vector_hits():
    # chunk 1: vector similarity 0.30 (passes 0.25)
    # chunk 2: vector similarity 0.20 (fails 0.25)
    vector_rows = [{"id": 1, "similarity": 0.30}, {"id": 2, "similarity": 0.20}]

    # chunk 3: keyword match with similarity 0.15 (passes 0.10)
    # chunk 4: keyword match with similarity 0.04 (fails 0.10)
    text_rows = [{"id": 3, "similarity": 0.15}, {"id": 4, "similarity": 0.04}]

    fused = filter_and_fuse(
        vector_rows,
        text_rows,
        min_similarity=0.25,
        min_keyword_similarity=0.10,
    )
    result_ids = [cid for cid, _score in fused]
    # Only chunk 1 and chunk 3 should pass their respective thresholds
    assert 1 in result_ids
    assert 3 in result_ids
    assert 2 not in result_ids
    assert 4 not in result_ids

