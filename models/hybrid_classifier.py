from sklearn.linear_model import LogisticRegression
import numpy as np

class HybridClassifier:
    def __init__(self):
        self.model = LogisticRegression(class_weight='balanced')
        self.is_trained = False
        
    def train(self, X, y):
        # X should be a list of [ast_similarity, semantic_similarity]
        if len(set(y)) > 1:
            self.model.fit(X, y)
            self.is_trained = True
        
    def predict(self, features):
        if not self.is_trained:
            # Fallback heuristic if not enough data to train
            ast_sim, sem_sim = features
            return 1 if (ast_sim + sem_sim) / 2.0 > 0.6 else 0
        return self.model.predict([features])[0]
