import numpy as np
from models.decision_matrix import DecisionMatrix
from models.criteria import Criteria
from models.alternative import Alternative
from methods.topsis import TOPSIS
from methods.ahp import AHP
from methods.promethee import PROMETHEE
from controllers.method_controller import MethodController

def main():
    # Create criteria
    criterios = [
        Criteria("Precio", Criteria.COST, "Costo de adquisición"),
        Criteria("Calidad", Criteria.BENEFIT, "Calidad del producto"),
        Criteria("Entrega", Criteria.COST, "Tiempo de entrega en días"),
        Criteria("Servicio", Criteria.BENEFIT, "Calidad del servicio postventa")
    ]
    
    # Crear alternativas
    alternativas = [
        Alternative("Proveedor A", "Proveedor con sede en Madrid"),
        Alternative("Proveedor B", "Proveedor con sede en Barcelona"),
        Alternative("Proveedor C", "Proveedor con sede en Valencia")
    ]
    
    # Datos de la matriz de decisión
    valores = np.array([
        [100, 8, 20, 6],  # Proveedor A
        [120, 9, 15, 8],  # Proveedor B
        [80, 7, 25, 5]    # Proveedor C
    ])
    
    # Pesos de los criterios
    pesos = np.array([0.4, 0.3, 0.2, 0.1])
    
    # Crear matriz de decisión
    matriz = DecisionMatrix(alternativas, criterios, valores, pesos)
    
    # Crear controlador de métodos
    controlador = MethodController()
    
    # Registrar métodos MCDM
    controlador.register_method(TOPSIS())
    controlador.register_method(PROMETHEE())
    # Para AHP se necesitarían matrices de comparación por pares
    
    # Ejecutar un método específico
    resultado_topsis = controlador.execute_method("TOPSIS", matriz)
    
    # Mostrar resultados
    print(f"Resultados de TOPSIS:")
    for alt, score, rank in resultado_topsis.get_ranked_alternatives():
        print(f"{alt.name}: Puntuación = {score:.4f}, Ranking = {rank}")
    
    # Comparar métodos
    comparacion = controlador.compare_methods(matriz)
    
    print("\nComparación de métodos:")
    for metodo in comparacion['methods']:
        mejor = comparacion['best_alternatives'][metodo]
        print(f"{metodo}: Mejor alternativa = {mejor}")

if __name__ == "__main__":
    main()