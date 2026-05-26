"""
Задание 2. Классы CFile и CMyDataFile.
Демонстрация инкапсуляции, наследования, работы с файлами и меню.
"""

import os
import pickle
import json

# ==================== Базовый класс CFile ====================
class CFile:
    """Инкапсулирует открытие, чтение и сохранение файла."""
    
    def __init__(self, filename):
        self._filename = filename   # защищённый атрибут
        self._data = None           # данные, считанные из файла
    
    def open(self):
        """Открывает файл (загружает данные)."""
        try:
            with open(self._filename, 'rb') as f:
                self._data = pickle.load(f)
            print(f"Файл '{self._filename}' успешно открыт (загружен).")
        except FileNotFoundError:
            print(f"Файл '{self._filename}' не найден. Будет создан новый при сохранении.")
            self._data = None
        except Exception as e:
            print(f"Ошибка при открытии: {e}")
    
    def save(self):
        """Сохраняет текущие данные в файл."""
        if self._data is None:
            print("Нет данных для сохранения. Сначала загрузите или создайте данные.")
            return
        try:
            with open(self._filename, 'wb') as f:
                pickle.dump(self._data, f)
            print(f"Данные успешно сохранены в '{self._filename}'.")
        except Exception as e:
            print(f"Ошибка при сохранении: {e}")
    
    def read(self):
        """Возвращает содержимое файла (данные)."""
        if self._data is None:
            print("Данные не загружены. Вызовите open() или создайте данные.")
            return None
        return self._data
    
    def set_data(self, data):
        """Устанавливает данные (например, перед сохранением)."""
        self._data = data
    
    # Для демонстрации инкапсуляции
    @property
    def filename(self):
        return self._filename


# ==================== Тип данных MyData ====================
class MyData:
    """Произвольный тип данных, который будет храниться в файле."""
    def __init__(self, name, value, tags=None):
        self.name = name
        self.value = value
        self.tags = tags if tags is not None else []
    
    def __repr__(self):
        return f"MyData(name='{self.name}', value={self.value}, tags={self.tags})"


# ==================== Производный класс CMyDataFile ====================
class CMyDataFile(CFile):
    """Файл, содержащий данные типа MyData + заголовок для быстрого доступа."""
    
    def __init__(self, filename, header=None):
        super().__init__(filename)
        self._header = header if header is not None else {}
        # Дополнительный индекс для быстрого доступа (например, по имени)
        self._index = None
    
    def open(self):
        """Открывает файл и восстанавливает данные + заголовок."""
        try:
            with open(self._filename, 'rb') as f:
                container = pickle.load(f)
                # Ожидаем словарь с ключами 'header', 'data'
                if isinstance(container, dict) and 'header' in container and 'data' in container:
                    self._header = container['header']
                    self._data = container['data']
                else:
                    # Попытка прочитать старый формат (только данные)
                    self._data = container
                    print("Предупреждение: файл не содержит заголовка. Используется пустой заголовок.")
            self._build_index()
            print(f"Файл '{self._filename}' открыт (заголовок: {self._header})")
        except FileNotFoundError:
            print(f"Файл '{self._filename}' не найден. Будет создан новый.")
            self._data = []
            self._header = {}
        except Exception as e:
            print(f"Ошибка при открытии: {e}")
    
    def save(self):
        """Сохраняет данные вместе с заголовком."""
        if self._data is None:
            print("Нет данных для сохранения.")
            return
        container = {
            'header': self._header,
            'data': self._data
        }
        try:
            with open(self._filename, 'wb') as f:
                pickle.dump(container, f)
            print(f"Данные и заголовок сохранены в '{self._filename}'.")
        except Exception as e:
            print(f"Ошибка при сохранении: {e}")
    
    def _build_index(self):
        """Создаёт индекс для быстрого доступа по имени записи MyData."""
        if isinstance(self._data, list):
            self._index = {item.name: idx for idx, item in enumerate(self._data) if isinstance(item, MyData)}
        else:
            self._index = None
    
    def add_record(self, mydata_obj):
        """Добавляет запись MyData в конец списка данных."""
        if self._data is None:
            self._data = []
        if not isinstance(mydata_obj, MyData):
            raise TypeError("Можно добавлять только объекты MyData")
        self._data.append(mydata_obj)
        self._build_index()
        print(f"Запись '{mydata_obj.name}' добавлена.")
    
    def get_by_name(self, name):
        """Быстрый доступ к записи по имени (использует индекс)."""
        if not self._index or name not in self._index:
            print(f"Запись с именем '{name}' не найдена.")
            return None
        idx = self._index[name]
        return self._data[idx]
    
    def update_header(self, key, value):
        """Обновляет заголовок."""
        self._header[key] = value
        print(f"Заголовок обновлён: {key} = {value}")
    
    def get_header(self):
        """Возвращает заголовок."""
        return self._header
    
    def get_all_records(self):
        """Возвращает все записи MyData."""
        if not isinstance(self._data, list):
            return []
        return [item for item in self._data if isinstance(item, MyData)]


# ==================== Демонстрационная программа с меню ====================
def main():
    print("=== Программа демонстрации классов CFile и CMyDataFile ===")
    filename = "mydata.dat"
    
    # Создаём экземпляр производного класса
    mydata_file = CMyDataFile(filename, header={"version": "1.0", "author": "Student"})
    
    while True:
        print("\n--- Меню ---")
        print("1. Открыть файл (open)")
        print("2. Показать заголовок и все записи")
        print("3. Добавить новую запись (MyData)")
        print("4. Найти запись по имени")
        print("5. Обновить заголовок")
        print("6. Сохранить файл (save)")
        print("7. Проверить базовый класс CFile на отдельном файле (демо инкапсуляции)")
        print("0. Выход")
        
        choice = input("Ваш выбор: ").strip()
        
        if choice == "1":
            mydata_file.open()
        elif choice == "2":
            header = mydata_file.get_header()
            print(f"\nЗаголовок: {header}")
            records = mydata_file.get_all_records()
            if records:
                print("Записи (MyData):")
                for rec in records:
                    print(f"  {rec}")
            else:
                print("Нет записей.")
        elif choice == "3":
            name = input("Введите имя (name): ")
            try:
                value = float(input("Введите числовое значение (value): "))
            except ValueError:
                print("Ошибка: значение должно быть числом.")
                continue
            tags_str = input("Введите теги через запятую (например, tag1,tag2): ")
            tags = [t.strip() for t in tags_str.split(",") if t.strip()]
            new_record = MyData(name, value, tags)
            mydata_file.add_record(new_record)
        elif choice == "4":
            name = input("Введите имя для поиска: ")
            record = mydata_file.get_by_name(name)
            if record:
                print(f"Найдено: {record}")
        elif choice == "5":
            key = input("Ключ заголовка: ")
            value = input("Значение: ")
            mydata_file.update_header(key, value)
        elif choice == "6":
            mydata_file.save()
        elif choice == "7":
            # Демонстрация работы базового класса на отдельном файле
            demo_base_class()
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Неверный выбор. Повторите.")

def demo_base_class():
    """Показывает, как работает базовый класс CFile с произвольными данными."""
    print("\n--- Демонстрация CFile (базовый класс) ---")
    f = CFile("base_demo.dat")
    print("Создаём и сохраняем простые данные (словарь)")
    test_data = {"name": "Тест", "values": [1,2,3]}
    f.set_data(test_data)
    f.save()
    print("Открываем и читаем...")
    f.open()
    loaded = f.read()
    print(f"Прочитано: {loaded}")
    print("Работа с CFile завершена.\n")


if __name__ == "__main__":
    main()