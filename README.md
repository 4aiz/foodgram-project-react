# https://4aizFoodgram.hidehost.me
## login and password to admin
* **login**: admin
* **password**: admin

# Проект Foodgram:

Как часто мы хотели что-то приготовить, но не знали что? А даже если знали что, приходя в магазин или, заказывая продукты на дом, забывали какой-либо ингредиент. Теперь все это не важно, ведь проект Foodgram специально придуман для того, чтобы больше таких неприятных ситуаций не было. 

Foodgram - программа-ассистент, который поможет Вам создать свое блюдо, а также сохранить блюда других авторов в избранном. Если захотите что-то из понравившегося приготовить, просто добавьте нужный рецепт в корзину и всё, ингредиенты уже готовы к выгрузке - нажмите "Скачать список покупок". 

Теперь Вы никогда не ошибетесь и не забудете что-то, ведь Foodgram всегда под рукой. 

# Об Авторе:

Автором идеи данного проекта выступает вся команда Yandex. 
* Fronted - Команда Яндекса
* Backend, CI/CD, Docker - Кириллов Всеволод (https://github.com/4aiz) 

# Как запустить проект:

### Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:4aiz/foodgram-project-react.git
```

```
cd foodgram-project-react
```

### Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```
### Перейти в рабочую директорию

```
cd backend/
```

### Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

### Выполнить миграции:

```
python3 manage.py migrate
```

### Запустить проект:

```
python3 manage.py runserver
```

### Список используемых библиотек:

* asgiref==3.7.2
* atomicwrites==1.4.1
* attrs==22.1.0
* certifi==2022.9.24
* cffi==1.15.1
* chardet==3.0.4
* click==8.1.3
* colorama==0.4.6
* coreapi==2.3.3
* coreschema==0.0.4
