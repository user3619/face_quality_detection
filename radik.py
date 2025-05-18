import telebot
from telebot import types
import requests
import os

bot = telebot.TeleBot('7761604165:AAF86f2zHBidKdurquVWFNMyKzCz8JyKQEo')

@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == "Привет":
        bot.send_message(message.chat.id, text="Привет! Я бот для анализа кожи. Отправляя фото, вы соглашаетесь на обработку данных. Фото удаляется после анализа. Напиши 'Задать вопрос' для меню!")
    elif message.text == "Задать вопрос":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Что может бот?")
        btn2 = types.KeyboardButton("Кожа")
        btn3 = types.KeyboardButton("Распознать тип кожи")
        btn4 = types.KeyboardButton("Помощь")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, btn3, btn4, back)
        bot.send_message(message.chat.id, text="Задай мне вопрос", reply_markup=markup)
    elif message.text == "Что может бот?":
        bot.send_message(message.chat.id, "Я анализирую кожу по фото, определяю тип (нормальная, сухая, жирная) и проблемы (акне, морщины), а также даю рекомендации по уходу!")
    elif message.text == "Кожа":
        bot.send_message(message.chat.id, text="Типы кожи:\n- Нормальная: сбалансированная, без излишней сухости или жирности.\n- Сухая: склонна к шелушению, требует увлажнения.\n- Жирная: склонна к блеску и акне, требует матирующих средств.\nОтправьте фото для анализа!")
    elif message.text == "Распознать тип кожи":
        bot.send_message(message.chat.id, text="Отправьте фото лица. Убедитесь, что:\n- Лицо хорошо освещено.\n- Фото сделано без фильтров.\n- Лицо занимает большую часть кадра.")
    elif message.text == "Помощь":
        bot.send_message(message.chat.id, text="Чем могу помочь? Отправьте фото или выберите 'Задать вопрос'.")
    elif message.text == "Вернуться в главное меню":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Помощь")
        button2 = types.KeyboardButton("Задать вопрос")
        button3 = types.KeyboardButton("Привет")
        markup.add(button1, button2, button3)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, text="На такую команду я не запрограммирован. Напиши 'Привет' или отправь фото.")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    bot.send_message(message.chat.id, "Фото получено, начинаю анализ... ⌛️")
    temp_path = "temp_image.jpg"
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(temp_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        if not os.path.exists(temp_path):
            bot.send_message(message.chat.id, "Не удалось сохранить изображение. Проверь доступ к папке.")
            return

        with open(temp_path, 'rb') as f:
            files = {'file': f}
            response = requests.post("http://localhost:8000/predict", files=files)

        if response.status_code == 200:
            data = response.json()
            predicted_class = data.get('predicted_class', 'неизвестно')
            advice = data.get('advice', 'Нет рекомендаций.')

            # Форматирование вероятностей
            probabilities = {k: v for k, v in data.items() if k not in ['predicted_class', 'advice']}
            probs_text = ""
            for k, v in probabilities.items():
                try:
                    probs_text += f"{k}: {float(v):.2%}\n"
                except (ValueError, TypeError):
                    probs_text += f"{k}: {v}\n"

            result_message = (
                f"🔍 Класс: *{predicted_class}*\n"
                f"📊 Вероятности:\n{probs_text}\n"
                f"📋 Советы:\n{advice}"
            )

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn = types.KeyboardButton("Отправить новое фото")
            markup.add(btn)
            bot.send_message(message.chat.id, result_message, reply_markup=markup, parse_mode="Markdown")
        else:
            bot.send_message(message.chat.id, "Ошибка при анализе изображения. Попробуйте позже.")

    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {e}")

    finally:
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass

bot.polling(none_stop=True)
