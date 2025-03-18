import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import Publisher, Book, Shop, Stock, Sale
import logging
import configparser

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Функция для чтения конфигурации


def read_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config

# Функция для установки соединения с базой данных


def create_session(dsn):
    engine = sqlalchemy.create_engine(dsn)
    Session = sessionmaker(bind=engine)
    return Session()

# Функция для загрузки данных из JSON-файла


def load_json_data(json_file):
    try:
        with open(json_file, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        logger.error('Файл не найден: %s', json_file)
        raise
    except json.JSONDecodeError:
        logger.error('Ошибка декодирования JSON-файла: %s', json_file)
        raise

# Функция для заполнения базы данных


def populate_database(session, data):
    model_map = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }

    for record in data:
        model = model_map.get(record.get('model'))
        if model:
            existing_record = session.query(
                model).filter_by(id=record.get('pk')).first()
            if existing_record:
                logger.info(
                    'Запись с ID %s уже существует, пропускаем.', record.get('pk'))
                continue
            session.add(model(id=record.get('pk'), **record.get('fields')))
            logger.info('Добавлена запись: %s с ID %s',
                        record.get('model'), record.get('pk'))
        else:
            logger.warning('Модель %s не найдена.', record.get('model'))

# Функция для получения полной информации


def output_full_info(session):
    try:
        query = session.query(Book.title, Shop.name, Sale.price, Sale.count, Sale.date_sale).join(Publisher).join(
            Stock).join(Shop).join(Sale)
        return query.all()
    except Exception as e:
        logger.error('Ошибка при выполнении запроса: %s', e)
        return []

# Функция для запроса информации по имени или ID


def query_publisher(session, publ_name):
    try:
        if publ_name.isnumeric():
            return session.query(Publisher).filter(Publisher.id == int(publ_name)).all()
        else:
            # Исправлено
            return session.query(Publisher).filter(Publisher.name.like(f'%{publ_name}%')).all()
    except Exception as e:
        logger.error('Ошибка при запросе: %s', e)
        return []


def main():
    # Чтение конфигурации
    config = read_config('config.ini')
    dsn = config['database']['dsn']

    session = None

    try:
        session = create_session(dsn)

        # Загрузка данных из JSON-файла
        data = load_json_data('tests_data.json')

        # Заполнение базы данных
        if data:  # Проверка наличия данных
            populate_database(session, data)
            session.commit()
            logger.info('Данные успешно добавлены в базу данных.')
        else:
            logger.warning('Нет данных для добавления в базу данных.')

        # Запрос информации
        publ_name = input('Введите имя писателя или ID для вывода: ')
        publishers = query_publisher(session, publ_name)
        if publishers:
            for publisher in publishers:
                print(publisher.name)
        else:
            print('Издатель не найден.')

        # Вывод полной информации
        full_info = output_full_info(session)
        for info in full_info:
            print(info)

    except Exception as e:
        logger.error('Произошла ошибка: %s', e)
        if session:
            session.rollback()
        logger.critical('Выполнение скрипта остановлено.')

    finally:
        if session:
            session.close()
            logger.info('Сессия закрыта.')


if __name__ == '__main__':
    main()
