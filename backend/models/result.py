import numpy as np

class Result:
    """Represents the result of a MCDM problem"""

    def __init__(self, method_name, decision_matrix, scores, rankings, additonal_data=None):
        self.method_name = method_name
        self.decision_matrix = decision_matrix
        self.scores = np.array(scores)
        self.rankings = np.array(rankings)
        self.additonal_data = additonal_data or {}

        #Validate dimensions
        if len(self.scores) != len(decision_matrix.alternatives):
            raise ValueError("The dimensions scores does not match the number of alternatives")
        
        if len(self.rankings) != len(decision_matrix.alternatives):
            raise ValueError("The dimensions rankings does not match the number of alternatives")
        
    
    def get_best_alternative(self):
        best_idx = np.argmin(self.rankings)
        return (
            self.decision_matrix.alternatives[best_idx],
            self.scores[best_idx],
            self.rankings[best_idx]
        )
    
    def get_ranked_alternatives(self):
        indexes = np.argsort(self.rankings)
        return [
            (self.decision_matrix.alternatives[idx], self.scores[idx], self.rankings[idx])
            for idx in indexes
        ]