# Модуль для работы с базой данных SQLite
import sqlite3
from colorama import init, Fore

init(autoreset=True)


class NotesManager:
    def __init__(self, db_file) -> None:
        """
        Инициализирует объект NotesManager для работы с базой данных.

        :param db_file: Имя файла базы данных SQLite.
        """
        self.conn = sqlite3.connect(db_file)  # Устанавливаем соединение с базой данных
        self.cursor = self.conn.cursor()  # Создаем курсор для выполнения SQL-запросов
        self.create_table()  # Создаем таблицу, если она не существует

    def create_table(self) -> None:
        """
        Создает таблицу в базе данных для хранения заметок, если она не существует.
        """
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                content TEXT
            )
        ''')
        self.conn.commit()  # Сохраняем изменения в базе данных

    def add_note(self, title, content) -> None:
        """
        Добавляет новую заметку в базу данных.

        :param title: Заголовок заметки.
        :param content: Содержание заметки.
        """
        self.cursor.execute('INSERT INTO notes (title, content) VALUES (?, ?)', (title, content))
        self.conn.commit()

    def get_all_notes(self) -> list:
        """
        Возвращает список всех заметок в базе данных.

        :return: Список заметок в формате [(id, title), ...]
        """
        self.cursor.execute('SELECT id, title FROM notes')
        return self.cursor.fetchall()

    def get_note_details(self, note_id) -> tuple:
        """
        Возвращает подробную информацию о заметке по её идентификатору.

        :param note_id: Идентификатор заметки.
        :return: Кортеж (title, content) или None, если заметка не найдена.
        """
        self.cursor.execute('SELECT title, content FROM notes WHERE id = ?', (note_id,))
        return self.cursor.fetchone()

    def delete_note(self, note_id) -> None:
        """
        Удаляет заметку из базы данных по её идентификатору.

        :param note_id: Идентификатор заметки.
        """
        self.cursor.execute('DELETE FROM notes WHERE id = ?', (note_id,))
        self.conn.commit()

    def close(self) -> None:
        """
        Закрывает соединение с базой данных.
        """
        self.conn.close()

    def search_notes(self, keyword) -> list:
        """
        Поиск заметок по ключевому слову или фразе.

        :param keyword: Ключевое слово или фраза для поиска.
        :return: Список заметок, содержащих заданное ключевое слово в формате [(id, title), ...].
        """
        self.cursor.execute('SELECT id, title FROM notes WHERE content LIKE ? OR title LIKE ?',
                            (f'%{keyword}%', f'%{keyword}%'))
        return self.cursor.fetchall()


# Модуль для управления заметками
class NotesApp:
    def __init__(self, db_file) -> None:
        """
        Инициализирует объект NotesApp для работы с заметками.

        :param db_file: Имя файла базы данных SQLite.
        """
        self.manager = NotesManager(db_file)  # Создаем объект NotesManager

    def add_note(self, title, content) -> None:
        """
        Добавляет новую заметку.

        :param title: Заголовок заметки.
        :param content: Содержание заметки.
        """
        self.manager.add_note(title, content)

    def get_all_notes(self) -> list:
        """
        Возвращает список всех заметок.

        :return: Список заметок в формате [(id, title), ...]
        """
        return self.manager.get_all_notes()

    def get_note_details(self, note_id) -> tuple:
        """
        Возвращает подробную информацию о заметке по её идентификатору.

        :param note_id: Идентификатор заметки.
        :return: Кортеж (title, content) или None, если заметка не найдена.
        """
        return self.manager.get_note_details(note_id)

    def delete_note(self, note_id) -> None:
        """
        Удаляет заметку по её идентификатору.

        :param note_id: Идентификатор заметки.
        """
        self.manager.delete_note(note_id)

    def close(self) -> None:
        """
        Закрывает приложение и соединение с базой данных.
        """
        self.manager.close()

    def search_notes(self, keyword: str) -> list:
        """
        Выполняет поиск заметок по ключевому слову или фразе.

        :param keyword: Ключевое слово или фраза для поиска.
        :return: Список заметок, содержащих заданное ключевое слово в формате [(id, title), ...].
        """
        return self.manager.search_notes(keyword=keyword)


# Цветной выбор действий
def colored_menu() -> None:
    print(f"{Fore.YELLOW}1. {Fore.RESET}Добавить заметку")
    print(f"{Fore.YELLOW}2. {Fore.RESET}Просмотреть список заметок")
    print(f"{Fore.YELLOW}3. {Fore.RESET}Просмотреть подробности заметки")
    print(f"{Fore.YELLOW}4. {Fore.RESET}Удалить заметку")
    print(f"{Fore.YELLOW}5. {Fore.RESET}Поиск заметки по ключевому слову или фразе")
    print(f"{Fore.YELLOW}6. {Fore.RESET}Выйти")


# Консольное приложение для взаимодействия с заметками
def main():
    app = NotesApp("notes.db")  # Инициализируем приложение с указанным файлом базы данных

    while True:
        colored_menu()  # Выводим цветное меню с доступными действиями
        choice = input("Выберите действие: ")

        if choice == "1":
            title = input("Введите заголовок: ")
            content = input("Введите содержание: ")
            app.add_note(title, content)
            print(f"{Fore.GREEN}Заметка добавлена.")
        elif choice == "2":
            all_notes = app.get_all_notes()
            print(f'{Fore.RED}{"➖" * 20}')
            if all_notes == []:
                print(f'{Fore.RED}Ваш список заметок пуст!')
            else:
                print(f"{Fore.GREEN}Список всех заметок:")
            for note in all_notes:
                print(f"{Fore.CYAN}{note[0]}. {note[1]}{Fore.RESET}")
            print(f'{Fore.RED}{"➖" * 20}')
        elif choice == "3":
            note_id = input("Введите идентификатор заметки: ")
            note_details = app.get_note_details(note_id)
            print(f'{Fore.RED}{"➖" * 20}')
            if note_details:
                print(f"{Fore.GREEN}Заголовок: {note_details[0]}")
                print(f"{Fore.GREEN}Содержание: {note_details[1]}")
            else:
                print(f"{Fore.RED}Заметка не найдена.")
            print(f'{Fore.RED}{"➖" * 20}')
        elif choice == "4":
            note_id = input("Введите идентификатор заметки для удаления: ")
            app.delete_note(note_id)
            print(f"{Fore.RED}Заметка удалена.")
        elif choice == "6":
            app.close()
            break
        elif choice == "5":
            keyword = input("Введите ключевое слово или фразу для поиска: ")
            matching_notes = app.search_notes(keyword)
            print(f'{Fore.RED}{"➖" * 20}')
            if matching_notes:
                print(f"{Fore.CYAN}Список заметок, содержащих '{keyword}':{Fore.RESET}")
                for note in matching_notes:
                    print(f"{Fore.CYAN}{note[0]}. {note[1]}{Fore.RESET}")
            else:
                print(f"{Fore.RED}Заметки не найдены.")
            print(f'{Fore.RED}{"➖" * 20}')
        else:
            print(f"{Fore.RED}Некорректный выбор. Пожалуйста, выберите действие из списка.")


if __name__ == "__main__":
    main()
