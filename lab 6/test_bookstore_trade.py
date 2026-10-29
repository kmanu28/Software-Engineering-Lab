import pytest
from bookstore_trade_in import process_book_buybacks, inspect_scanner_calibration

# ==============================================================================
# COMPREHENSIVE BRANCH COVERAGE TEST SUITE
# Covers all decision branches (True / False outcomes, short-circuit paths,
# loop conditions, and condition ladders).
# ==============================================================================

# --- Tests for process_book_buybacks ---

def test_buybacks_invalid_batches_type():
    # Branch: not isinstance(batches, list) is True
    with pytest.raises(ValueError, match="Invalid batches list or credit bonus"):
        process_book_buybacks("not_a_list", 5.0)


def test_buybacks_invalid_credit_bonus():
    # Branch: not isinstance(batches, list) is False, but store_credit_bonus < 0 is True
    with pytest.raises(ValueError, match="Invalid batches list or credit bonus"):
        process_book_buybacks([], -1.0)


def test_buybacks_intake_not_approved():
    # Branch: not batch.get("intake_approved", False) is True -> continue
    batches = [
        {"intake_approved": False, "format": "paperback", "books": []}
    ]
    result = process_book_buybacks(batches, 5.0)
    assert result["total_payout"] == 0.0
    assert result["status"] == "ZERO_CREDIT"


def test_buybacks_format_ladder_and_conditions():
    # Covers: format == "textbook", "hardcover", "paperback"
    # Covers: condition == "mint", "poor", "good" (else)
    # Covers: payout_in_credit == True and False
    batches = [
        {
            "intake_approved": True,
            "format": "textbook",
            "payout_in_credit": True,  # True branch for line 49
            "books": [
                {"missing_pages": 0, "condition": "mint", "counterfeit": False},
                {"missing_pages": 0, "condition": "poor", "counterfeit": False},
            ]
        },
        {
            "intake_approved": True,
            "format": "hardcover",
            "payout_in_credit": False,  # False branch for line 49
            "books": [
                {"missing_pages": 0, "condition": "good", "counterfeit": False}
            ]
        },
        {
            "intake_approved": True,
            "format": "paperback",
            "payout_in_credit": False,
            "books": [
                {"missing_pages": 0, "condition": "other_condition", "counterfeit": False}
            ]
        }
    ]
    # Textbook base = 40.0: mint = 50.0, poor = 16.0, payout_in_credit (+5) -> batch = 71.0
    # Hardcover base = 15.0: good = 15.0 -> batch = 15.0
    # Paperback base = 8.0: other = 8.0 -> batch = 8.0
    # Total = 94.0
    result = process_book_buybacks(batches, 5.0)
    assert result["total_payout"] == 94.0
    assert result["status"] == "COMPLETED"


def test_buybacks_unrecognized_format():
    # Branch: format not in ("textbook", "hardcover", "paperback") -> else rejected_items += 1, continue
    batches = [
        {"intake_approved": True, "format": "digital", "books": []}
    ]
    result = process_book_buybacks(batches, 0.0)
    assert result["total_payout"] == 0.0
    assert result["status"] == "ZERO_CREDIT"


def test_buybacks_missing_pages_and_counterfeit():
    # Covers:
    # - pages_missing > 0 (True branch)
    # - is_counterfeit True with format_type == "textbook" (breaks & zeros batch_credit)
    # - is_counterfeit True with format_type != "textbook" (adds 0.0, continues)
    batches = [
        {
            "intake_approved": True,
            "format": "hardcover",
            "payout_in_credit": False,
            "books": [
                {"missing_pages": 2, "condition": "good", "counterfeit": False},
                {"missing_pages": 0, "condition": "good", "counterfeit": True},
            ]
        },
        {
            "intake_approved": True,
            "format": "textbook",
            "payout_in_credit": False,
            "books": [
                {"missing_pages": 0, "condition": "mint", "counterfeit": False},
                {"missing_pages": 0, "condition": "good", "counterfeit": True},  # breaks
            ]
        }
    ]
    result = process_book_buybacks(batches, 0.0)
    assert result["total_payout"] == 0.0
    assert result["status"] == "ZERO_CREDIT"


def test_buybacks_audit_rejected():
    # Branch: rejected_items > 4 (True branch)
    batches = [
        {"intake_approved": True, "format": "magazine", "books": []}
        for _ in range(5)
    ]
    result = process_book_buybacks(batches, 0.0)
    assert result["status"] == "AUDIT_REJECTED"


def test_buybacks_empty_batch_zero_credit():
    # Branch: rejected_items <= 4 and total_payout == 0.0
    result = process_book_buybacks([], 0.0)
    assert result["total_payout"] == 0.0
    assert result["status"] == "ZERO_CREDIT"


# --- Tests for inspect_scanner_calibration ---

def test_scanner_no_data():
    # Branch: not scanner_matrix is True
    assert inspect_scanner_calibration([]) == "NO_DATA"


def test_scanner_recalibrate_streak():
    # Covers:
    # - error_rate > 5 (True)
    # - misread_streak >= 2 (True) -> return "RECALIBRATE"
    matrix = [
        [1, 2],
        [7, 8, 2]
    ]
    assert inspect_scanner_calibration(matrix) == "RECALIBRATE"


def test_scanner_calibrated_with_reset_streak():
    # Covers:
    # - error_rate > 5 (True, but misread_streak < 2, does not trigger RECALIBRATE)
    # - error_rate <= 5 (False -> resets streak to 0)
    # - loops finish -> return "CALIBRATED"
    matrix = [
        [6, 2, 7, 1]
    ]
    assert inspect_scanner_calibration(matrix) == "CALIBRATED"
