import random
import psycopg2
import traceback
import time
from datetime import datetime, timedelta

time.sleep(10)

ADDRESSES = [
    "ЖК Северное сияние",
    "ЖК Центральный парк",
    "ЖК Солнечный берег",
    "ЖК Лесная поляна",
    "ЖК Речной вокзал",
    "ЖК Город мечты",
    "ЖК Уютный квартал",
    "ЖК Новый город",
    "ЖК Зеленый остров",
    "ЖК Парковый проспект",
    "Деловой центр 'Столичный'",
    "Бизнес-центр 'Плаза'",
    "Сити-центр 'Нева'",
    "БЦ 'Европа'",
    "БЦ 'Северная башня'",
    "БЦ 'Гринвич'",
    "БЦ 'Москва-Сити'",
    "БЦ 'Аметист'",
    "БЦ 'Рублевский'",
    "БЦ 'Форум'",
    "Центральный автовокзал",
    "Северный автовокзал",
    "Южный автовокзал",
    "Железнодорожный вокзал 'Центральный'",
    "Вокзал 'Восточный'",
    "Вокзал 'Западный'",
    "Речной вокзал",
    "Морской вокзал",
    "Аэровокзал",
    "Международный аэропорт 'Шереметьево'",
    "Аэропорт 'Домодедово'",
    "Аэропорт 'Внуково'",
    "Аэропорт 'Пулково'",
    "Аэропорт 'Кольцово'",
    "Аэропорт 'Толмачево'",
    "Аэропорт 'Храброво'",
    "ТРЦ 'Мега'",
    "ТЦ 'Атриум'",
    "ТЦ 'Галерея'",
    "ТЦ 'Океан'",
    "ТЦ 'Континент'",
    "ТЦ 'Колизей'",
    "ТЦ 'Планета'",
    "ТЦ 'Светофор'",
    "ТЦ 'Радуга'",
    "ТЦ 'Версаль'",
    "Главный корпус университета",
    "Университетский городок",
    "Политехнический институт",
    "Медицинская академия",
    "Экономический университет",
    "Технический колледж",
    "Школа №1",
    "Лицей №25",
    "Гимназия №3",
    "Городская больница №1",
    "Клиническая больница",
    "Роддом №3",
    "Детская больница",
    "Стоматологическая поликлиника",
    "Диагностический центр",
    "Медгородок",
    "Стадион 'Локомотив'",
    "Стадион 'Динамо'",
    "Спорткомплекс 'Олимпийский'",
    "Ледовый дворец",
    "Бассейн 'Волна'",
    "Фитнес-клуб 'Здоровье'",
    "Спортзал 'Атлет'",
    "Кинотеатр 'Космос'",
    "Театр драмы",
    "Театр оперы и балета",
    "Концертный зал 'Филармония'",
    "Цирк",
    "Зоопарк",
    "Аквапарк 'Нептун'",
    "Боулинг-центр 'Страйк'",
    "Центральный парк культуры",
    "Парк Победы",
    "Ботанический сад",
    "Лесопарк 'Дубки'",
    "Набережная реки",
    "Сквер у фонтанов",
    "Парк аттракционов",
    "Гостиница 'Европа'",
    "Отель 'Метрополь'",
    "Гостиница 'Центральная'",
    "Отель 'Премьер'",
    "Гостиница 'Турист'",
    "Отель 'Астория'",
    "Гостиница 'Россия'",
    "Ресторан 'У озера'",
    "Кафе 'Бриз'",
    "Ресторан 'Старый город'",
    "Кофейня 'Амстердам'",
    "Ресторан 'Восточный'",
    "Пиццерия 'Италия'",
    "Мэрия города",
    "Администрация района",
    "Почтамт",
    "Отделение полиции",
    "Пожарная часть",
    "Суд",
    "Прокуратура",
    "Завод 'Металлист'",
    "Фабрика 'Текстиль'",
    "Автозавод",
    "Нефтеперерабатывающий завод",
    "Пищевой комбинат",
    "Строительный комбинат",
    "Площадь Революции",
    "Красная площадь",
    "Памятник основателям",
    "Выставочный центр",
    "Музей изобразительных искусств",
    "Библиотека им. Ленина",
    "Архив",
    "Обсерватория"
]

PAYMENT_METHODS = [
    "card",
    "cash"
]

VEHICLE_TYPE = [
    "economy",
    "comfort",
    "business"
]

PRICE_PER_KM = {
    "economy": 25,
    "comfort": 35,
    "business": 50
}

BASE_PRICE = {
    "economy": 100,
    "comfort": 150,
    "business": 250
}

try:
    connection = psycopg2.connect(
        host="postgres",
        database="taxi_db",
        user="root",
        password="qwerty",
        port=5432
    )
    print("Connected successfully", flush=True)
    cursor = connection.cursor()

    while True:
        time.sleep(1)

        current_time = datetime.now() - timedelta(days=7)
        cursor.execute("SELECT MAX(timestamp) FROM taxi_rides")
        max_time_result = cursor.fetchone()
        if max_time_result and max_time_result[0]:
            base_time = max_time_result[0].replace(second=0, microsecond=0)
            random_minutes = random.randint(1, 20)
            current_time = base_time + timedelta(minutes=random_minutes)
        else:
            current_time = datetime.now() - timedelta(days=7)
            current_time = current_time.replace(second=0, microsecond=0)

        from_address_choice = random.choice(ADDRESSES)
        to_address_choice = random.choice([address for address in ADDRESSES if address != from_address_choice])
        vehicle_type = random.choices(
            VEHICLE_TYPE,
            weights=[60, 30, 10],
            k=1
        )[0]
        distance = round(random.uniform(1.0, 50.0), 2)
        price = round((BASE_PRICE[vehicle_type] + (distance * PRICE_PER_KM[vehicle_type])) * random.uniform(0.9, 1.1), 2)

        new_ride = {
            "timestamp": current_time,
            "from_address": from_address_choice,
            "to_address": to_address_choice,
            "distance_km": distance,
            "price": price,
            "rating": round(random.uniform(1.0, 5.0), 1),
            "vehicle_type": vehicle_type,
            "duration_min": random.randint(5, 120),
            "payment_method": random.choice(PAYMENT_METHODS),
        }

        sql = '''
        INSERT INTO taxi_rides
        (timestamp, from_address, to_address, distance_km, price, 
        rating, vehicle_type, duration_min, payment_method)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        cursor.execute(sql,(
                       new_ride["timestamp"],
                       new_ride["from_address"],
                       new_ride["to_address"],
                       new_ride["distance_km"],
                       new_ride["price"],
                       new_ride["rating"],
                       new_ride["vehicle_type"],
                       new_ride["duration_min"],
                       new_ride["payment_method"]))
        connection.commit()
        cursor.execute("SELECT * FROM taxi_rides ORDER BY id DESC LIMIT 1")
        last_record = cursor.fetchone()
        if last_record:
            print(f"Take from {last_record[2]}", flush=True)

except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()
