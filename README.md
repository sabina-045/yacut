#### Yacut - сервис укорачивания ссылок.

Клонируем репозиторий и переходим в него в командной строке:

```
git clone git@github.com:sabina-045/yacut.git
```

```
cd yacut
```

Cоздаем и активируем виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS:

    ```
    source venv/bin/activate
    ```

* Если у вас windows:

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Создаем репозиторий для миграций:

```
flask db init
```

Создаем миграцию:

```
flask db migrate -m "name of migration"
```
Применяем миграцию:

```
flask db upgrade
```

Запускаем приложение, набрав в терминале:

```
flask run
```
#### Эндпойнты:
/api/id/ — POST-запрос на создание новой короткой ссылки;
/api/id/<short_id>/ — GET-запрос на получение оригинальной ссылки по указанному короткому идентификатору

</br>

> Команда создателей:
Яндекс Практикум, Сабина Гаджиева.
