# Рекоменбук - сервис рекомендации книг для библиотек
## Ресурс
http://178.154.241.46:4985/
## Данные авторизации
credentials: https://docs.yandex.ru/docs/view?url=ya-disk-public%3A%2F%2FEEEAUEMOwR2HsBamb%2FKxg7To7F0vKbD80WvRvh5GZFCfFPzpXxDgVV0S24f1r3cZq%2FJ6bpmRyOJonT3VoXnDag%3D%3D%3A%2Fcredentials.csv&name=credentials.csv&nosw=1

## Запуск
1. **Склонировать репозиторий командой**
   > git clone https://github.com/bronsoun/recommendbook.git
4. **Установить необходимые библиотеки командой**
   > pip3 install -r /web/requirements.txt
6. **Установить миграции последовательностью команд**
   > python3 manage.py makemigrations
   >> python3 manage.py migrate
8. **Запустить проект командой**
   > python3 manage.py runserver
