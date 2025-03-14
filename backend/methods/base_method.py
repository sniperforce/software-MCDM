from abc import ABC, abstractmethod
import numpy as np
from models import DecisionMatrix, Result

class BaseMethod(ABC):
    "Base abstract class for all MCDM methods"

    def __init__(self, name):
        self.name = name
    
    def execute(self, decision_matrix):
        "Executes the MCDM method"

        #Validate input data
        self._validate_input(decision_matrix)

        #Normalize the decision matrix
        normalized_matrix = self._normalize(decision_matrix)

        #Execute specific algorithm
        scores, rankings = self._run_algorithm(normalized_matrix)

        #Create and return the result
        return Result(
            method_name=self.name,
            decision_matrix=decision_matrix,
            scores=scores,
            rankings=rankings,
            additional_data=self._get_additional_data()
        )
    
    def _validate_input(self, decision_matrix):
        """Validates the input data"""
        if not isinstance(decision_matrix, DecisionMatrix):
            raise ValueError("The input must be a DecisionMatrix instance")

        if decision_matrix.is_empty():
            raise ValueError("The decision matrix cannot be empty")
        
        if not decision_matrix.has_weights():
            raise ValueError("The decision matrix must have weights")
        
        #Specific Validation of the method
        self._validate_method_specific(decision_matrix)
    
    @abstractmethod
    def _validate_method_specific(self, decision_matrix):
        pass

    @abstractmethod
    def _normalize(self, decision_matrix):
        pass

    @abstractmethod
    def _run_algorithm(self, normalized_matrix):
        pass

    def _get_additional_data(self):
        return {}
        
        