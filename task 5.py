import time
import threading
import multiprocessing
import asyncio
import concurrent.futures


def io_task(name, duration):
    """I/O-bound задача (имитация)"""
    time.sleep(duration)
    return f"{name} completed in {duration} seconds"


async def async_io_task(name, duration):
    """Асинхронная I/O-bound задача"""
    await asyncio.sleep(duration)
    return f"{name} completed in {duration} seconds"


def task5_performance_comparison():
    """
    Задача: Сравните производительность разных подходов.

    Набор I/O-bound задач (имитация):
    1. "Task1" - 2 секунды
    2. "Task2" - 3 секунды
    3. "Task3" - 1 секунда
    4. "Task4" - 2 секунды
    5. "Task5" - 1 секунда

    Требуется:
    - Реализовать выполнение одним потоком
    - Реализовать выполнение несколькими потоками
    - Реализовать выполнение несколькими процессами
    - Реализовать асинхронное выполнение
    - Сравнить время выполнения каждого подхода
    - Сделать выводы о эффективности
    """
    tasks = [("Task1", 2), ("Task2", 3), ("Task3", 1), ("Task4", 2), ("Task5", 1)]

    # Ваш код здесь
    # TODO: Реализуйте все 4 подхода
    # TODO: Измерьте время для каждого
    # TODO: Проанализируйте результаты

    print("=" * 60)
    print("СРАВНЕНИЕ ПРОИЗВОДИТЕЛЬНОСТИ ДЛЯ I/O-BOUND ЗАДАЧ")
    print("=" * 60)

    # 1. Синхронное выполнение (один поток)
    print("\n=== 1. СИНХРОННОЕ ВЫПОЛНЕНИЕ ===")
    start_time = time.time()

    sync_results = []
    for name, duration in tasks:
        print(f"Начало {name} (длительность: {duration} сек)")
        result = io_task(name, duration)
        sync_results.append(result)
        print(f"Завершено: {result}")

    sync_time = time.time() - start_time
    print(f"Общее время синхронного выполнения: {sync_time:.2f} сек")

    # 2. Многопоточное выполнение
    print("\n=== 2. МНОГОПОТОЧНОЕ ВЫПОЛНЕНИЕ ===")
    start_time = time.time()

    thread_results = []
    threads = []
    results_lock = threading.Lock()

    # Функция-обертка для потока
    def thread_worker(name, duration):
        result = io_task(name, duration)
        with results_lock:
            thread_results.append(result)
        print(f"Завершен поток для {name}: {result}")

    # Создаем и запускаем потоки
    for name, duration in tasks:
        print(f"Создание потока для {name} (длительность: {duration} сек)")
        thread = threading.Thread(target=thread_worker, args=(name, duration))
        threads.append(thread)
        thread.start()

    # Ждем завершения всех потоков
    for thread in threads:
        thread.join()

    thread_time = time.time() - start_time
    print(f"Общее время многопоточного выполнения: {thread_time:.2f} сек")

    # 3. Многопроцессное выполнение
    print("\n=== 3. МНОГОПРОЦЕССНОЕ ВЫПОЛНЕНИЕ ===")
    start_time = time.time()

    # Используем ProcessPoolExecutor для удобства
    with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
        print("Создание процессов...")
        # Подготавливаем задачи для процессов
        future_to_task = {
            executor.submit(io_task, name, duration): (name, duration)
            for name, duration in tasks
        }

        process_results = []
        for future in concurrent.futures.as_completed(future_to_task):
            name, duration = future_to_task[future]
            try:
                result = future.result()
                process_results.append(result)
                print(f"Завершен процесс для {name}: {result}")
            except Exception as e:
                print(f"Ошибка в процессе для {name}: {e}")

    process_time = time.time() - start_time
    print(f"Общее время многопроцессного выполнения: {process_time:.2f} сек")

    # 4. Асинхронное выполнение
    print("\n=== 4. АСИНХРОННОЕ ВЫПОЛНЕНИЕ ===")

    async def run_async_tasks():
        print("Запуск асинхронных задач...")
        async_tasks = []
        for name, duration in tasks:
            print(f"Создание асинхронной задачи для {name} (длительность: {duration} сек)")
            task = async_io_task(name, duration)
            async_tasks.append(task)

        return await asyncio.gather(*async_tasks)

    start_time = time.time()
    # Запускаем асинхронные задачи
    async_results = asyncio.run(run_async_tasks())
    async_time = time.time() - start_time

    print(f"Общее время асинхронного выполнения: {async_time:.2f} сек")

    print("\n" + "=" * 60)
    print("=== АНАЛИЗ РЕЗУЛЬТАТОВ ===")
    print("=" * 60)

    # Выводим сводную таблицу
    print(f"\n{'Подход':<20} {'Время (сек)':<15} {'Ускорение':<15}")
    print("-" * 50)

    approaches = [
        ("Синхронное", sync_time),
        ("Многопоточное", thread_time),
        ("Многопроцессное", process_time),
        ("Асинхронное", async_time)
    ]

    for approach_name, approach_time in approaches:
        if sync_time > 0:
            speedup = sync_time / approach_time
        else:
            speedup = 0

        print(f"{approach_name:<20} {approach_time:<15.2f} {speedup:<15.2f}x")

    # Анализ эффективности
    print("\n" + "=" * 60)
    print("ВЫВОДЫ:")
    print("=" * 60)

    # Определяем самый быстрый подход
    fastest_approach = min(approaches, key=lambda x: x[1])
    slowest_approach = max(approaches, key=lambda x: x[1])

    print(f"\n1. Самый быстрый подход: {fastest_approach[0]} ({fastest_approach[1]:.2f} сек)")
    print(f"   Самый медленный подход: {slowest_approach[0]} ({slowest_approach[1]:.2f} сек)")

    print("\n2. Анализ производительности для I/O-bound задач:")
    print("   - Синхронное выполнение: выполняет задачи последовательно,")
    print("     общее время = сумма длительностей всех задач")

    total_duration = sum(duration for _, duration in tasks)
    print(f"     Теоретическое время: {total_duration} сек")
    print(f"     Фактическое время: {sync_time:.2f} сек")

    print("\n   - Многопоточное выполнение: эффективно для I/O-bound задач,")
    print("     позволяет выполнять несколько операций ввода-вывода параллельно")

    print("\n   - Многопроцессное выполнение: обычно менее эффективно для")
    print("     чистых I/O-bound задач из-за накладных расходов на создание")
    print("     процессов и межпроцессное взаимодействие")

    print("\n   - Асинхронное выполнение: оптимально для I/O-bound задач,")
    print("     переключается между задачами без блокировки потока")

    print("\n3. Рекомендации:")
    print("   - Для CPU-bound задач (вычисления): используйте процессы")
    print("   - Для I/O-bound задач (сеть, файлы): используйте потоки или async/await")
    print("   - Для смешанных задач: комбинируйте подходы")

    print("\n4. Теоретический минимум времени:")
    max_duration = max(duration for _, duration in tasks)
    print(f"   Минимальное возможное время (при идеальном параллелизме): {max_duration:.1f} сек")
    print(f"   (определяется самой длительной задачей)")

    # Сравнение с теоретическим минимумом
    for approach_name, approach_time in approaches:
        if max_duration > 0:
            efficiency = (max_duration / approach_time) * 100
            print(f"   Эффективность {approach_name}: {efficiency:.1f}% от теоретического минимума")

    return {
        "sync_time": sync_time,
        "thread_time": thread_time,
        "process_time": process_time,
        "async_time": async_time,
        "sync_results": sync_results,
        "thread_results": thread_results,
        "process_results": process_results,
        "async_results": async_results
    }


# Запуск задачи
if __name__ == "__main__":
    results = task5_performance_comparison()