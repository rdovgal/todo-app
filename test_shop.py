# День 14 — тесты: как программисты проверяют, что код не сломался
# Запуск: python3 день14_тесты.py
# Ничего ставить не нужно: unittest встроен в Python.
#
# ЗАЧЕМ ЭТО НА ДНЕ ПРО DOCKER И CI/CD?
# CI (Continuous Integration) = «после каждого git push робот САМ запускает тесты».
# Тесты зелёные ✅ → код можно выкладывать (деплоить). Красные ❌ → стоп, кто-то сломал.
# То есть сначала нужны ТЕСТЫ — без них CI нечего запускать. Сегодня пишем их руками.
#
# ТЕСТ — это маленькая программа, которая проверяет другую программу:
#   «вызови функцию с такими данными → результат ДОЛЖЕН быть вот таким».
# Если функция вернула что-то другое — тест падает и пишет, где именно.
#
# UNIT-ТЕСТ (модульный) — проверяет ОДНУ функцию отдельно от всего остального.
# Это самые быстрые и самые частые тесты. Их на собеседовании и имеют в виду.

import unittest


# ======================= КОД, КОТОРЫЙ ПРОВЕРЯЕМ =======================
# Представь, что это кусок интернет-магазина из дня 13 (таблица orders).

def total_price(prices):
    """Сумма заказа. prices — список цен, например [80000, 1500]."""
    return sum(prices)


def apply_discount(price, percent):
    """Цена со скидкой. apply_discount(1000, 10) → 900.0"""
    if percent < 0 or percent > 100:
        raise ValueError("Скидка должна быть от 0 до 100")   # raise = «выбросить ошибку» сознательно
    return price * (100 - percent) / 100


def is_adult(age):
    """Совершеннолетний ли пользователь (как WHERE age >= 18 в дне 13)."""
    return age >= 18
def average_age(ages):
    """Средний возраст, округлённый до 1 знака (как AVG в дне 13)."""
    if len(ages) == 0:
        return 0
    return round(sum(ages) / len(ages), 1)
def delivery_cost(total):
    """Стоимость доставки: 300 ₽, но если сумма заказа от 5000 ₽ — бесплатно."""
    if total >= 5000:
        return 0
    return 300


# ======================= ТЕСТЫ =======================
# Правила unittest:
#   1. Класс наследуется от unittest.TestCase (ООП из бонуса недели 1!)
#   2. Каждый метод, имя которого начинается с test_, — это отдельный тест
#   3. Внутри — проверки assert...: «утверждаю, что...»

class TestShop(unittest.TestCase):

    def test_total_price(self):
        self.assertEqual(total_price([80000, 1500]), 81500)   # assertEqual(факт, ожидание)

    def test_total_price_empty(self):
        # Пустой заказ — КРАЕВОЙ СЛУЧАЙ (edge case). Тестировщики любят именно такие.
        self.assertEqual(total_price([]), 0)

    def test_discount(self):
        self.assertEqual(apply_discount(1000, 10), 900)

    def test_discount_zero(self):
        self.assertEqual(apply_discount(1000, 0), 1000)

    def test_discount_bad_percent(self):
        # Проверяем, что на плохие данные функция РУГАЕТСЯ, а не молча считает чепуху.
        with self.assertRaises(ValueError):
            apply_discount(1000, 150)

    def test_is_adult(self):
        self.assertTrue(is_adult(22))     # Аня
        self.assertFalse(is_adult(17))    # Лена
        self.assertTrue(is_adult(18))  
        
    def test_average_age(self):
        self.assertEqual(average_age([22, 30, 17]), 23.0)

    def test_average_age_empty(self):
        self.assertEqual(average_age([]), 0) 
    def test_delivery(self):
        self.assertEqual(delivery_cost(1000), 300)    # дёшево — платим
        self.assertEqual(delivery_cost(5000), 0)      # ровно 5000 — граница! уже бесплатно
        self.assertEqual(delivery_cost(10000), 0)     # дорого — бесплатно  # граница! ровно 18 — уже взрослый


if __name__ == "__main__":
    unittest.main(verbosity=2)   # verbosity=2 — печатать каждый тест по имени

# Что ты увидишь:
#   test_discount ... ok
#   ...
#   Ran 6 tests in 0.001s
#   OK                      ← всё зелёное. Именно это CI проверяет после каждого push.
#
# Если тест упал — будет FAIL и строка вида  AssertionError: 950.0 != 900
#   (слева — что вернула функция, справа — что ты ожидал).
#
#
# ======================= ЗАДАНИЯ =======================
#
# 1. Сломай код специально.
#    В apply_discount замени (100 - percent) на (100 + percent). Запусти.
#    Какие тесты упали? Прочитай сообщение AssertionError. Верни как было.
#    👉 Ровно так CI ловит баг ДО того, как он попадёт к пользователям (в prod).
#
# 2. Тест на свою функцию.
#    Напиши функцию average_age(ages) — средний возраст, округлённый до 1 знака
#    (как AVG в дне 13). Напиши тест: average_age([22, 30, 17]) == 23.0
#    Подумай про краевой случай: что будет при average_age([])? Деление на ноль!
#    Реши, что функция должна делать (вернуть 0? выбросить ValueError?) и напиши тест на это.
#
# 3. TDD (Test-Driven Development — «сначала тест, потом код»).
#    Сначала напиши тест test_delivery: доставка стоит 300 ₽, но если сумма заказа
#    от 5000 ₽ — бесплатно. Проверь 3 случая: 1000 → 300, 5000 → 0, 10000 → 0.
#    Запусти — тест упадёт (функции ещё нет). Теперь напиши delivery_cost(total),
#    чтобы тест позеленел. Это и есть TDD — слово для собеседования.
#
# 4. (Бонус, настоящий CI) Подключи GitHub Actions к репозиторию из дня 9.
#    Инструкция и готовый файл ci.yml — в 14_DevOps_шпаргалка.md, раздел 3.
#    После push открой вкладку Actions на GitHub — увидишь зелёную галочку ✅.
#    Это можно смело писать в резюме: «настроил CI на GitHub Actions».
#
# Самопроверка: объясни вслух — unit-тест, CI, CD, деплой, Docker-контейнер,
#   dev / staging / prod. Если какое-то слово «плывёт» — перечитай шпаргалку.
