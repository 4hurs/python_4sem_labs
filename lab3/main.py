from datetime import datetime
from functools import wraps
import time


# task1
def log_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        timestamp_start = start_time.strftime("[%Y-%m-%d %H:%M:%S]")

        with open("log.txt", "a", encoding="utf-8") as f:
            f.write(f"{timestamp_start} Функция '{func.__name__}' вызвана с аргументами: {args}\n")

        start = time.time()
        try:
            result = func(*args, **kwargs)
        except:
            result = None
        end = time.time()

        end_time = datetime.now()
        timestamp_end = end_time.strftime("[%Y-%m-%d %H:%M:%S]")
        with open("log.txt", "a", encoding="utf-8") as f:
            f.write(f"{timestamp_end} Функция '{func.__name__}' завершена. Время выполнения: {end - start:.1f} сек.\n")

        return result

    return wrapper


@log_decorator
def calculate(a, b, operation):
    if operation == '+':
        return a + b
    elif operation == '-':
        return a - b
    elif operation == '*':
        return a * b
    elif operation == '/':
        return a / b
    else:
        raise ValueError("Неподдерживаемая операция")


calculate(10, 5, '+')


# task2
def rate_limit(max_calls, period):
    def decorator(func):
        calls = []

        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal calls
            now = time.time()

            calls = [t for t in calls if t > now - period]

            if len(calls) >= max_calls:
                print("Превышен лимит вызовов. Попробуйте позже.")
                return

            calls.append(now)
            return func(*args, **kwargs)

        return wrapper

    return decorator


@rate_limit(max_calls=3, period=60)
def send_message(message):
    print(f"Сообщение отправлено: {message}")


for _ in range(5):
    send_message("Привет!")


# task3


def cache_decorator(func):
    cache = {}

    @wraps(func)
    def wrapper(*args):
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result

    return wrapper


@cache_decorator
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


print(fibonacci(10))
