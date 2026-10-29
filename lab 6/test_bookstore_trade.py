import pytest
from bookstore_trade_in import process_book_buybacks, inspect_scanner_calibration

# --- Tests for process_book_buybacks ---

def test_single_paperback_good():
    batches = [
        {
            "intake_approved": True,
            "format": "paperback",
            "payout_in_credit": False,
            "books": [{"missing_pages": 0, "condition": "good", "counterfeit": False}]
        }
    ]
    result = process_book_buybacks(batches, 5.0)
    assert result["total_payout"] == 8.0
    assert result["status"] == "COMPLETED"


def test_invalid_batches_type():
    with pytest.raises(ValueError, match="Invalid batches list or credit bonus"):
        process_book_buybacks("not_a_list", 5.0)


def test_invalid_credit_bonus():
    with pytest.raises(ValueError, match="Invalid batches list or credit bonus"):
        process_book_buybacks([], -1.0)


def test_intake_not_approved():
    batches = [
        {
            "intake_approved": False,
            "format": "paperback",
            "books": [{"missing_pages": 0, "condition": "good", "counterfeit": False}]
        }
    ]
    result = process_book_buybacks(batches, 5.0)
    assert result["total_payout"] == 0.0
    assert result["status"] == "ZERO_CREDIT"


def test_hardcover_and_textbook_conditions():
    batches = [
        {
            "intake_approved": True,
            "format": "textbook",
            "payout_in_credit": True,
            "books": [
                {"missing_pages": 0, "condition": "mint", "counterfeit": False},
                {"missing_pages": 0, "condition": "poor", "counterfeit": False},
            ]
        },
        {
            "intake_approved": True,
            "format": "hardcover",
            "payout_in_credit": False,
            "books": [
                {"missing_pages": 0, "condition": "good", "counterfeit": False}
            ]
        }
    ]
    result = process_book_buybacks(batches, 5.0)
    assert result["total_payout"] == 86.0
    assert result["status"] == "COMPLETED"


def test_invalid_format_type():
    batches = [
        {
            "intake_approved": True,
            "format": "audiobook",
            "books": []
        }
    ]
    result = process_book_buybacks(batches, 0.0)
    assert result["total_payout"] == 0.0
    assert result["status"] == "ZERO_CREDIT"


def test_missing_pages_and_counterfeit():
    batches = [
        {
            "intake_approved": True,
            "format": "hardcover",
            "payout_in_credit": False,
            "books": [
                {"missing_pages": 3, "condition": "good", "counterfeit": False},
                {"missing_pages": 0, "condition": "good", "counterfeit": True},
            ]
        },
        {
            "intake_approved": True,
            "format": "textbook",
            "payout_in_credit": False,
            "books": [
                {"missing_pages": 0, "condition": "mint", "counterfeit": False},
                {"missing_pages": 0, "condition": "good", "counterfeit": True},
            ]
        }
    ]
    result = process_book_buybacks(batches, 0.0)
    assert result["total_payout"] == 0.0
    assert result["status"] == "ZERO_CREDIT"


def test_audit_rejected_when_more_than_4_rejected():
    batches = [
        {
            "intake_approved": True,
            "format": "unknown",
            "books": []
        }
        for _ in range(5)
    ]
    result = process_book_buybacks(batches, 0.0)
    assert result["status"] == "AUDIT_REJECTED"


# --- Tests for inspect_scanner_calibration ---

def test_inspect_scanner_empty():
    assert inspect_scanner_calibration([]) == "NO_DATA"


def test_inspect_scanner_calibrated():
    matrix = [
        [1, 2, 6, 2, 1],
        [0, 5, 4, 3]
    ]
    assert inspect_scanner_calibration(matrix) == "CALIBRATED"


def test_inspect_scanner_recalibrate():
    matrix = [
        [1, 2, 3],
        [6, 7, 1]
    ]
    assert inspect_scanner_calibration(matrix) == "RECALIBRATE"
