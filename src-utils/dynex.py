import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier

class DYNEX:
    """
    Dynamic Ensemble Classifier with Confidence Optimization.
    Trains five base classifiers and adjusts their weights based on
    runtime performance confidence.
    """

    def __init__(self, alpha=0.2, adaptation_threshold=0.5):
        self.models = {
            "rf": RandomForestClassifier(n_estimators=100),
            "svm": SVC(probability=True),
            "xgb": XGBClassifier(eval_metric="logloss"),
            "gnb": GaussianNB(),
            "knn": KNeighborsClassifier(n_neighbors=5)
        }
        self.weights = {name: 1 / len(self.models) for name in self.models}
        self.alpha = alpha
        self.adaptation_threshold = adaptation_threshold
        self.trained = False

    def fit(self, X, y):
        """Train all base classifiers."""
        for name, model in self.models.items():
            model.fit(X, y)
        self.trained = True

    def predict(self, X):
        """
        Predict using the weighted ensemble.
        Adjusts weights dynamically based on confidence scores.
        """
        if not self.trained:
            raise RuntimeError("DYNEX models must be trained before prediction.")

        final_score = 0
        for name, model in self.models.items():
            proba = model.predict_proba(X)[:, 1]
            mean_confidence = np.mean(proba)
            # Weight adaptation
            self.weights[name] = (1 - self.alpha) * self.weights[name] + self.alpha * mean_confidence
            final_score += self.weights[name] * mean_confidence

        return int(final_score >= self.adaptation_threshold)
