import sqlite3

connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
city TEXT
)
''')

where_id = 'SELECT * FROM Users WHERE id = ?'
where_username = 'SELECT * FROM Users WHERE username = ?'


def add_user():
    username = input('Введите username >>> ')

    cursor.execute(where_username, (username.lower(),))
    existing_user = cursor.fetchone()

    if existing_user:
        print(f'{username} уже существует.\n')
        return

    mail = input('Введите почту пользователя >>> ')
    age = input('Введите возраст пользователя >>> ')
    city = input('Введите город пользователя >>> ')
    cursor.execute('INSERT into Users (username, email, age, city) VALUES (?, ?, ?, ?)',
                   (username.lower(), mail.lower(), age.lower(), city.lower()))
    print('Пользователь добавлен.\n')

    connection.commit()


def del_user():
    id_ = input('Введите id >>> ')

    cursor.execute(where_id, (id_,))
    existing_user = cursor.fetchone()

    if not existing_user:
        print(f'User {id_} не найден.\n')
        return

    cursor.execute('DELETE FROM Users WHERE id = ?', (id_,))
    print(f'User {id_} удалён.\n')

    connection.commit()


def upd_user():
    id_ = input('Введите id >>> ')

    cursor.execute(where_id, (id_,))
    existing_user = cursor.fetchone()

    if not existing_user:
        print(f'User {id_} не найден.\n')
        return

    while True:
        mode_ = input(
            'Выберите действие: \n1 - Обновить username \n2 - Обновить mail \n3 - Обновить age \n4 - Обновить city '
            '\nq - Выход \n>>> ')

        match mode_:
            case '1':
                new_username = input('Введите новый username >>> ')
                cursor.execute('UPDATE Users SET username = ? WHERE id = ?', (new_username.lower(), id_,))
                print(f'User {id_} обновлён.\n')
            case '2':
                new_mail = input('Введите новый mail >>> ')
                cursor.execute('UPDATE Users SET email = ? WHERE id = ?', (new_mail.lower(), id_,))
                print(f'User {id_} обновлён.\n')
            case '3':
                new_age = input('Введите новый age >>> ')
                cursor.execute('UPDATE Users SET age = ? WHERE id = ?', (new_age.lower(), id_,))
                print(f'User {id_} обновлён.\n')
            case '4':
                new_city = input('Введите новый city >>> ')
                cursor.execute('UPDATE Users SET city = ? WHERE id = ?', (new_city.lower(), id_,))
                print(f'User {id_} обновлён.\n')
            case 'q':
                break

    connection.commit()


def view_all_users():
    cursor.execute('SELECT * FROM Users')
    all_users = cursor.fetchall()

    if not all_users:
        print('База данных пуста.\n')
        return

    column_widths = []
    for row in zip(*all_users):
        max_width = 0
        for value in row:
            max_width = max(max_width, len(str(value)))
        column_widths.append(max_width)

    for i in range(len(column_widths)):
        column_widths[i] += 4

    header = ['ID', 'Username', 'Email', 'Age', 'City']
    header_format = ''
    for width in column_widths:
        header_format += f'{{:<{width}}}'
    print(header_format.format(*header))

    separator_line = '-' * sum(column_widths)
    print(separator_line)

    for user in all_users:
        user_format = ''
        for width in column_widths:
            user_format += f'{{:<{width}}}'
        print(user_format.format(*user))

    print()
    connection.commit()


def find_user():
    username = input('Введите username >>> ')

    cursor.execute("SELECT * FROM Users WHERE LOWER(Username) = ?", (username.lower(),))
    existing_user = cursor.fetchone()

    if not existing_user:
        print(f'Пользователь {username} не найден.\n')
        return

    column_widths = []
    for value in existing_user:
        max_width = len(str(value))
        column_widths.append(max_width)

    for i in range(len(column_widths)):
        column_widths[i] += 4

    header = ['\nID', 'Username', 'Email', 'Age', 'City']
    header_format = ''
    for width in column_widths:
        header_format += f'{{:<{width}}}'
    print(header_format.format(*header))

    separator_line = '-' * sum(column_widths)
    print(separator_line)

    user_format = ''
    for width in column_widths:
        user_format += f'{{:<{width}}}'
    print(user_format.format(*existing_user))

    print()
    connection.commit()


while True:
    mode = input(
        'Выберите действие: \n1 - Добавить user \n2 - Удалить user \n3 - Обновить user \n4 - Просмотр всех '
        'пользователей \n5 - Найти user \nq - Выход \n>>> ')

    match mode:
        case '1':
            add_user()
        case '2':
            del_user()
        case '3':
            upd_user()
        case '4':
            view_all_users()
        case '5':
            find_user()
        case 'q':
            break

connection.close()
