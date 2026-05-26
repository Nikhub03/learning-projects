"""
Функциональный калькулятор.
Поддерживает базовые арифметические операции и элементарные функции.
Легко расширяется добавлением новых функций в словарь FUNCTIONS.
"""

import math

# Словарь доступных функций: имя -> (функция, количество аргументов, описание)
FUNCTIONS = {
    # Арифметика
    '+':    (lambda a, b: a + b, 2, 'Сложение'),
    '-':    (lambda a, b: a - b, 2, 'Вычитание'),
    '*':    (lambda a, b: a * b, 2, 'Умножение'),
    '/':    (lambda a, b: a / b, 2, 'Деление'),
    '^':    (lambda a, b: a ** b, 2, 'Возведение в степень'),
    # Унарные элементарные функции
    'sqrt': (math.sqrt, 1, 'Квадратный корень'),
    'sin':  (math.sin, 1, 'Синус (в радианах)'),
    'cos':  (math.cos, 1, 'Косинус (в радианах)'),
    'tan':  (math.tan, 1, 'Тангенс (в радианах)'),
    'log':  (math.log, 1, 'Натуральный логарифм'),
    'log10':(math.log10,1, 'Десятичный логарифм'),
    'exp':  (math.exp, 1, 'Экспонента'),
    'abs':  (abs, 1, 'Модуль числа'),
    'floor':(math.floor,1, 'Округление вниз'),
    'ceil': (math.ceil, 1, 'Округление вверх'),
}

def add_function(name, func, arity, description=""):
    """Добавляет новую функцию в калькулятор."""
    FUNCTIONS[name] = (func, arity, description)

def show_help():
    """Выводит список доступных функций."""
    print("\nДоступные функции:")
    for name, (_, arity, desc) in FUNCTIONS.items():
        print(f"  {name:<8} (аргументов: {arity}) - {desc}")
    print("\nФормат ввода: <имя_функции> <аргументы через пробел>")
    print("Примеры: + 3 5, sqrt 9, sin 1.5708, ^ 2 10")
    print("Для выхода введите 'exit' или 'quit'.")
    print("Для просмотра справки введите 'help'.\n")

def evaluate(name, args):
    """Вычисляет функцию по имени и списку строковых аргументов."""
    if name not in FUNCTIONS:
        raise ValueError(f"Неизвестная функция: {name}")
    func, arity, _ = FUNCTIONS[name]
    if len(args) != arity:
        raise ValueError(f"Функция {name} требует {arity} аргументов, получено {len(args)}")
    try:
        numeric_args = [float(x) for x in args]
    except ValueError:
        raise ValueError("Все аргументы должны быть числами")
    return func(*numeric_args)

def main():
    print("=== Функциональный калькулятор ===")
    show_help()
    while True:
        user_input = input(">>> ").strip()
        if not user_input:
            continue
        if user_input.lower() in ('exit', 'quit'):
            print("До свидания!")
            break
        if user_input.lower() == 'help':
            show_help()
            continue

        parts = user_input.split()
        func_name = parts[0]
        args = parts[1:]
        try:
            result = evaluate(func_name, args)
            print(f"Результат: {result}\n")
        except Exception as e:
            print(f"Ошибка: {e}\n")

if __name__ == "__main__":
    # Пример добавления пользовательской функции (расширяемость)
    # add_function("cube", lambda x: x**3, 1, "Куб числа")
    main()