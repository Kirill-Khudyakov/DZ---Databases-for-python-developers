import psycopg2
import logging


# Настройка логирования
logging.basicConfig(level=logging.INFO, filename='app.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Создание обработчика для ошибок
error_handler = logging.FileHandler('error.log')
error_handler.setLevel(logging.ERROR)

# Форматирование сообщений
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
error_handler.setFormatter(formatter)

# Добавление обработчика в корневой логгер
logging.getLogger().addHandler(error_handler)


# Функция, создающая структуру БД (таблицы).
def create_db(conn):

    with conn.cursor() as cur:
        try:
            cur.execute(
                'DROP TABLE IF EXISTS phones; DROP TABLE IF EXISTS customers;')
            cur.execute("""
                CREATE TABLE IF NOT EXISTS customers (
                    id SERIAL PRIMARY KEY,
                    client_name VARCHAR(100) NOT NULL,
                    client_surname VARCHAR(100) NOT NULL,
                    client_email VARCHAR(100) NOT NULL
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS phones (
                    phone VARCHAR(100) UNIQUE,
                    client_id INTEGER REFERENCES customers(id)
                );
            """)
            conn.commit()
            logging.info('База данных успешно создана.')
        except Exception as e:
            logging.error(f'Ошибка при создании базы данных: {e}')
            conn.rollback()


# Функция, позволяющая добавить нового клиента.
def add_new_client(conn):

    client_name = input('Введите имя клиента: ')
    client_surname = input('Введите фамилию клиента: ')
    client_email = input('Введите email клиента: ')

    with conn.cursor() as cur:
        try:
            cur.execute("""
                INSERT INTO customers (client_name, client_surname, client_email) 
                VALUES (%s, %s, %s) RETURNING id;
            """, (client_name, client_surname, client_email))
            client_id = cur.fetchone()[0]
            conn.commit()
            logging.info(f'Клиент добавлен с ID: {client_id}')
            return client_id
        except Exception as e:
            logging.error(f'Ошибка при добавлении клиента: {e}')
            conn.rollback()


# Функция, позволяющая добавить телефон для существующего клиента.
def add_phone(conn):

    client_id = input('Введите ID клиента: ')
    phone = input('Введите номер телефона: ')

    with conn.cursor() as cur:
        try:
            cur.execute("""
                INSERT INTO phones (client_id, phone) VALUES (%s, %s);
            """, (client_id, phone))
            conn.commit()
            logging.info(
                f'Телефон {phone} добавлен для клиента с ID: {client_id}')
        except Exception as e:
            logging.error(f'Ошибка при добавлении телефона: {e}')
            conn.rollback()


# Функция, позволяющая изменить данные о клиенте.
def change_client(conn):

    with conn.cursor() as cur:
        try:
            client_id = input(
                'Введите ID клиента, информацию которого вы хотите изменить: ')
            print('Для изменения информации о клиенте, нужно ввести команду:\n'
                  '1 - изменить имя\n'
                  '2 - изменить фамилию\n'
                  '3 - изменить email\n'
                  '4 - изменить номер телефона')

            command_symbol = int(input('Введите номер команды: '))

            if command_symbol == 1:
                input_name_customers = input('Введите новое имя: ')
                cur.execute("""
                    UPDATE customers SET client_name=%s WHERE id=%s;
                """, (input_name_customers, client_id))

            elif command_symbol == 2:
                input_surname_customers = input('Введите новую фамилию: ')
                cur.execute("""
                    UPDATE customers SET client_surname=%s WHERE id=%s;
                """, (input_surname_customers, client_id))

            elif command_symbol == 3:
                input_email_customers = input('Введите новый email: ')
                cur.execute("""
                    UPDATE customers SET client_email=%s WHERE id=%s;
                """, (input_email_customers, client_id))

            elif command_symbol == 4:
                input_phone_customers = input('Введите новый номер телефона: ')
                cur.execute("""
                    UPDATE phones SET phone=%s WHERE client_id=%s;
                """, (input_phone_customers, client_id))

            else:
                print('Неверная команда!')

            conn.commit()
            logging.info(f'Данные клиента с ID {client_id} успешно изменены.')
        except Exception as e:
            logging.error(f'Ошибка при изменении данных клиента: {e}')
            conn.rollback()


# Функция, позволяющая удалить телефон для существующего клиента.
def delete_phone(conn):

    with conn.cursor() as cur:
        try:
            client_id = input(
                'Введите ID клиента, телефон которого хотите удалить: ')
            phone_del = input(
                'Введите номер телефона, который хотите удалить: ')

            cur.execute("""
                DELETE FROM phones WHERE client_id=%s AND phone=%s;
            """, (client_id, phone_del))
            conn.commit()
            logging.info(
                f'Телефонный номер {phone_del} клиента с ID {client_id} успешно удалён!')
        except Exception as e:
            logging.error(f'Ошибка при удалении телефона: {e}')
            conn.rollback()


# Функция, позволяющая удалить существующего клиента.
def delete_client(conn):

    with conn.cursor() as cur:
        try:
            client_id = input('Введите ID клиента, которого хотите удалить: ')
            cur.execute("""
                DELETE FROM customers WHERE id=%s RETURNING id;
            """, (client_id,))
            deleted_id = cur.fetchone()
            if deleted_id:
                conn.commit()
                logging.info(f'Клиент с ID {deleted_id[0]} успешно удалён!')
            else:
                logging.warning(f'Клиент с ID {client_id} не найден.')
        except Exception as e:
            logging.error(f'Ошибка при удалении клиента: {e}')
            conn.rollback()


# Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.
def execute_query(cur, query, params):

    try:
        cur.execute(query, params)
        return cur.fetchall()
    except Exception as e:
        print(f'Ошибка при выполнении запроса: {e}')
        return []


def find_client(cur):

    print('Для поиска информации о клиенте, введите нужную команду: \n'
          '1 - Имя\n'
          '2 - Фамилия\n'
          '3 - email\n'
          '4 - Номер телефона\n'
          '5 - Поиск по нескольким критериям\n')

    command_find = input('Введите номер команды: ')

    criteria_map = {
        '1': 'client_name',
        '2': 'client_surname',
        '3': 'client_email',
        '4': 'phone'
    }

    if command_find in criteria_map:
        input_value = input(f'Введите {criteria_map[command_find]} клиента: ')
        query = f"""
                SELECT ct.id, ct.client_name, ct.client_surname, ct.client_email, p.phone
                FROM customers AS ct
                LEFT JOIN phones AS p ON p.client_id = ct.id
                WHERE {criteria_map[command_find]}=%s
                """
        result = execute_query(cur, query, (input_value,))
    elif command_find == '5':
        find_client_multiple_criteria(cur)
        return
    else:
        print('Некорректный ввод команды. Пожалуйста, попробуйте еще раз.')
        return

    if result:
        print('Найденные клиенты: ')
        for row in result:
            print(
                f'ID: {row[0]}, Имя: {row[1]}, Фамилия: {row[2]}, email: {row[3]}, Телефон: {row[4]}')
    else:
        print('Клиенты не найдены.')


def find_client_multiple_criteria(cur):

    print('Введите данные для поиска клиента (оставьте поле пустым, если не хотите использовать этот критерий):')
    input_name = input('Имя: ')
    input_surname = input('Фамилия: ')
    input_email = input('email: ')
    input_phone = input('Номер телефона: ')

    if not (input_name or input_surname or input_email or input_phone):
        print('Необходимо ввести хотя бы один критерий для поиска.')
        return

    query = """
            SELECT ct.id, ct.client_name, ct.client_surname, ct.client_email, p.phone
            FROM customers AS ct
            LEFT JOIN phones AS p ON p.client_id = ct.id
            WHERE 1=1
            """
    params = []
    if input_name:
        query += ' AND ct.client_name=%s'
        params.append(input_name)
    if input_surname:
        query += ' AND ct.client_surname=%s'
        params.append(input_surname)
    if input_email:
        query += ' AND ct.client_email=%s'
        params.append(input_email)
    if input_phone:
        query += ' AND p.phone=%s'
        params.append(input_phone)

    results = execute_query(cur, query, tuple(params))

    if results:
        print('Найденные клиенты: ')
        for row in results:
            print(
                f'ID: {row[0]}, Имя: {row[1]}, Фамилия: {row[2]}, email: {row[3]}, Телефон: {row[4]}')
    else:
        print('Клиенты не найдены')


# Функция, позволяющая получить данные всех клиентов
def get_all_clients(conn):
    with conn.cursor() as cur:
        try:
            cur.execute("""
                SELECT ct.id, ct.client_name, ct.client_surname, ct.client_email, p.phone
                FROM customers AS ct
                LEFT JOIN phones AS p ON p.client_id = ct.id;
            """)
            results = cur.fetchall()
            if results:
                print('Список всех клиентов:')
                for row in results:
                    print(
                        f'ID: {row[0]}, Имя: {row[1]}, Фамилия: {row[2]}, email: {row[3]}, Телефон: {row[4] if row[4] else "Нет телефона"}')
            else:
                print('Клиенты не найдены.')
        except Exception as e:
            logging.error(f'Ошибка при получении клиентов: {e}')


# Основная функция для работы с базой данных
def main():

    conn = None
    try:
        conn = psycopg2.connect(database='netology_db',
                                user='postgres', password='Samsung')
        logging.info('Соединение с базой данных успешно установлено.')
        create_db(conn)

        while True:
            print('\nВыберите действие: ')
            print('1 - Добавить клиента')
            print('2 - Добавить телефон для существующего клиента')
            print('3 - Изменить данные о клиенте')
            print('4 - Удалить телефон для существующего клиента')
            print('5 - Удалить существующего клиента')
            print('6 - Найти клиента по его данным')
            print('7 - Показать всех клиентов')
            print('8 - Выйти из программы')

            action = input('Введите номер действия: ')

            if action == '1':
                add_new_client(conn)

            elif action == '2':
                add_phone(conn)

            elif action == '3':
                change_client(conn)

            elif action == '4':
                delete_phone(conn)

            elif action == '5':
                delete_client(conn)

            elif action == '6':
                find_client(conn)

            elif action == '7':
                get_all_clients(conn)

            elif action == '8':
                print('Выход из программы!')
                break

            else:
                print('Неверный ввод. Попробуйте еще раз.')

    except psycopg2.Error as e:
        print(f'Произошла ошибка: {e}')
    finally:
        if conn:
            conn.close()
            logging.info('Соединение с базой данных закрыто.')


if __name__ == "__main__":
    main()
