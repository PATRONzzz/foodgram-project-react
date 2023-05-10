<h1  style="margin-left: 0"><img  src='https://user-images.githubusercontent.com/60087209/230705080-f7863f40-6753-463b-b5be-2c407e404d86.png'  width='30'  
style=" position: relative; top: 0.3ch; margin-right: 0ch"> api_yamdb</h1>
  


Проект api_yamdb является бэкенд составляющей социальной сети **YaMDb**. Проект собирает отзывы пользователей на произведения.

**_Статус workflow_**
![example workflow](https://github.com/PATRONzzz/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

**_Адрес сервера: 158.160.60.92_**

**_В api_yamdb реализованы эндпоинты для:_**

- Регистрация пользователей и выдача токенов,
- Категории (типы) произведений
- Категории жанров
- Произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
- Отзывы
- Комментарии к отзывам
- Пользователи

## Поддерживаемые оперционные системы

![Linux](https://img.shields.io/badge/Linux-black?style=flat&logo=Linux&logoColor=white&color=2d2d2d)![Mac](https://img.shields.io/badge/macOS-black?style=flat&logo=Apple&logoColor=black&color=white)


## Технологии
- Django rest_framework 
- Django rest_framework_simplejwt
- Django django_filters
- Git
- Docker
- NGINX
- GUNICORN
- POSTGRES

## Подготовка
<details>

<summary><b  style="font-size: 1.1rem;">1. Клонирование репазитория </b></summary>

```
git clone https://github.com/PATRONzzz/yamdb_final.git

```
  
</details>

  
<details>

<summary><b  style="font-size: 1.1rem;">2. Установка Docker, Docker Compose </b></summary>

**На примере Linux Ubuntu 20.04**

```
# Установка утилиты для скачивания файлов
sudo apt install curl
# Скрипт 
docker.com -o get-docker.sh
# Эта команда запустит его
sh get-docker.sh   
# Обновить список пакетов
sudo apt update

```

```
# Добавьте ключ GPG для подтверждения подлинности в процессе установки
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

```

```
# Установить необходимые пакеты для загрузки через https
sudo apt install \
  apt-transport-https \
  ca-certificates \
  curl \
  gnupg-agent \
  software-properties-common -y 
```

```
# Добавьте репозиторий Docker в пакеты apt
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" 
# Так как в APT был добавлен новый репозиторий, снова обновите индекс пакетов
sudo apt update 
```

```
# Установка
sudo apt install docker-ce docker-compose -y 
```

Инструкция по установке есть [в официальной документации Docker](https://docs.docker.com/engine/install/ubuntu/)


</details>

## Развертывание
<details>

<summary><b  style="font-size: 1.1rem;">1. Расположение </b></summary>

```
#Переход к расположению docker-compose.yaml
cd /infra/

```
</details>

<details>

<summary><b  style="font-size: 1.1rem;">2. Шаблон переменных .env </b></summary>

```
# Укажите, что используете postgresql
DB_ENGINE=django.db.backends.postgresql
# Укажите имя созданной базы данных
DB_NAME=yatube
# Укажите имя пользователя
POSTGRES_USER=yatube_user
# Укажите пароль для пользователя
POSTGRES_PASSWORD=xxxyyyzzz
# Укажите localhost
DB_HOST=127.0.0.1
# Укажите порт для подключения к базе
DB_PORT=5432 
```
</details>


<details>

<summary><b  style="font-size: 1.1rem;">3. Запуск docker-compose </b></summary>

```
docker-compose up -d --build 

```
</details>


<details>

<summary><b  style="font-size: 1.1rem;">4. Миграции </b></summary>

```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```
</details>

<details>
<summary><b  style="font-size: 1.1rem;">5. Заполнение базы данных (при наличии дампа) </b></summary>

```
docker-compose exec web python manage.py loaddata path/to/your/json


```
</details>

## Остановка сервисов
```
# остановка запущенных контейнеров
docker-compose down
```
Подробнее в документации [docker compose down](https://docs.docker.com/engine/reference/commandline/compose_down/) 




## Документация  [api_yamdb](http://localhost/redoc/) 

**Пример**

POST .../api/v1/titles/

```
{
    "name": "string",
    "year": 0,
    "description": "string",
    "genre": [
        "string"
    ],
    "category": "string"
}
```
Ответ

```
{
    "id": 0,
    "name": "string",
    "year": 0,
    "rating": 0,
    "description": "string",
    "genre": [
        {
        "name": "string",
        "slug": "string"
        }
    ],
    "category": {
        "name": "string",
        "slug": "string"
    }
}
```

## Автор

- [PATRONzzz (Python-разработчика - разработчик 3)](https://github.com/PATRONzzz)