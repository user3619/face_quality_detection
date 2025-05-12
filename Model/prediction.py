import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model

def prediction_result(prediction):
    pass


def predict(image_path, model):
    img = image.load_img(image_path, target_size=(512, 512))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0
    prediction = model.predict(img_array)
    return prediction_result(prediction)


model = load_model('Model/Neural_model.keras')
image_path = 'path_to_your_image'

print(predict(image_path, model))