import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Book, Shop, Stock, Sale
import logging
import configparser


# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Чтение конфигурации из файла
config = configparser.ConfigParser()
config.read('config.ini')

# Установка соединения с базой данных
DSN = config['database']['dsn']
engine = sqlalchemy.create_engine(DSN)

# Создание таблиц
try:
    create_tables(engine)
    logger.info('Таблицы успешно созданы.')
except Exception as e:
    logger.error(f'Ошибка при создании таблиц: {e}')

Session = sessionmaker(bind=engine)
session = Session()


# Вносим данные об издателях:
try:
    pub1 = Publisher(name='Дмитрий Глуховский')
    pub2 = Publisher(name='Сергей Лукьяненко')
    pub3 = Publisher(name='Александр Пушкин')
    pub4 = Publisher(name='Лев Толстой')
    pub5 = Publisher(name='Джордж Оруэлл')

    session.add_all([pub1, pub2, pub3, pub4, pub5])
    session.commit()
    logger.info('Данные об издателях успешно добавлены.')
except Exception as e:
    logger.error(f'Ошибка при добавлении данных об издателях.')
    session.rollback()


# Вносим данные о книгах:
try:
    book1 = Book(title='Метро 2033', id_publisher=pub1.id)
    book2 = Book(title='Текст', id_publisher=pub1.id)
    book3 = Book(title='Будущее', id_publisher=pub1.id)
    book4 = Book(title='Дозоры" (серия)', id_publisher=pub2.id)
    book5 = Book(title='Лабиринт отражений', id_publisher=pub2.id)
    book6 = Book(title='Черновик', id_publisher=pub2.id)
    book7 = Book(title='Евгений Онегин', id_publisher=pub3.id)
    book8 = Book(title='Капитанская дочка', id_publisher=pub3.id)
    book9 = Book(title='Руслан и Людмила', id_publisher=pub3.id)
    book10 = Book(title='Война и мир', id_publisher=pub4.id)
    book11 = Book(title='Анна Каренина', id_publisher=pub4.id)
    book12 = Book(title='Смерть Ивана Ильича', id_publisher=pub4.id)
    book13 = Book(title='1984', id_publisher=pub5.id)
    book14 = Book(title='Скотный двор', id_publisher=pub5.id)
    book15 = Book(title='Дорога на Виген', id_publisher=pub5.id)

    session.add_all([book1, book2, book3, book4, book5, book6, book7,
                     book8, book9, book10, book11, book12, book13, book14, book15])
    session.commit()
    logger.info('Данные о книгах успешно добавлены.')
except Exception as e:
    logger.error(f'О(шибка при добавлении данных о книгах.')
    session.rollback()


# Вносим данные о магазинах:
try:
    shop1 = Shop(name='Библио-Глобус')
    shop2 = Shop(name='Читай-город')
    shop3 = Shop(name='Лабиринт')
    shop4 = Shop(name='Книжный магазин "Москва"')
    shop5 = Shop(name='Ozon')

    session.add_all([shop1, shop2, shop3, shop4, shop5])
    session.commit()
    logger.info('Данные об магазинах успешно добавлены.')
except Exception as e:
    logger.error(f'Ошибка при добавлении данных о магазинах.')
    session.rollback()


# Вносим данные о складских остатках:
try:
    stock1 = Stock(id_book=1, id_shop=1, count=189)
    stock2 = Stock(id_book=1, id_shop=2, count=12)
    stock3 = Stock(id_book=2, id_shop=3, count=124)
    stock4 = Stock(id_book=2, id_shop=4, count=17)
    stock5 = Stock(id_book=3, id_shop=5, count=176)
    stock6 = Stock(id_book=4, id_shop=1, count=16)
    stock7 = Stock(id_book=4, id_shop=2, count=16)
    stock8 = Stock(id_book=5, id_shop=2, count=164)
    stock9 = Stock(id_book=6, id_shop=3, count=64)
    stock10 = Stock(id_book=7, id_shop=1, count=684)
    stock11 = Stock(id_book=8, id_shop=3, count=68)
    stock12 = Stock(id_book=9, id_shop=4, count=5)
    stock13 = Stock(id_book=10, id_shop=3, count=74)
    stock14 = Stock(id_book=11, id_shop=5, count=20)
    stock15 = Stock(id_book=12, id_shop=1, count=8)
    stock16 = Stock(id_book=12, id_shop=3, count=26)
    stock17 = Stock(id_book=13, id_shop=3, count=68)
    stock18 = Stock(id_book=14, id_shop=5, count=564)
    stock19 = Stock(id_book=15, id_shop=3, count=58)

    session.add_all([stock1, stock2, stock3, stock4, stock5, stock6, stock7, stock8, stock9,
                     stock10, stock11, stock12, stock13, stock14, stock15, stock16, stock17,
                     stock18, stock19])
    session.commit()
    logger.info('Данные о складских остатках успешно добавлены.')
except Exception as e:
    logger.error(f'Ошибка при добавлении данных о складских остатках.')
    session.rollback()


# Вносим данные о продажах:
try:
    sale1 = Sale(price=1250, date_sale='2025-02-08', id_stock=1, count=10)
    sale2 = Sale(price=1150, date_sale='2025-02-08', id_stock=2, count=20)
    sale3 = Sale(price=1050, date_sale='2025-02-08', id_stock=3, count=15)
    sale4 = Sale(price=800, date_sale='2025-02-08', id_stock=4, count=65)
    sale5 = Sale(price=2000, date_sale='2025-02-08', id_stock=5, count=156)
    sale6 = Sale(price=2000, date_sale='2025-02-08', id_stock=6, count=156)
    sale7 = Sale(price=2100, date_sale='2025-02-08', id_stock=7, count=126)
    sale8 = Sale(price=2000, date_sale='2025-02-08', id_stock=8, count=156)
    sale9 = Sale(price=2020, date_sale='2025-02-28', id_stock=9, count=185)
    sale10 = Sale(price=2020, date_sale='2025-02-28', id_stock=10, count=548)
    sale11 = Sale(price=2120, date_sale='2025-02-28', id_stock=11, count=598)
    sale12 = Sale(price=3878, date_sale='2025-02-28', id_stock=12, count=58)
    sale13 = Sale(price=202, date_sale='2025-02-28', id_stock=13, count=5418)
    sale14 = Sale(price=202, date_sale='2025-02-28', id_stock=14, count=5418)
    sale15 = Sale(price=5000, date_sale='2025-02-28', id_stock=15, count=54118)
    sale16 = Sale(price=50, date_sale='2025-02-28', id_stock=16, count=1)
    sale17 = Sale(price=800, date_sale='2025-02-28', id_stock=17, count=5411)
    sale18 = Sale(price=800, date_sale='2025-02-28', id_stock=18, count=5411)
    sale19 = Sale(price=80000, date_sale='2025-02-28',
                  id_stock=19, count=514511)

    session.add_all([sale1, sale2, sale3, sale4, sale5, sale6, sale7, sale8, sale9,
                     sale10, sale11, sale12, sale13, sale14, sale15, sale16, sale17, sale18, sale19])
    session.commit()
    logger.info('Данные о продажах успешно добавлены.')
except Exception as e:
    logger.error(f'Ошибка при добавлении данных о продажах.')
    session.rollback()


# Функция для получения информации о продажах книг издателя:
def get_sales_info(result):
    try:
        query = session.query(Book.title, Shop.name, Sale.price,
                              Sale.date_sale).select_from(Shop).join(Stock).join(Book).join(Publisher).join(Sale)
        if result.isdigit():
            query = query.filter(Publisher.id == result).all()
        else:
            query = query.filter(Publisher.name.ilike(f'%{result}%')).all()

        if query:
            print(
                f'Информация о продажах книг данного издателя {result} в книжных магазинах: ')
            for title, name, price, date_sale in query:
                print(f'{title} | {name} | {price} | {date_sale}')
        else:
            print('Нет данных о продажах для указанного издателя.')
            logger.info(f'Нет данных о продажах для издателя: {result}')

    except Exception as e:
        logger.error(f'Ошибка при получении информации о продажах: {e}')


# Запрашиваем имя издателя:
if __name__ == "__main__":
    while True:
        user_input = input('Введите ID или имя издателя ("exit" для выхода): ')
        if user_input.lower() == 'exit':
            break

        get_sales_info(user_input)

# Отключаемся от БД (закрываем сессию)
session.close()
