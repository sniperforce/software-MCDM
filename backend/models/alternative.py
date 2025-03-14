class Alternative:
    """Represents an alternative in a MCDM problem"""

    def __init__(self, name, description=""):
        self.name = name
        self.description = description
    
    def __str__(self):
        return self.name