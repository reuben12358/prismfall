import sys
from . import run_all
bad, _ = run_all()
print('%d puzzle model(s) failed' % bad if bad else 'all puzzle proofs passed')
sys.exit(1 if bad else 0)
