import pytest

pytest.importorskip("fastembed")

from app.services.embedder import embed  # noqa: E402


def test_shape_and_normalised():
    v = embed(["one", "two", "three"])
    assert v.shape == (3, 384)
    assert abs(float((v[0] ** 2).sum()) - 1.0) < 1e-3


def test_related_scores_higher_than_unrelated():
    q, related, unrelated = embed([
        "How many vacation days do employees get?",
        "Full-time staff receive 25 days of paid annual leave.",
        "The quarterly server maintenance window is on Sunday.",
    ])
    assert float(q @ related) > float(q @ unrelated)
