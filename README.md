
# Rishat_test_assignment

Ссылка на задание: [Тестовое задания для Python разработчика](https://docs.google.com/document/d/1RqJhk-pRDuAk4pH1uqbY9-8uwAqEXB9eRQWLSMM_9sI/edit?usp=sharing)

Тестовый сервер на [paythonanywere.com](http://andyplo.pythonanywhere.com/order/1/)
Для быстрой проверки:

- доступ в Django Admin панель: пользователь admin, пароль admin;
- созданы предметы с ID 1, 2 и 3;
- созданы заказы с ID 1, 2 и 3;

## Реализация задания

### Выполнена минимальная версия задания

    [GET] /item/{id}

Простая HTML страница с информацией о выбранном предмете и кнопкой "Купить".  По нажатию на кнопку происходит запрос на `/buy/{id}`, получение session_id. С помощью JS библиотеки Stripe происходит редирект на Checkout форму.

     [GET] /buy/{id}

Получение Stripe Session Id:

    {   
        sessionId: "sessionId"
    }

### Выполнены бонусные задачи

 1. Модель **Order** - заказ, содержащий предметы и их количество, информацию о скидке и налоге.
 2. Модели **Discount** и **Tax**, связанные с соответствующими атрибутами при создании платежа Stripe.
 3. `[GET] /order/{id}/` - создает html-страницу с данными заказа и кнопкой "Купить", которая переадресует на `/buy-order/{id}/`
 4. `[GET] /buy-order/{id}/`- создает stripe-сессию для оплаты заказа с учетом атрибутов tax и discount.
 5. Реализован просмотр и заполнение моделей в Django Admin панели.
 6. Использованы environment variables.
 7. Реализован запуск через Docker.
 8. Приложение запущено на тестовом сервере <http://andyplo.pythonanywhere.com/order/1/>

## Установка и запуск docker-compose

1. В директории `/rishat_test_assignment/infra` создайте файл `.env`

2. Шаблон для заполнения `.env` находится в `/rishat_test_assignment/infra/.env.example`

3. Выполните команду `docker-compose up -d --buld`

4. Выполните миграции `docker-compose exec web python manage.py migrate`

5. Создайте суперюзера `docker-compose exec web python manage.py createsuperuser`

6. Соберите статику `docker-compose exec web python manage.py collectstatic --no-input`

7. Заполните базу `docker-compose exec web python manage.py loaddata db.json`
  
## Автор

Андрей Плотников (Andy.Plo@yandex.ru)
