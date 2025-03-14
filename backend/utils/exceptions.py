class MCDMError(Exception):
    """Base class for exceptions in the MCDM software"""
    pass

class MethodExecutionError(MCDMError):
    """"Error raised when a method execution fails"""
    pass

class DataValidationError(MCDMError):
    """Error raised in data validation"""
    pass

class WeightCalculationError(MCDMError):
    """"Error raised in the weight calculation"""
    pass