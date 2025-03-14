from methods.base_method import BaseMethod

class MethodController:
    """Controller for the MCDM methods managments"""

    def __init__(self):
        self.available_methods = {}
        self.results = {}
    
    def register_method(self, method):
        if not isinstance(method, BaseMethod):
            raise ValueError("The method must be an instance of an existing method")

        self.available_methods[method.name] = method

    def get_available_methods(self):
        return list(self.available_methods.keys())

    def execute_method(self, method_name, decision_matrix):
        if method_name not in self.available_methods:
            raise ValueError(f"Method '{method_name}' not registered")
        
        method = self.available_methods[method_name]
        result = method.execute(decision_matrix)

        #Store the result
        self.results[method_name] = result

        return result

    def execute_all_methods(self, decision_matrix):
        results = {}

        for method_name in self.available_methods:
            results[method_name] = self.execute_method(method_name, decision_matrix)
        
        return results
    
    def compare_methods(self, decision_matrix, method_names=None):
        #If no method names are provided, compare all available methods
        if method_names is None:
            method_names = self.get_available_methods()
        
        #Validate methods
        for name in method_names:
            if name not in self.available_methods:
                raise ValueError(f"Method '{name}' not registered")
        
        #Ejecutar métodos
        results = {}
        for name in method_names:
            results[name] = self.execute_method(name, decision_matrix)

        #Analize consistency between methods
        comparison = {
            'methods': method_names,
            'rankings': {},
            'best_alternatives': {},
            'worst_alternatives': {}
        }

        #Collect rankings
        for name, result in results.items():
            comparison['rankings'][name] = result.rankings
            comparison['best_alternatives'][name] = result.get_best_alternative()[0].name
            comparison['worst_alternatives'][name] = result.get_ranked_alternatives()[-1][0].name

        return comparison