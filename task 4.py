import asyncio
import aiohttp
import time


async def fetch_url(session, url, name):
    """
    Асинхронно загружает веб-страницу
    """
    print(f"Начало загрузки {name}")

    try:
        async with session.get(url) as response:
            content = await response.text()
            print(f"Завершена загрузка {name}, статус: {response.status}")
            return len(content)
    except Exception as e:
        print(f"Ошибка при загрузке {name}: {e}")
        return 0


async def task4_async_scraper():
    """
    Задача: Создайте асинхронный веб-скрапер.

    URL для сканирования:
    1. "https://httpbin.org/delay/1" - "Сайт 1"
    2. "https://httpbin.org/delay/2" - "Сайт 2"
    3. "https://httpbin.org/delay/1" - "Сайт 3"
    4. "https://httpbin.org/delay/3" - "Сайт 4"

    Требования:
    - Реализовать асинхронную загрузку всех URL
    - Использовать aiohttp для HTTP запросов
    - Измерить общее время выполнения
    - Вывести размер загруженного контента для каждого сайта
    """
    urls = [
        ("https://httpbin.org/delay/1", "Сайт 1"),
        ("https://httpbin.org/delay/2", "Сайт 2"),
        ("https://httpbin.org/delay/1", "Сайт 3"),
        ("https://httpbin.org/delay/3", "Сайт 4")
    ]

    print("=== НАЧАЛО АСИНХРОННОЙ ЗАГРУЗКИ ===")
    start_time = time.time()

    # Ваш код здесь
    # TODO: Создайте ClientSession
    # TODO: Создайте задачи для каждого URL
    # TODO: Используйте asyncio.gather для параллельного выполнения

    # Создаем ClientSession с таймаутом
    timeout = aiohttp.ClientTimeout(total=30)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        # Создаем задачи для каждого URL
        tasks = []
        for url, name in urls:
            task = fetch_url(session, url, name)
            tasks.append(task)

        # Запускаем все задачи параллельно и собираем результаты
        results = await asyncio.gather(*tasks)

    end_time = time.time()
    total_time = end_time - start_time

    print(f"\nОбщее время выполнения: {total_time:.2f} секунд")

    # Выводим детальную информацию о каждом сайте
    print("\n" + "=" * 50)
    print("РЕЗУЛЬТАТЫ ЗАГРУЗКИ:")
    print("=" * 50)

    total_size = 0
    for i, ((url, name), size) in enumerate(zip(urls, results), 1):
        total_size += size
        print(f"{i}. {name}:")
        print(f"   URL: {url}")
        print(f"   Размер контента: {size} символов")

    print(f"\nОбщий размер всех загруженных данных: {total_size} символов")

    # Теоретическое время синхронной загрузки
    print("\n" + "=" * 50)
    print("АНАЛИЗ ПРОИЗВОДИТЕЛЬНОСТИ:")
    print("=" * 50)

    # Вычисляем теоретическое время синхронной загрузки
    # (сумма всех задержек из URL)
    delays = []
    for url, _ in urls:
        try:
            # Извлекаем число из URL типа "https://httpbin.org/delay/2"
            delay_str = url.split('/')[-1]
            delay = float(delay_str)
            delays.append(delay)
        except (ValueError, IndexError):
            delays.append(0)  # Если не удалось извлечь задержку

    theoretical_sync_time = sum(delays)
    actual_async_time = total_time
    speedup = theoretical_sync_time / actual_async_time if actual_async_time > 0 else 0

    print(f"Теоретическое время синхронной загрузки: {theoretical_sync_time:.1f} сек")
    print(f"Фактическое время асинхронной загрузки: {actual_async_time:.2f} сек")

    if speedup > 0:
        print(f"Ускорение: {speedup:.2f}x")
        if speedup > 1:
            print("Асинхронная загрузка эффективнее синхронной!")
        else:
            print("Синхронная загрузка была бы эффективнее (возможно из-за накладных расходов)")

    return results


# Запуск задачи
async def main():
    """
    Основная асинхронная функция для запуска скрапера
    """
    try:
        results = await task4_async_scraper()
        print(f"\nИтоговые результаты: {results}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


# Запуск основной асинхронной функции
if __name__ == "__main__":
    asyncio.run(main())