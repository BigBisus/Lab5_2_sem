import asyncio
import time
from datetime import datetime
from typing import List, Tuple


async def scheduled_task(name, priority, duration):
    """
    Задача с приоритетом и временем выполнения

    Параметры:
    name (str): название задачи
    priority (int): приоритет (1 - высший)
    duration (float): время выполнения
    """
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Задача '{name}' (приоритет {priority}) начата")
    await asyncio.sleep(duration)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Задача '{name}' завершена")
    return f"Результат {name}"


async def task6_async_scheduler():
    """
    Задача: Создайте асинхронный планировщик задач.

    Задачи:
    1. "Экстренная задача" - приоритет 1, длительность 1 сек
    2. "Важная задача" - приоритет 2, длительность 2 сек
    3. "Обычная задача A" - приоритет 3, длительность 3 сек
    4. "Обычная задача B" - приоритет 3, длительность 2 сек
    5. "Фоновая задача" - приоритет 4, длительность 5 сек

    Требуется:
    - Запустить задачи в порядке приоритета
    - Обеспечить выполнение высокоприоритетных задач первыми
    - Реализовать ограничение на одновременное выполнение (не более 2 задач)
    - Вывести порядок завершения задач
    """
    tasks_with_priority = [
        ("Экстренная задача", 1, 1),
        ("Важная задача", 2, 2),
        ("Обычная задача A", 3, 3),
        ("Обычная задача B", 3, 2),
        ("Фоновая задача", 4, 5)
    ]

    # Ваш код здесь
    # TODO: Отсортируйте задачи по приоритету
    # TODO: Реализуйте семафор для ограничения одновременного выполнения
    # TODO: Запустите задачи и соберите результаты

    print("=" * 60)
    print("АСИНХРОННЫЙ ПЛАНИРОВЩИК ЗАДАЧ С ПРИОРИТЕТАМИ")
    print("=" * 60)
    print(f"Начало работы: {datetime.now().strftime('%H:%M:%S')}")
    print(f"Всего задач: {len(tasks_with_priority)}")
    print("Ограничение: не более 2 задач одновременно")
    print()

    start_time = time.time()

    # Сортировка задач по приоритету (1 - высший)
    sorted_tasks = sorted(tasks_with_priority, key=lambda x: x[1])
    print("Порядок выполнения задач по приоритету:")
    for i, (name, priority, duration) in enumerate(sorted_tasks, 1):
        print(f"{i}. {name} (приоритет {priority}, длительность {duration} сек)")
    print()

    # Создаем семафор для ограничения одновременного выполнения
    semaphore = asyncio.Semaphore(2)
    results = []
    completion_order = []

    # Асинхронная функция для выполнения одной задачи
    async def execute_task(name, priority, duration):
        async with semaphore:  # Ограничиваем одновременное выполнение
            result = await scheduled_task(name, priority, duration)
            completion_order.append(name)
            return result

    # Создаем задачи
    tasks = []
    for name, priority, duration in sorted_tasks:
        task = execute_task(name, priority, duration)
        tasks.append(task)

    # Запускаем все задачи и собираем результаты
    results = await asyncio.gather(*tasks)

    end_time = time.time()
    total_time = end_time - start_time

    print()
    print("=" * 60)
    print("РЕЗУЛЬТАТЫ ВЫПОЛНЕНИЯ:")
    print("=" * 60)

    print("\nПорядок завершения задач:")
    for i, task_name in enumerate(completion_order, 1):
        print(f"{i}. {task_name}")

    print("\nОбщее время выполнения всех задач: {:.2f} секунд".format(total_time))
    print("\nТеоретическое время при последовательном выполнении: {} секунд".format(
        sum(duration for _, _, duration in tasks_with_priority)
    ))

    # Анализ эффективности
    print("\n" + "=" * 60)
    print("АНАЛИЗ ЭФФЕКТИВНОСТИ:")
    print("=" * 60)

    # Группируем задачи по приоритетам
    tasks_by_priority = {}
    for name, priority, duration in tasks_with_priority:
        if priority not in tasks_by_priority:
            tasks_by_priority[priority] = []
        tasks_by_priority[priority].append((name, duration))

    print("\nГруппировка задач по приоритетам:")
    for priority in sorted(tasks_by_priority.keys()):
        tasks_list = tasks_by_priority[priority]
        print(f"Приоритет {priority}:")
        for name, duration in tasks_list:
            print(f"  - {name} ({duration} сек)")

    print("\nВыводы:")
    print("1. Задачи с высшим приоритетом выполняются первыми")
    print("2. Ограничение в 2 одновременные задачи:")
    print("   - Позволяет контролировать нагрузку")
    print("   - Предотвращает перегрузку системы")
    print("3. Асинхронное выполнение позволяет:")
    print("   - Эффективно использовать время ожидания")
    print("   - Выполнять задачи параллельно в рамках ограничений")

    print("\nВсе задачи завершены!")
    return results


# Запуск задачи
async def main():
    try:
        results = await task6_async_scheduler()
        print(f"\nРезультаты выполнения: {results}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    asyncio.run(main())