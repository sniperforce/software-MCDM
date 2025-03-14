class Criteria:
    """Represents a criteria in a MCDM problem"""

    BENEFIT = "benefit"
    COST = "cost"

    def _init__(self, name, criteria_type=BENEFIT, description=''):
        self.name = name
        self.criteria_type = criteria_type
        self.description = description

        if criteria_type not in [self.BENEFIT, self.COST]:
            raise ValueError("criteria_type not valid must be either 'benefit' or 'cost'")
    
    def is_benefit(self):
        return self.criteria_type == self.BENEFIT
    
    def is_cost(self):
        return self.criteria_type == self.COST
    
    def __str__(self):
        return f"{self.name} ({self.criteria_type})"
        