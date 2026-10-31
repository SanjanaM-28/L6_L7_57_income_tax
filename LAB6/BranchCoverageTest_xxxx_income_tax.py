import pytest
from income_tax import taxable_income, tax_due, refund_status

# --- Branch Coverage Tests: taxable_income ---

def test_taxable_income_negative_gross_branch():
    with pytest.raises(ValueError, match="invalid income"):
        taxable_income(-1, "new", 0)

def test_taxable_income_new_regime_branch():
    assert taxable_income(500000, "new", 0) == 425000

def test_taxable_income_old_regime_investments_over_limit():
    # Branch: investments > 150000 (True)
    assert taxable_income(500000, "old", 160000) == 300000

def test_taxable_income_old_regime_investments_under_limit():
    # Branch: investments > 150000 (False)
    assert taxable_income(500000, "old", 100000) == 350000

def test_taxable_income_old_regime_investments_exact_limit():
    # Boundary: investments == 150000
    assert taxable_income(500000, "old", 150000) == 300000

def test_taxable_income_invalid_regime_branch():
    with pytest.raises(ValueError, match="unknown regime"):
        taxable_income(500000, "corporate", 0)

def test_taxable_income_negative_result_branch():
    # Branch: taxable < 0 (True)
    assert taxable_income(10000, "new", 0) == 0

def test_taxable_income_positive_result_branch():
    # Branch: taxable < 0 (False)
    assert taxable_income(100000, "new", 0) == 25000


# --- Branch Coverage Tests: tax_due ---

def test_tax_due_negative_taxable_branch():
    with pytest.raises(ValueError, match="invalid amount"):
        tax_due(-1, 25)

def test_tax_due_age_80_exact_super_senior():
    # Boundary: age >= 80 (True)
    assert tax_due(600000, 80) == 5000

def test_tax_due_age_79_senior():
    # Boundary: age >= 80 (False), age >= 60 (True)
    assert tax_due(600000, 79) == 22500

def test_tax_due_age_60_exact_senior():
    # Boundary: age >= 60 (True)
    assert tax_due(600000, 60) == 22500

def test_tax_due_age_59_regular():
    # Boundary: age >= 60 (False)
    assert tax_due(600000, 59) == 32500

def test_tax_due_exact_exemption():
    # Branch: taxable <= exempt (True)
    assert tax_due(250000, 30) == 0

def test_tax_due_above_exemption():
    # Branch: taxable <= exempt (False)
    # Slab = 250100 - 250000 = 100 -> Tax = 100 * 5 // 100 = 5
    assert tax_due(250100, 30) > 0

def test_tax_due_slab_250k_exact():
    # Boundary: slab <= 250000 (True) -> taxable = 500000 (slab = 250000)
    assert tax_due(500000, 30) == 12500

def test_tax_due_slab_over_250k():
    # Branch: slab <= 250000 (False)
    assert tax_due(500001, 30) == 12500


# --- Branch Coverage Tests: refund_status ---

def test_refund_status_positive_diff_on_time():
    assert refund_status(100, 50, True) == "refund"

def test_refund_status_positive_diff_late():
    assert refund_status(100, 50, False) == "refund delayed"

def test_refund_status_negative_diff_on_time():
    assert refund_status(50, 100, True) == "pay balance"

def test_refund_status_negative_diff_late():
    assert refund_status(50, 100, False) == "pay balance with penalty"

def test_refund_status_zero_diff():
    assert refund_status(100, 100, True) == "settled"