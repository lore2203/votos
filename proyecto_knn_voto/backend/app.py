import joblib
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS

# --- 1. Inicializar la Aplicación Flask ---
app = Flask(__name__)
# Habilitar CORS para permitir que el frontend (en otro puerto) hable con esta API
CORS(app)

# --- 2. Cargar los Modelos Entrenados ---
# (Asegúrate de que estos archivos estén en la misma carpeta 'backend')
try:
    knn = joblib.load('knn_model.joblib')
    preprocessor = joblib.load('preprocessor.joblib')
    le = joblib.load('label_encoder.joblib')
    print("Modelos cargados exitosamente.")
except FileNotFoundError:
    print("Error: No se encontraron los archivos .joblib. Asegúrate de que estén en la carpeta 'backend'.")
    exit()

# --- 3. Definir las Columnas y Valores por Defecto ---
# El preprocesador espera 30 columnas. 
# El frontend solo enviará las 9 más importantes.
# Rellenamos las 21 restantes con sus valores "medianos" (vistos en el Colab).

# Lista de las 9 features que pediremos en el frontend
FEATURES_FROM_FRONTEND = [
    'age', 'gender', 'education', 'employment_status', 'income_bracket',
    'party_id_strength', 'tv_news_hours', 'social_media_hours', 'trust_media'
]

# Valores por defecto para las 21 features que NO pedimos
DEFAULT_FEATURES = {
    'employment_sector': 3.0,
    'marital_status': 2.0,
    'household_size': 4.0,
    'has_children': 1.0,
    'urbanicity': 1.0,
    'region': 2.0,
    'voted_last': 1.0,
    'union_member': 0.0,
    'public_sector': 0.0,
    'home_owner': 0.0,
    'small_biz_owner': 0.0,
    'owns_car': 0.0,
    'wa_groups': 2.0,
    'refused_count': 2.5,
    'attention_check': 1.0,
    'will_turnout': 1.0,
    'undecided': 1.0,
    'preference_strength': 5.0,
    'survey_confidence': 5.0,
    'civic_participation': 5.0,
    'job_tenure_years': 20.0 
    # (job_tenure_years SÍ estaba en numerical_features, pero lo simplificamos aquí)
    # (Ajuste: 'age' y 'job_tenure_years' eran numéricas. Dejemos 'job_tenure_years' aquí)
}

# --- 4. Crear el Endpoint de Predicción ---
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Obtener los 9 datos del JSON enviado por el frontend
        data = request.get_json()
        
        # Crear el diccionario completo con 30 features
        full_data_dict = {}
        
        # 1. Añadir los valores por defecto
        full_data_dict.update(DEFAULT_FEATURES)
        
        # 2. Añadir/Sobrescribir los 9 valores del usuario
        # Convertimos a float por seguridad
        for key in FEATURES_FROM_FRONTEND:
            full_data_dict[key] = float(data[key])
            
        # Corregir 'job_tenure_years' si 'age' es menor
        # (Lógica simple para evitar inconsistencias)
        if full_data_dict['age'] < 30:
            full_data_dict['job_tenure_years'] = 5.0
        
        # Convertir el diccionario en un DataFrame de 1 fila
        # (El preprocesador espera un DataFrame)
        df_input = pd.DataFrame(full_data_dict, index=[0])
        
        # --- 5. Realizar la Predicción ---
        
        # 1. Aplicar el preprocesador (imputar, escalar, one-hot encode)
        X_processed = preprocessor.transform(df_input)
        
        # 2. Obtener probabilidades para todas las clases
        pred_probabilities = knn.predict_proba(X_processed)
        
        # 3. Encontrar el índice (clase) con la probabilidad más alta
        prediction_encoded = np.argmax(pred_probabilities, axis=1)[0]
        
        # 4. Obtener el nombre del candidato
        prediction_name = le.inverse_transform([prediction_encoded])[0]
        
        # 5. Obtener el valor de esa probabilidad (confianza)
        confidence = pred_probabilities[0][prediction_encoded]
        
        # --- 6. Devolver la Respuesta ---
        return jsonify({
            'candidato_predicho': prediction_name,
            'probabilidad': round(confidence * 100, 2) # Enviar como porcentaje
        })
        
    except Exception as e:
        print(f"Error durante la predicción: {e}")
        return jsonify({'error': str(e)}), 400

# --- 7. Correr la Aplicación ---
if __name__ == '__main__':
    # '0.0.0.0' es crucial para que Docker pueda exponer el puerto
    app.run(host='0.0.0.0', port=5000, debug=True)