Проект Курсовой работы
Стеганографический алгоритм в интернете вещей

1. Запуск
  Для запуска программы, необходимо скачать целиком архив с кодом, распаковать его. Далее, нужно перейти в директорию .\dist и запустить app.exe
2. Проверка работы
   После запуска app.exe перейти на http:\\127.0.0.1:5000 или на другой адрес, написанный в терминале
   2.1 Функционал входа в систему
   При переходе по указанному адресу должна быть видна панель входа на сайт, на данный момент реализованы 2 пользователя (admin - пароль admin; user - пароль user) при заходе как любой из этих пользователей, можно увидеть страницу 'dashboard'.
   
   2.2 Функционал вложения пароля в изображение
   Для вложения пароля в изображение необходимо нажать на соответствующую кнопку на странице, после чего изображение со вложенным паролем отобразиться на экране, после загрузки которого, его можно будет использовать вместо пароля.

   2.3 Функционал проверки пароля в изображении
   Для проверки вложенного изображения на содержащийся в нем пароль, необходимо перейти по соответствующей ссылке и загрузить непосредственно изображение

Замечание: В диерктории .\dist\static\uploads уже находятся примеры изображений без ключа и с ключом соответственно
