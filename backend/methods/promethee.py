import numpy as np
from methods.base_method import BaseMethod

class PROMETHEE(BaseMethod):
    """PROMETHEE method Implementation"""

    #Function types preference
    USUAL = 'usual'                 # Strict preference
    U_SHAPE = 'u_shape'             # U form
    V_SHAPE = 'v_shape'             # V form
    LEVEL = 'level'                 # Level form
    LINEAR = 'linear'               # Linear with indifference area
    GAUSSIAN = 'gaussian'           # Gaussian

    def __init__(self):
        super().__init__("PROMETHEE")
    
    def _validate_method_specific(self, decision_matrix):
        # PROMETHEE need preference and parameters functions
        if not hasattr(decision_matrix, 'preference_functions'):
            # By default, use usual function for all criteria
            decision_matrix.preference_functions = [self.USUAL] * len(decision_matrix.criteria)
            decision_matrix.preference_params = [(0, 0)] * len(decision_matrix.criteria)

    def _normalize(self, decision_matrix):
        # PROMETHEE does not require normalization
        return decision_matrix
    
    def _run_algorithm(self, decision_matrix):
        n_alternatives = len(decision_matrix.alternatives)
        n_criteria = len(decision_matrix.criteria)

        #Flow and preference matrix
        preference_matrix = np.zeros((n_alternatives, n_alternatives))

        #Calculate diference and preference
        for i in range(n_alternatives):
            for j in range(n_alternatives):
                if i != j:
                    preference = 0

                    for k in range(n_criteria):
                        #Difference between alternatives for criterion k
                        if decision_matrix.criteria[k].is_benefit():
                            d = decision_matrix.values[i, k] - decision_matrix.values[j, k]
                        else:
                            d = decision_matrix.values[j, k] - decision_matrix.values[i, k]
                        
                        # Apply preference function
                        pref_func = getattr(decision_matrix, 'preference_functions', [self.USUAL] * n_criteria)[k]
                        pref_params = getattr(decision_matrix, 'preference_params', [(0, 0)] * n_criteria)[k]

                        p = self._apply_preference_function(pref_func, d, pref_params)

                        #Weighted preference
                        preference += decision_matrix.weights[k] * p

                    preference_matrix[i, j] = preference

        # Calculate in and out flows
        outflow = np.sum(preference_matrix, axis=1) / (n_alternatives - 1)
        inflow = np.sum(preference_matrix, axis=0) / (n_alternatives - 1)

        # Net flow (bigger is better)      
        net_flow = outflow - inflow

        rankings = len(net_flow) - np.argsort(np.argsort(-net_flow))

        self._additional_data = {
            'preference_matrix': preference_matrix,
            'outflow': outflow,
            'inflow': inflow
        }   

        return net_flow, rankings
    
    def _apply_preference_function(self, d, preference_function, parameters):
        q, p = parameters # Indifference and preference thresholds

        if d <= 0:
            return 0 
        
        if preference_function == self.USUAL:
            return 1 if d > 0 else 0
        
        elif preference_function == self.U_SHAPE:
            return 1 if d > q else 0
        
        elif preference_function == self.V_SHAPE:
            return min(d / p, 1) if p > 0 else (1 if d > 0 else 0)
        
        elif preference_function == self.LEVEL:
            if d <= q:
                return 0
            elif d <= p:
                return 0.5
            else:
                return 1
        
        elif preference_function == self.LINEAR:
            if d <= q:
                return 0
            elif d <= p:
                return (d - q) / (p - q)
            else:
                return 1  

        elif preference_function == self.GAUSSIAN:
            sigma = p / np.sqrt(2)
            if d <= 0:
                return 0
            else:
                return 1 - np.exp(-(d**2) / (2 * sigma**2))

        return 0 # Default value  

