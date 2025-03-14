import time

class TimedClass:
    def timing_decorator(func):
        """Декоратор для измерения времени выполнения метода."""
        def wrapper(self, *args, **kwargs):
            start_time = time.time()
            result = func(self, *args, **kwargs)
            end_time = time.time()
            print(f'Метод {func.__name__} выполнялся {end_time - start_time:.4f} секунд.')
            return result
        return wrapper

    @timing_decorator
    def slow_method(self):
        """Метод, который работает медленно."""
        time.sleep(2)  # Симуляция долгой работы
        print("Работа метода завершена.")

# Пример использования
timed_instance = TimedClass()
timed_instance.slow_method()  # Вызов медленного метода