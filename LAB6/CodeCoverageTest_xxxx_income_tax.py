import pytest
from income_tax import taxable_income, tax_due, refund_status

# --- Line Coverage Tests: taxable_income ---

def test_taxable_income_negative_gross():
    with pytest.raises(ValueError, match="invalid income"):
        taxable_income(-100, "new", 0)

def test_taxable_income_new_regime():
    assert taxable_income(1000000, "new", 0) == 925000

def test_taxable_income_old_regime_high_investments():
    # Deduction capped at 150000 + 50000 = 200000
    assert taxable_income(1000000, "old", 200000) == 800000

def test_taxable_income_unknown_regime():
    with pytest.raises(ValueError, match="unknown regime"):
        taxable_income(500000, "invalid_regime", 0)

def test_taxable_income_below_zero_result():
    # Deduction is 75000, gross is 50000 -> taxable becomes < 0
    assert taxable_income(50000, "new", 0) == 0


# --- Line Coverage Tests: tax_due ---

def test_tax_due_negative_taxable():
    with pytest.raises(ValueError, match="invalid amount"):
        tax_due(-5000, 30)

def test_tax_due_super_senior():
    assert tax_due(200000, 80) == 0

def test_tax_due_senior():
    assert tax_due(200000, 65) == 0

def test_tax_due_regular_below_exempt():
    assert tax_due(200000, 30) == 0

def test_tax_due_5_percent_slab():
    # Regular exemption = 250000, slab = 100000 <= 250000
    assert tax_due(350000, 30) == 5000

def test_tax_due_20_percent_slab():
    # Regular exemption = 250000, slab = 350000 > 250000
    assert tax_due(600000, 30) == 32500


# --- Line Coverage Tests: refund_status ---

def test_refund_status_refund_on_time():
    assert refund_status(10000, 5000, True) == "refund"

def test_refund_status_refund_delayed():
    assert refund_status(10000, 5000, False) == "refund delayed"

def test_refund_status_pay_balance_on_time():
    assert refund_status(5000, 10000, True) == "pay balance"

def test_refund_status_pay_balance_penalty():
    assert refund_status(5000, 10000, False) == "pay balance with penalty"

def test_refund_status_settled():
    assert refund_status(5000, 5000, True) == "settled"