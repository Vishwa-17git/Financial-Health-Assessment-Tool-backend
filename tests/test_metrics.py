import os, sys
# ensure backend package root is importable when tests run from workspace root
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import pandas as pd
from analysis.financial_metrics import calculate_metrics


def test_calculate_metrics_types_and_values():
    df = pd.DataFrame({
        'Revenue': [1000, 2000, 3000],
        'Expenses': [400, 500, 600],
        'Loan_EMI': [100, 100, 100]
    })

    metrics = calculate_metrics(df)

    assert isinstance(metrics['revenue'], int)
    assert isinstance(metrics['expenses'], int)
    assert isinstance(metrics['profit_margin'], float)
    assert metrics['revenue'] == 6000
    assert metrics['expenses'] == 1500
    assert metrics['profit'] == 4500
    assert metrics['cash_flow'] == 4200
