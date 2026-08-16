"""Boundary-level scoring for sentence boundary detection.

Evaluates segmentation quality using word-level binary boundary arrays.
A boundary array marks the index of each word that ends a sentence with ``1``
and all other words with ``0``. Traditional Precision, Recall, and F1 are then
derived from True Positive / False Positive / False Negative counts.
"""


def _to_binary(sentences: list[str]) -> list[int]:
    """Convert segmented sentences into a word-level binary boundary array.

    Each sentence is split on whitespace; every word except the last in a
    sentence is marked ``0`` and the final word of each sentence is marked ``1``.
    Empty sentences are skipped to keep the array aligned with real tokens.
    """
    binary: list[int] = []
    for sent in sentences:
        sent_len = len(sent.split())
        if sent_len == 0:
            continue
        binary.extend([0] * (sent_len - 1))
        binary.append(1)
    return binary


def _align_arrays(
    gold_binary: list[int], pred_binary: list[int]
) -> tuple[list[int], list[int]]:
    """Align binary arrays of different lengths for positional comparison.

    When the model drops or adds words, the two arrays can differ in length.
    The shorter array is right-justified with ``0`` padding so both arrays share
    their final word's boundary marker (``1``) at the same index. This keeps the
    sentence-final boundary aligned without mutating the caller's arrays.
    """
    if len(gold_binary) == len(pred_binary):
        return gold_binary, pred_binary

    diff = len(gold_binary) - len(pred_binary)
    if diff > 0:
        pred_binary = [0] * diff + pred_binary
    else:
        gold_binary = [0] * (-diff) + gold_binary
    return gold_binary, pred_binary


def evaluate_segmentation(pred: list[str], gold: list[str]) -> dict[str, float]:
    """SBD evaluation using word-level binary boundary arrays.

    Converts both the predicted and gold segmentations into binary boundary
    markers, aligns them when lengths differ, and computes Precision, Recall,
    and F1 over the class of sentence-ending word positions.

    Args:
        pred: Predicted sentence boundaries as a list of sentence strings.
        gold: Ground-truth sentence boundaries as a list of sentence strings.

    Returns:
        A dict with ``"precision"``, ``"recall"``, ``"f1"``, ``"tp"``, ``"fp"``,
        and ``"fn"``. Precision/Recall/F1 fall back to ``0.0`` when their
        denominator is zero and the arrays contain no useful boundary signal.
    """
    gold_binary = _to_binary(gold)
    pred_binary = _to_binary(pred)

    gold_binary, pred_binary = _align_arrays(gold_binary, pred_binary)

    tp = fp = fn = 0
    for g, p in zip(gold_binary, pred_binary, strict=True):
        if g == 1 and p == 1:
            tp += 1
        elif g == 0 and p == 1:
            fp += 1
        elif g == 1 and p == 0:
            fn += 1

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1_score = (
        2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    )

    return {
        "precision": precision,
        "recall": recall,
        "f1": f1_score,
        "tp": tp,
        "fp": fp,
        "fn": fn,
    }
