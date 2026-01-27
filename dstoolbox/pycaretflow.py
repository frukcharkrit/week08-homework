# load sample dataset
from pycaret.datasets import get_data
data = get_data('diabetes')

from pycaret.classification import ClassificationExperiment
s = ClassificationExperiment()
s.setup(data, target = 'Class variable', session_id = 123)
best = s.compare_models()
print(best)

s.evaluate_model(best)

# OOP API
s.plot_model(best, plot = 'auc')

# OOP API
s.plot_model(best, plot = 'confusion_matrix')