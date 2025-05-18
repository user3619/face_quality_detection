import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from api.prediction_results import result as prediction_result_texts  

def load_and_preprocess_image(image_path):
    img = load_img(image_path, target_size=(512, 512))
    img_array = img_to_array(img) / 255.0
    return np.expand_dims(img_array, axis=0)  

def predict(image_path, model):
    img = load_and_preprocess_image(image_path)
    predictions = model.predict(img)[0]
    class_labels = ['non-acne', 'acne']
    result = {label: float(prob) for label, prob in zip(class_labels, predictions)}
    predicted_class = class_labels[np.argmax(predictions)]
    advice = prediction_result_texts.get(predicted_class, "Нет рекомендаций для данного класса.")
    result['predicted_class'] = predicted_class
    result['advice'] = advice

    return result
