import cv2
import numpy as np
import os

# Функция изменяет размер изображений (копирует каждое изображение с изменением разрешения)
# Можно использовать в дальнейшем, чтобы изменять разрешение изображений, полученных от пользователей
# На вход принимает исходную папку с изображениями, папку, в которую необходимо сохранить изменённые изображения и желаемое разрешение изображения
def resize_images(input_folder, output_folder, size=(1024, 1024)):

    # Если указанной папки, в которую нужно сохранять изображения, не существует, создаём новую
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Перебор всех файлов в исходной папке
    for filename in os.listdir(input_folder):
        try:
            img_path = os.path.join(input_folder, filename)
            img = cv2.imread(img_path)
            height, width = img.shape[:2]
            new_w, new_h = size
                
            # Изменение размера
            scale = max(new_w / width, new_h / height)
            new_w, new_h = int(width * scale), int(height * scale)
            resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
                    
            # Корректировка на случай, если длина и ширина не соответствуют заданным параметрам
            x = abs((new_w - new_w)) // 2
            y = abs((new_h - new_h)) // 2
            new_img = resized[y:y+new_h, x:x+new_w]

            if new_img.shape[0] < new_h or new_img.shape[1] < new_w:
                pad_h = max(0, new_h - new_img.shape[0])
                pad_w = max(0, new_w - new_img.shape[1])
                new_img = cv2.copyMakeBorder(
                                new_img, 
                                pad_h//2, pad_h - pad_h//2, 
                                pad_w//2, pad_w - pad_w//2, 
                                cv2.BORDER_CONSTANT, 
                                value=(0, 0, 0)
                )

            # Сохраняем новые изображения
            cv2.imwrite(os.path.join(output_folder, filename), new_img)
            print(f"Замена выполнена: {filename}")
        except Exception as e:
            print(f"Ошибка при обработке {filename}: {e}")