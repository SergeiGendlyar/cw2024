# локальные функции вложения и извлечения сообщения из изображения

from PIL import Image


def embed_message(image_path, message, output_path):
    # Открываем изображение
    image = Image.open(image_path)

    # Проверяем режим изображения
    print(f"Режим изображения: {image.mode}")  # Выводим режим изображения для отладки

    # Если изображение в неподдерживаемом формате, конвертируем его в RGB
    if image.mode not in ('RGB', 'RGBA', 'L'):
        print("Конвертация изображения в RGB")
        image = image.convert('RGB')

    pixels = image.load()  # Получаем доступ к пикселям изображения

    # Преобразуем сообщение в двоичный формат
    message += '\0'  # Добавляем символ конца строки
    binary_message = ''.join(format(ord(char), '08b') for char in message)

    # Проверяем, достаточно ли пикселей для встраивания сообщения
    if len(binary_message) > image.width * image.height:
        raise ValueError("Сообщение слишком длинное для данного изображения.")

    # Встраиваем сообщение в изображение
    data_index = 0
    for y in range(image.height):
        for x in range(image.width):
            if data_index < len(binary_message):
                # Получаем текущий пиксель
                pixel = pixels[x, y]

                # Обрабатываем разные режимы изображения
                if image.mode == 'RGB':
                    # Заменяем младший бит красного канала
                    r, g, b = pixel
                    r = (r & ~1) | int(binary_message[data_index])
                    pixels[x, y] = (r, g, b)
                elif image.mode == 'RGBA':
                    # Заменяем младший бит красного канала
                    r, g, b, a = pixel
                    r = (r & ~1) | int(binary_message[data_index])
                    pixels[x, y] = (r, g, b, a)
                elif image.mode == 'L':
                    # Для градаций серого, просто заменяем значение
                    gray = pixel
                    gray = (gray & ~1) | int(binary_message[data_index])
                    pixels[x, y] = gray
                else:
                    raise ValueError(
                        "Неподдерживаемый режим изображения.")  # Это сообщение теперь должно срабатывать реже

                data_index += 1
            else:
                break

    # Сохраняем измененное изображение
    image.save(output_path)
    print(f"Сообщение успешно встроено в изображение и сохранено как {output_path}")


# # Пример использования
# embed_message('input_image.png', 'Pay Gorn!', 'output_image.png')
#

def extract_messpage(image_path):
    # Открываем изображение
    image = Image.open(image_path)
    pixels = image.load()  # Получаем доступ к пикселям изображения

    binary_message = ''

    # Извлекаем младшие биты из пикселей
    for y in range(image.height):
        for x in range(image.width):
            pixel = pixels[x, y]

            # Обрабатываем разные режимы изображения
            if image.mode == 'RGB':
                r, g, b = pixel
                binary_message += str(r & 1)  # Извлекаем младший бит красного канала
            elif image.mode == 'RGBA':
                r, g, b, a = pixel
                binary_message += str(r & 1)  # Извлекаем младший бит красного канала
            elif image.mode == 'L':
                gray = pixel
                binary_message += str(gray & 1)  # Извлекаем младший бит значения серого цвета
            else:
                raise ValueError("Неподдерживаемый режим изображения.")

    # Преобразуем двоичный код обратно в строку
    message = ''
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i + 8]
        char = chr(int(byte, 2))  # Преобразуем 8-битные кусочки в символы
        if char == '\0':  # Если встретили символ конца строки, прекращаем извлечение
            break
        message += char

    return message


# Пример использования
extracted_message = extract_message('AK-74_1.png')
print(f"Извлеченное сообщение: {extracted_message}")