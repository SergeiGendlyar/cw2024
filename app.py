from flask import Flask, render_template, request, redirect, url_for, session, send_file, flash
from PIL import Image
import os

# непосредственно веб-приложение
app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'  # Относительный путь к папке загрузок
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.secret_key = 'your_secret_key'

# Настройки пользователей
USERS = {
    'admin': 'admin',
    'user': 'user'
}

# Главная страница с формой входа
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form.get('password')
        file = request.files.get('file')

        # Проверка логина и пароля
        if login in USERS:
            if password and password == USERS[login]:
                session['username'] = login
                return redirect(url_for('dashboard'))
            elif file:
                # Если загружена фотография, проверяем пароль в фотографии
                file_path = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(file_path)
                extracted_password = extract_password_from_image(file_path)

                if extracted_password == USERS[login]:
                    session['username'] = login
                    return redirect(url_for('dashboard'))
                else:
                    return "Неправильный фото ключ"
            else:
                return "Неправильный логин или пароль"
        else:
            return "Неправильный логин или пароль"

    return render_template('index.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']

    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return "Нет файла"

            # Сохраняем исходное изображение
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)

            # Встраиваем пароль пользователя в изображение и сохраняем его с новым именем
            output_path = os.path.join(UPLOAD_FOLDER, f"embedded_{file.filename}")
            embed_password_in_image(file_path, USERS[username], output_path)

            # Отправляем обратно файл с вложенным паролем
            return send_file(output_path, mimetype='image/png')

    return render_template('dashboard.html', username=username)

# Страница проверки изображения (показывает пароль в фото)
@app.route('/check_photo', methods=['GET', 'POST'])
def check_photo():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        if 'file' not in request.files:
            return "Файл не выбран"

        file = request.files['file']
        if file.filename == '':
            return "Нет файла"

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        extracted_password = extract_password_from_image(file_path)

        return f"Извлечённый пароль: {extracted_password}"

    return render_template('check_photo.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Нет файла для загрузки')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('Не выбран файл')
            return redirect(request.url)

        # Сохраняем файл в `uploads`
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        flash('Файл успешно загружен')

        # Перенаправление или отправка файла в зависимости от логики
        return redirect(url_for('dashboard', filename=file.filename))
    return render_template('upload.html')

def embed_password_in_image(image_path, message, output_path):
    image = Image.open(image_path)
    pixels = image.load()

    # Добавляем конечный символ и переводим сообщение в двоичный формат
    message += '\0'
    binary_message = ''.join(format(ord(char), '08b') for char in message)

    # Проверка длины сообщения для встраивания
    if len(binary_message) > image.width * image.height:
        raise ValueError("Сообщение слишком длинное для данного изображения.")

    data_index = 0
    for y in range(image.height):
        for x in range(image.width):
            if data_index < len(binary_message):
                pixel = pixels[x, y]

                if isinstance(pixel, int):  # для градаций серого
                    pixel = (pixel & ~1) | int(binary_message[data_index])
                    pixels[x, y] = pixel
                else:
                    r, g, b = pixel[:3]  # для RGB изображений
                    r = (r & ~1) | int(binary_message[data_index])
                    pixels[x, y] = (r, g, b)

                data_index += 1
            else:
                break

    image.save(output_path)

def extract_password_from_image(image_path):
    image = Image.open(image_path)
    pixels = image.load()

    binary_message = ''
    for y in range(image.height):
        for x in range(image.width):
            pixel = pixels[x, y]

            if isinstance(pixel, int):  # для градаций серого
                r = pixel
            else:
                r, g, b = pixel[:3]  # для RGB изображений

            binary_message += str(r & 1)

    message = ''
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        char = chr(int(byte, 2))
        if char == '\0':  # Остановка на конечном символе
            break
        message += char

    return message

# Выход из системы
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
