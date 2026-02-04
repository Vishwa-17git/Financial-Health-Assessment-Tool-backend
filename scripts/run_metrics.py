import sys
import os
# Ensure 'backend' directory is on sys.path so imports like 'analysis' work
BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE not in sys.path:
    sys.path.insert(0, BASE)

import pandas as pd
from analysis.financial_metrics import calculate_metrics
from analysis.risk_analysis import generate_health_score

print('Reading CSV...')
df = pd.read_csv(os.path.join(BASE, 'uploads', 'sample_input.csv'))
print('CSV rows:', len(df))
metrics = calculate_metrics(df)
print('metrics:', metrics)
score = generate_health_score(metrics)
print('score:', score)
