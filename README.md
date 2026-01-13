# E2E-system
# Система анализа данных такси

## Описание проекта

Полнофункциональная система сбора, хранения и анализа данных о поездках такси. Система автоматически генерирует реалистичные данные о поездках с учетом зависимостей между параметрами (цена зависит от расстояния и типа автомобиля, длительность от расстояния и т.д.) и предоставляет инструменты для их визуализации и анализа.

### Основные возможности:
- Автоматическая генерация реалистичных данных о поездках
- Хранение данных в PostgreSQL
- Интерактивные дашборды в Redash
- Анализ данных в Jupyter Notebook
- Полная контейнеризация с Docker Compose

---

### Компоненты:

1. **Generator** - Python-скрипт, генерирующий данные о поездках каждые 10 секунд
2. **PostgreSQL** - реляционная СУБД для хранения данных
3. **Redis** - хранилище для очереди задач Redash
4. **Redash** - платформа для визуализации данных (server + worker + scheduler)
5. **Jupyter Notebook** - среда для интерактивного анализа данных

---

## Структура данных

### Таблица `taxi_rides`

| Поле           | Тип          | Описание                          |
|----------------|--------------|-----------------------------------|
| id             | SERIAL       | Уникальный идентификатор поездки  |
| timestamp      | TIMESTAMP    | Время поездки                     |
| from_address   | VARCHAR(255) | Адрес отправления                 |
| to_address     | VARCHAR(255) | Адрес назначения                  |
| distance_km    | DECIMAL(5,2) | Расстояние в километрах (1-50)    |
| price          | DECIMAL(10,2)| Стоимость поездки (100-3000 руб)  |
| rating         | DECIMAL(3,1) | Рейтинг поездки (1.0-5.0)         |
| vehicle_type   | VARCHAR(20)  | Тип авто (economy/comfort/business)|
| duration_min   | INTEGER      | Длительность поездки (5-120 мин)  |
| payment_method | VARCHAR(10)  | Способ оплаты (cash/card)         |
| created_at     | TIMESTAMP    | Время создания записи             |


Имитация реальных зависимостей в генерируемых данных:

- **Цена** = Базовая цена + (Расстояние × Тариф за км) ± 10%
  - Economy: 100₽ + 25₽/км
  - Comfort: 150₽ + 35₽/км
  - Business: 250₽ + 50₽/км
    
- **Распределение типов авто**: Economy (60%), Comfort (30%), Business (10%)

---

### Установка и запуск

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/wiccdt/E2E-system.git
   cd "Путь до репозитория на вашем компьютере"
   ```

2. **Запустите систему:**
   ```bash
   docker-compose up -d --build
   ```

3. **Дождитесь генерации первых данных** (~30 секунд)

---

## Доступ к сервисам

| Сервис          | URL                        | Описание                    |
|-----------------|----------------------------|-----------------------------|
| Redash          | http://localhost:5000      | Дашборды и визуализации     |
| Jupyter         | http://localhost:8888      | Анализ данных               |
| PostgreSQL      | localhost:5432             | База данных (для клиентов)  |

### Учетные данные PostgreSQL:
```
Host: localhost (или postgres внутри Docker)
Port: 5432
Database: taxi_db
User: root
Password: qwerty
```

---

## Настройка Redash (первый запуск)

### 1. Регистрация
1. Откройте http://localhost:5000
2. Создайте аккаунт администратора
3. Придумайте пароль и войдите в систему

### 2. Подключитесь к базе данных
   ```
   Name: Taxi Database
   Host: postgres
   Port: 5432
   User: root
   Password: qwerty
   Database Name: taxi_db
   ```
5. Нажмите **Test Connection** → **Должно быть Success**

### 3. Создание запросов (Query)

#### Query 1: Зависимость цены от расстояния
```sql
SELECT 
    distance_km,
    price,
    vehicle_type,
    rating
FROM taxi_rides
ORDER BY distance_km;
```
**Визуализация:** Chart / Scatter 

#### Query 2: Средняя стоимость по типам автомобилей
```sql
SELECT 
    vehicle_type AS "Тип автомобиля",
    COUNT(*) AS "Количество поездок",
    ROUND(AVG(price), 2) AS "Средняя цена (руб)",
    ROUND(AVG(distance_km), 2) AS "Среднее расстояние (км)",
    ROUND(AVG(rating), 2) AS "Средний рейтинг"
FROM taxi_rides
GROUP BY vehicle_type
ORDER BY AVG(price) DESC;
```
**Визуализация:** Chart / Bar

#### Query 3: Распределение по способам оплаты
```sql
SELECT 
    payment_method AS "Способ оплаты",
    COUNT(*) AS "Количество",
    ROUND(SUM(price), 2) AS "Общая сумма (руб)",
    ROUND(AVG(price), 2) AS "Средний чек (руб)"
FROM taxi_rides
GROUP BY payment_method;
```
**Визуализация:** Chart / Pie

#### Query 4: Распределение по типам автомобилей
```sql
SELECT 
    vehicle_type,
    COUNT(*) as trips_count,
    AVG(price) as avg_price,
    AVG(rating) as avg_rating,
    AVG(distance_km) as avg_distance
FROM trips
GROUP BY vehicle_type
ORDER BY trips_count DESC;
```
**Визуализация:** Chart / Pie

### 4. Создание дашборда
1. **Dashboards** → **New Dashboard**
2. Введите название: "Здесь ваше название"
3. **Add Widget** → выберите созданные визуализации
4. Расположите виджеты на дашборде
5. **Publish Dashboard**

---

## Работа с Jupyter Notebook

1. **Откройте Jupyter:**
   ```
   http://localhost:8888
   ```

2. **Создайте новый notebook:**
   - Нажмите **New** → **Python 3**
   - Назовите файл `здесь ваше название`

3. **Пример кода для анализа:**
Приведён в папке notebooks/analysis.ipynb

## Скриншоты дашборда

### Общий вид дашборда
![Общий вид дашборда](../screenshots/dashboard.png)

### Зависимость цены от расстояния
![Зависимость цены от расстояния](../screenshots/img_1.png)

### Средняя стоимость по типам автомобилей
![Средняя стоимость по типам автомобилей](../screenshots/img_2.png)

### Распределение по способам оплаты
![Распределение по способам оплаты](../screenshots/img_3.png)

### Распределение по типам автомобилей
![Распределение по типам автомобилей](../screenshots/img_4.png)
