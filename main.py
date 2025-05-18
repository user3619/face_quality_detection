from fastapi import FastAPI, HTTPException, UploadFile, File, Request
import logging
import os
import time
from tensorflow.keras.models import load_model
from api.prediction import predict
from api.prediction_results import result as prediction_result_texts  

logging.basicConfig(
    filename="server.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = FastAPI()

MODEL_PATH = os.path.join(os.path.dirname(__file__), "Model", "Neural_model1.h5")

logging.info(f"Проверяю модель по пути: {os.path.abspath(MODEL_PATH)}")
if not os.path.exists(MODEL_PATH):
    logging.error(f"Модель не найдена: {MODEL_PATH}")
    raise FileNotFoundError(f"Модель не найдена: {MODEL_PATH}")

try:
    model = load_model(MODEL_PATH, compile=False)
    logging.info(f"Модель успешно загружена: {MODEL_PATH}")
except Exception as e:
    logging.error(f"Ошибка загрузки модели: {e}")
    raise Exception(f"Не удалось загрузить модель: {e}")

@app.post("/predict")
async def predict_acne(file: UploadFile = File(...), request: Request = None):
    try:
        filename = file.filename.lower()
        if not filename.endswith(('.jpg', '.jpeg', '.png')):
            raise HTTPException(status_code=400, detail="Неподдерживаемый формат. Используйте JPG или PNG.")

        contents = await file.read()
        if len(contents) > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="Файл слишком большой. Максимум 10 МБ.")

        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as buffer:
            buffer.write(contents)

        client_host = request.client.host if request else 'unknown'
        logging.info(f"[{client_host}] Получено изображение: {file.filename}")

        result = predict(temp_path, model)
        predicted_class = result['predicted_class']
        advice = result['advice']

        logging.info(f"Результат анализа: {predicted_class}")

        time.sleep(0.1)
        if os.path.exists(temp_path):
            os.remove(temp_path)

        return {"predicted_class": predicted_class, "advice": advice, **{k: v for k, v in result.items() if k not in ['predicted_class', 'advice']}}

    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Ошибка в /predict: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка обработки изображения: {str(e)}")
