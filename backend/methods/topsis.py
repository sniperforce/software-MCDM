import numpy as np
from methods.base_method import BaseMethod
from models.decision_matrix import DecisionMatrix

class TOPSIS(BaseMethod):
    """TOPSIS method Implementation"""

    def __init__(self):
        super().__init__("TOPSIS")
    
    def _validate_method_specific(self, decision_matrix):
        #TOPSIS does not have specific validation
        pass

    def _normalize(self, decision_matrix):
        normalized_matrix = decision_matrix.copy()
        values = normalized_matrix.values

        #Vectorial Normalization   
        norms = np.sqrt(np.sum(values**2, axis=0))
        norms[norms == 0] = 1 #Avoid division by zero
        normalized_values = values / norms

        #Apply weights
        weighted_normalized_values = normalized_values * normalized_matrix.weights

        normalized_matrix.values = weighted_normalized_values
        return normalized_matrix
    
    def _run_algorithm(self, normalized_matrix):
        #Determining the ideals solutions
        values = normalized_matrix.values
        is_benefit = np.array([criteria.is_benefit() for criteria in normalized_matrix.criteria])

        #Positive ideal Solution (PIS) and negative (NIS)
        pis = np.zeros(len(normalized_matrix.criteria))
        nis = np.zeros(len(normalized_matrix.criteria))

        for j in range(len(normalized_matrix.criteria)):
            if is_benefit[j]:
                pis[j] = np.max(values[:, j])
                nis[j] = np.min(values[:, j])
            else:
                pis[j] = np.min(values[:, j])
                nis[j] = np.max(values[:, j])
        
        #Calculate the distance
        dist_pis = np.sqrt(np.sum((values - pis)**2, axis=1))
        dist_nis = np.sqrt(np.sum((values - nis)**2, axis=1))

        #Relative proximity index
        closeness = dist_nis / (dist_pis + dist_nis)

        #Ordering alternatives (more closeness best)
        rankings = len(closeness) - np.argsort(np.argsort(-closeness))

        #Adittional data for visualization
        self._additional_data = {
            'pis': pis,
            'nis': nis,
            'dist_pis': dist_pis,
            'dist_nis': dist_nis,
        }

        return closeness, rankings
    
    def _get_additional_data(self):
        return self._additional_data if hasattr(self, '_additional_data') else {}