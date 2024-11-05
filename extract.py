# локальная функция проверки вложенного сообщения
from PIL import Image

def extract_password_from_image(image_path):
    image = Image.open(image_path)
    pixels = image.load()

    binary_message = ''
    for y in range(image.height):
        for x in range(image.width):
            pixel = pixels[x, y]
            r, g, b = pixel[:3]
            binary_message += str(r & 1)

    message = ''
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        char = chr(int(byte, 2))
        if char == '\0':
            break
        message += char

    return message

# # Использование
# image_path = 'static/uploads/Shrek_(character).png'  # Замените на имя вашего файла
# print("Извлечённый пароль:", extract_password_from_image(image_path))
