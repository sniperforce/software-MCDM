import numpy as np
from methods.base_method import BaseMethod
from utils.exceptions import MethodExecutionError

class AHP(BaseMethod):
    """Analytic Hierarchy Process (AHP) method Implementation"""

    def __init__(self):
        super().__init__("AHP")
        #Random consistency Index (RI) values for n criteria
        self.RI = {1: 0, 2: 0, 3: 0.58, 4: 0.9, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}

    def _validate_method_specific(self, decision_matrix):
        #AHP need comparison matrix for pairs
        if 'pairwise_criteria' not in decision_matrix.additional_data:
            raise ValueError("Required pairwise comparison matrix for criteria")
        
        if 'pairwise_alternatives' not in decision_matrix.additional_data:
            raise ValueError("Required pairwise comparison matrix for alternatives")
        
    def _normalize(self, decision_matrix):
        return decision_matrix #No normalization required for AHP
    
    def _run_algorithm(self, decision_matrix):
        try:
            #Get the comparison matrices
            pairwise_criteria = decision_matrix.additional_data['pairwise_criteria']
            pairwise_alternatives = decision_matrix.additional_data['pairwise_alternatives']

            #Calculate the criteria weights
            criteria_weights = self._calculate_weights(pairwise_criteria)

            #Verify consistency of the criteria
            cr = self._consistency_ratio(pairwise_criteria, criteria_weights)
            if cr > 0.1:
                raise MethodExecutionError(f"The comparison matrix of criteria is inconsistent (CR={cr:.4f})")

            #Calculate the alternatives weights
            alt_weights = []
            for j, criterion_matrix in enumerate(pairwise_alternatives):
                weights = self.calculate_weights(criterion_matrix)

                #Verify consistency
                cr = self._consistency_ratio(criterion_matrix, weights)
                if cr > 0.1:
                    raise MethodExecutionError(f"The comparison matrix of criterion {j+1} is inconsistent (CR={cr:.4f})")        

                alt_weights.append(weights)
            
            alt_weights_matrix = np.array(alt_weights).T

            scores = np.dot(alt_weights_matrix, criteria_weights)

            rankings = len(scores) - np.argsort(np.argsort(-scores))

            self._additional_data = {
                'criteria_weights': criteria_weights,
                'alternatives_weights': alt_weights,
                'consistency_ratio': cr
            }

            return scores, rankings
        
        except Exception as e:
            raise MethodExecutionError(f"Error executing AHP method: {str(e)}")
    
    def _calculate_weights(self, pairwise_matrix):
        """Calculate the weights from a pairwise comparison matrix"""
        #Normalize columns
        col_sums = np.sum(pairwise_matrix, axis=0)
        normalized_matrix = pairwise_matrix / col_sums

        weights = np.mean(normalized_matrix, axis=1)

        return weights
    
    def _consistency_ratio(self, pairwise_matrix, weights):
        """Calculate the Consistency Ratio (CR) of a pairwise comparison matrix"""
        n = len(weights)
        
        if n <= 1:
            return 0 #Perfectly consistent
        
        weighted_sum = np.dot(pairwise_matrix, weights)

        #Calculate lambda max
        consistency_vector = weighted_sum / weights
        lambda_max = np.mean(consistency_vector)

        #Calculate CI (Consistency Index)
        ci = (lambda_max - n) / (n - 1)

        #Obtain Random Consistency Index (RI)
        ri = self.RI.get(n, 1.5) #Approximation for n > 10

        #Calculate Consistency Ratio (CR)
        cr = ci/ri if ri > 0 else 0

        return cr