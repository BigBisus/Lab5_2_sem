import concurrent.futures
import time
import random


def process_data(item):
    """
    Обрабатывает элемент данных (имитация CPU-bound операции)
    """
    process_time = random.uniform(0.5, 2.0)
    time.sleep(process_time)
    result = item * 2
    print(f"Обработан элемент {item} -> {result} (время: {process_time:.2f}с)")
    return result


def task7_thread_pool():
    """
    Задача: Реализуйте обработку данных с использованием пула потоков.
    """
    data = list(range(1, 11))

    print("=== ОБРАБОТКА ДАННЫХ С ПОМОЩЬЮ ПУЛА ПОТОКОВ ===")

    # Ваш код здесь
    results_by_pool = {}
    times_by_pool = {}

    # Размеры пула для тестирования
    pool_sizes = [2, 4, 8]

    for pool_size in pool_sizes:
        print(f"\n--- Пуллинг с {pool_size} потоками ---")
        start_time = time.time()

        with concurrent.futures.ThreadPoolExecutor(max_workers=pool_size) as executor:
            # Запускаем обработку всех элементов
            results = list(executor.map(process_data, data))

        end_time = time.time()
        execution_time = end_time - start_time

        results_by_pool[pool_size] = results
        times_by_pool[pool_size] = execution_time

        print(f"Время выполнения: {execution_time:.2f} сек")

    # Синхронная обработка для сравнения
    print("\n--- Синхронная обработка ---")
    sync_start = time.time()
    sync_results = [process_data(item) for item in data]
    sync_time = time.time() - sync_start
    print(f"Время выполнения: {sync_time:.2f} сек")

    print("\n=== СРАВНЕНИЕ ПРОИЗВОДИТЕЛЬНОСТИ ===")
    print(f"{'Размер пула':<12} {'Время (сек)':<12} {'Ускорение':<12}")
    print("-" * 36)

    print(f"{'Синхронно':<12} {sync_time:<12.2f} {'1.00x':<12}")

    for pool_size in pool_sizes:
        exec_time = times_by_pool[pool_size]
        speedup = sync_time / exec_time if exec_time > 0 else 0
        print(f"{pool_size} потоков{'':<7} {exec_time:<12.2f} {speedup:<12.2f}x")

    # Анализ
    print("\n=== АНАЛИЗ ===")
    best_pool = min(times_by_pool, key=times_by_pool.get)
    print(f"Наиболее эффективный пул: {best_pool} потоков")
    print(f"Минимальное время: {times_by_pool[best_pool]:.2f} сек")

    # Проверка корректности результатов
    all_same = all(
        results_by_pool[pool_sizes[0]] == results_by_pool[pool_size]
        for pool_size in pool_sizes
    ) and results_by_pool[pool_sizes[0]] == sync_results

    if all_same:
        print("✓ Все результаты корректны и совпадают")
    else:
        print("✗ Результаты различаются!")

    return results_by_pool, times_by_pool, sync_time


# Запуск задачи
if __name__ == "__main__":
    task7_thread_pool()