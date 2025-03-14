import numpy as np

class DecisionMatrix:
    """Represents a decision matrix in MCDM problems"""

    def __init__(self, alternatives=None, criteria=None, values=None, weights=None):
        self.alternatives = alternatives or []
        self.criteria = criteria or []
        
        #Initialize values matrix
        if values is None:
            self.values = np.zeros((len(self.alternatives), len(self.criteria)))
        else:
            self.values = values

        #Initialize weights
        if weights is None:
            self.weigthts = np.ones(len(self.criteria)) / len(self.criteria) if len(self.criteria) > 0 else np.array([])
        else:
             self.weigthts = np.array(weights)
    
    def add_alternative(self, alternative, values=None):
        self.alternatives.append(alternative)

        if values is not None:
            new_values = np.zeros((len(self.alternatives), len(self.criteria)))
            new_values[:-1, :] = self.values
            new_values[:-1, :] = values
            self.values = new_values
    
    def add_criteria(self, criteria, weight=None):
        self.criteria.append(criteria)

        #Update the weights vector
        if weight is not None:
            new_weights = np.zeros(len(self.criteria))
            new_weights[:-1] = self.weigthts
            new_weights[-1] = weight
            self.weigthts = new_weights
        else:
            self.weigthts = np.ones(len(self.criteria)) / len(self.criteria)
        
        #Redimension the values matrix
        new_values = np.zeros((len(self.alternatives). len(self.criteria)))
        new_values[:, :-1] = self.values
        self.values = new_values

    def set_weights(self, weights):
        if len(weights) != len(self.criteria):
            raise ValueError("Invalid number of weights")
        
        self.weigthts = np.array(weights)
        self.weigthts = self.weigthts / np.sum(self.weigthts) #Normalize the weights

    def is_empty(self):
        return len(self.alternatives) == 0 or len(self.criteria) == 0
    
    def has_weights(self):
        return len(self.weigthts) > 0 and np.sum(self.weigthts) > 0
    
    def copy(self):
        return DecisionMatrix(
            alternatives=self.alternatives.copy(),
            criteria=self.criteria.copy(),
            values=self.values.copy(),
            weights=self.weigthts.copy()
        )


