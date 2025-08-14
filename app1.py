from fastapi import FastAPI
from fastapi.responses import JSONResponse
from schema.user_input import UserInput
from models.predict import predict_output, model, MODEL_VERSION

app = FastAPI(title="Insurance Premium Predictor", version="1.0.0")

@app.get('/')
def home():
    return {'message': 'Insurance premium predictor'}

@app.get('/health')
def health_check():
    return {
        'status': 'OK',
        'version': MODEL_VERSION,
        'model_loaded': model is not None
    }

@app.post('/predict')  
def predict_premium(data: UserInput):
    user_input = {
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }

    prediction = predict_output(user_input)
    
    try:
        input_values = list(user_input.values())
        probabilities = model.predict_proba([input_values])[0]
        class_names = model.classes_ if hasattr(model, 'classes_') else [f"Class_{i}" for i in range(len(probabilities))]
        class_probabilities = dict(zip(class_names, probabilities.tolist()))
        confidence = max(probabilities)
    except Exception as e:
        print(f"Error calculating probabilities: {e}")
        class_probabilities = {}
        confidence = 1.0

    return JSONResponse(
        status_code=200,
        content={
            'response': {
                'predicted_category': prediction,
                'confidence': float(confidence),
                'class_probabilities': class_probabilities,
                'user_input': user_input
            }
        }
    )