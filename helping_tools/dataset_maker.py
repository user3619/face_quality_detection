import os
# Программа для переименования картинок в более удобный формат - разделение на лица с акне и без них
# Имея удобные названия фото, можно начинать обучать нейросеть

acne_faces = 'название папки с фото'
non_acne_faces = 'название папки с фото'
i=0
for filename in os.listdir(acne_faces):
    try:
        i+=1
        os.rename('путь к файлу'+filename, 'тот же путь к файлу'+'face-'+str(i)+'-acne.jpg')
        print(f'Переименовано: {filename}')
    except Exception as e:
        print(f'Ошибка: {e}')

for filename in os.listdir(non_acne_faces):
    try:
        i+=1
        os.rename('путь к файлу'+filename, 'тот же путь к файлу'+'face-'+str(i)+'-non_acne.jpg')
        print(f'Переименовано: {filename}')
    except Exception as e:
        print(f'Ошибка: {e}')