# recommendation_system.py
# Sistema de recomendación de productos basado en K-Nearest Neighbors (KNN).
# Código inicial generado con apoyo de GitHub Copilot y luego revisado/ampliado.

# Importar las librerías necesarias
import os

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.neighbors import KNeighborsClassifier, NearestNeighbors
from sklearn.preprocessing import StandardScaler

FEATURES = ["feature1", "feature2", "feature3"]
DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "products.csv")


# Cargar los datos (dataset de productos incluido en el repositorio)
def load_data(path=DATA_PATH):
    data = pd.read_csv(path)
    return data


def main():
    data = load_data()
    print(f"Productos cargados: {len(data)}")
    print(data.head(), "\n")

    # Preprocesamiento de datos
    # Seleccionar las características y la etiqueta
    features = data[FEATURES]
    labels = data["label"]

    # Escalar las características para que todas pesen lo mismo en la distancia
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)

    # Dividir los datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(
        features_scaled, labels, test_size=0.2, random_state=42, stratify=labels
    )

    # Crear y entrenar el modelo de clasificación
    model = KNeighborsClassifier(n_neighbors=5)
    model.fit(X_train, y_train)

    # Realizar predicciones
    y_pred = model.predict(X_test)

    # Evaluar el modelo
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy * 100:.2f}%")
    print(classification_report(y_test, y_pred, zero_division=0))

    # Modelo de vecinos más cercanos para recomendar productos similares
    nn = NearestNeighbors(n_neighbors=4)
    nn.fit(features_scaled)

    # Función de recomendación
    def recommend(product_features, k=3):
        """Devuelve la categoría predicha y los k productos más parecidos."""
        x = scaler.transform(pd.DataFrame([product_features], columns=FEATURES))
        category = model.predict(x)[0]
        _, idx = nn.kneighbors(x, n_neighbors=k)
        similar = data.iloc[idx[0]][["product_id", "name", "label"]]
        return category, similar

    # Ejemplo de uso de la función de recomendación
    example_product = [4.2, 1.1, 7.5]
    category, similar = recommend(example_product)
    print(f"Producto de ejemplo: {example_product}")
    print(f"Recommended category: {category}")
    print("Productos recomendados:")
    print(similar.to_string(index=False))


if __name__ == "__main__":
    np.random.seed(42)
    main()
