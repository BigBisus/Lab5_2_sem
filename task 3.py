import multiprocessing
import time
import math
import sys


def calculate_factorial(n):
    """
    Вычисляет факториал числа (CPU-intensive операция)
    """
    print(f"Начало вычисления факториала {n}!")
    result = math.factorial(n)
    # Изменяем вывод - не пытаемся печатать весь результат
    print(f"Завершено вычисление факториала {n}!")
    return result


def calculate_prime(n):
    """
    Проверяет, является ли число простым
    """
    print(f"Начало проверки числа {n} на простоту")

    if n < 2:
        result = False
    else:
        result = all(n % i != 0 for i in range(2, int(math.sqrt(n)) + 1))

    print(f"Число {n} простое: {result}")
    return result


def task3_multiprocess_calculations():
    """
    Задача: Реализуйте многопроцессные вычисления.
    Вычисления:
    1. Факториал 100000
    2. Факториал 80000
    3. Проверка числа 10000000019 на простоту
    4. Проверка числа 10000000033 на простоту

    Требуется:
    - Выполнить вычисления в отдельных процессах
    - Сравнить время с последовательным выполнением
    - Собрать и вывести результаты
    """
    # Увеличиваем лимит для преобразования больших целых чисел в строки
    sys.set_int_max_str_digits(1000000)  # Устанавливаем достаточно высокий лимит

    calculations = [
        (calculate_factorial, 10000),  # Уменьшено для демонстрации
        (calculate_factorial, 8000),
        (calculate_prime, 10000019),
        (calculate_prime, 10000033)
    ]

    # Многопроцессное выполнение
    print("=== МНОГОПРОЦЕССНОЕ ВЫПОЛНЕНИЕ ===")
    start_time = time.time()

    processes = []
    results = []

    # Ваш код здесь
    # TODO: Создайте и запустите процессы
    # TODO: Соберите результаты

    # Создаем пул процессов
    pool = multiprocessing.Pool(processes=4)

    # Запускаем вычисления в отдельных процессах
    async_results = []
    for func, arg in calculations:
        async_result = pool.apply_async(func, (arg,))
        async_results.append(async_result)

    # Закрываем пул и ждем завершения всех процессов
    pool.close()
    pool.join()

    # Собираем результаты
    for async_result in async_results:
        results.append(async_result.get())

    end_time = time.time()
    multiprocess_time = end_time - start_time

    # Синхронное выполнение для сравнения
    print("\n=== СИНХРОННОЕ ВЫПОЛНЕНИЕ ===")
    start_time = time.time()

    sync_results = []
    for func, arg in calculations:
        sync_results.append(func(arg))

    end_time = time.time()
    sync_time = end_time - start_time

    print(f"\nСравнение времени:")
    print(f"Многопроцессное: {multiprocess_time:.2f} сек")
    print(f"Синхронное: {sync_time:.2f} сек")
    if multiprocess_time > 0:
        print(f"Ускорение: {sync_time / multiprocess_time:.2f}x")
    else:
        print("Ускорение: невозможно вычислить (нулевое время выполнения)")

    # Выводим результаты факториалов без полного преобразования в строку
    print("\nРезультаты вычислений:")
    for i, (func, arg) in enumerate(calculations):
        if func == calculate_factorial:
            # Для факториалов показываем только длину числа
            result = results[i]
            print(f"Факториал {arg}! имеет {len(str(result))} цифр")
        else:
            print(f"Число {arg} простое: {results[i]}")

    # Проверка, что результаты одинаковые
    print("\nПроверка результатов:")
    for i, (multiprocess_result, sync_result) in enumerate(zip(results, sync_results)):
        if isinstance(multiprocess_result, bool):
            # Для булевых значений
            match = multiprocess_result == sync_result
        else:
            # Для больших чисел сравниваем напрямую
            match = multiprocess_result == sync_result
        print(f"Задача {i + 1}: {'Совпадают' if match else 'Не совпадают'}")


# Запуск задачи
if __name__ == "__main__":
    task3_multiprocess_calculations()