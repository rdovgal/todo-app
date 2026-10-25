# День 7 — мини-проект: менеджер задач (To-Do)
# Запуск: python3 день07_todo.py
#
# Это твой ПЕРВЫЙ ПРОЕКТ для портфолио (на 9-й день зальём его на GitHub).
# Здесь собрано всё, что ты выучил за неделю:
#   списки (день 5), функции (день 6), while/for/break (день 4),
#   if/elif/else (день 3), try/except (бонус дня 4).
#
# Как устроена программа:
#   tasks = []           — список задач (строки): ["купить хлеб", "сделать уроки"]
#   show_tasks(tasks)    — показать все задачи с номерами
#   add_task(tasks)      — спросить задачу и добавить в список
#   delete_task(tasks)   — спросить номер и удалить задачу
#   main()               — главное меню (уже готово, его трогать не надо)
#
# ВАЖНО: когда мы передаём СПИСОК в функцию, функция работает с ТЕМ ЖЕ САМЫМ списком.
# Если внутри функции сделать tasks.append(...) — задача появится и в главном списке.
# Поэтому return здесь не нужен.


# ===== ЗАДАНИЕ 1: показать задачи =====
# Если список пустой — напечатай "Список задач пуст 🎉".
# Иначе — выведи задачи с номерами:
#     1. купить хлеб
#     2. сделать уроки
# Подсказка: пустой список проверяется так:  if len(tasks) == 0:
# Номера — как в списке покупок (день 5): счётчик number = 1 и number += 1.
def show_tasks(tasks):
    if len(tasks) == 0 :
        print("Список задач пуст 🎉")
    else:
        number = 1
        for task in tasks:
            print(f"{number}. {task}")
            number += 1


# ===== ЗАДАНИЕ 2: добавить задачу =====
# Спроси текст задачи через input и добавь его в список (append).
# Напиши "Задача добавлена ✅".
def add_task(tasks):
    task = input("Новая задача: ")
    tasks.append(task)
    print("Задача добавлена")


# ===== ЗАДАНИЕ 3: удалить задачу =====
# 1) Покажи задачи (вызови свою функцию show_tasks(tasks) — функции могут вызывать функции!)
# 2) Спроси номер задачи и преврати его в число через int().
# 3) Люди считают с 1, а Python с 0. Поэтому индекс = номер - 1.
# 4) Удали задачу: tasks.pop(индекс) — pop удаляет элемент по индексу и ВОЗВРАЩАЕТ его.
#        removed = tasks.pop(index)
#        print(f"Удалено: {removed}")
# 5) Защита от ошибок:
#      - ввели не число → try/except ValueError → "Нужно ввести число"
#      - номер вне списка (например 99) → проверь: if 1 <= number <= len(tasks):
def delete_task(tasks):
    show_tasks(tasks)
    try:
        number = int(input("Номер задачи для удаления: "))
    except ValueError:
        print("Нужно ввести число")
        return
    if 1 <= number <= len(tasks):
        index = number - 1
        removed = tasks.pop(index)
        print(f"Удалено: {removed}")
    else:
        print("Нет задачи с таким номером")


def save_tasks(tasks):
    with open("tasks.txt", "w") as f:
        for task in tasks:
            f.write(task + "\n")


def load_tasks():
    try:
        with open("tasks.txt") as f:
            return f.read().splitlines()
    except FileNotFoundError:
        return []


# ===== ГЛАВНОЕ МЕНЮ (уже готово) =====
def main():
    tasks = load_tasks()
    print("📝 Менеджер задач")

    while True:
        print()
        print("1 — показать задачи")
        print("2 — добавить задачу")
        print("3 — удалить задачу")
        print("0 — выход")
        choice = input("Выбери: ")

        if choice == "1":
            show_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            delete_task(tasks)
        elif choice == "0":
            save_tasks(tasks) 
            print("задачи сохранены 💾 Пока! 👋")
            break
        else:
            print("Нет такого пункта")


main()


# ===== БОНУСЫ (когда основное заработает) =====
# Бонус 1: сохранять задачи в файл, чтобы они не пропадали после выхода.
#   Запись:   with open("tasks.txt", "w") as f:
#                 for task in tasks:
#                     f.write(task + "\n")        # "\n" — перенос строки
#   Чтение:   with open("tasks.txt") as f:
#                 tasks = f.read().splitlines()   # каждая строка файла → элемент списка
#
# Бонус 2: отмечать задачу выполненной ✅ (храни задачи как словари:
#   {"title": "купить хлеб", "done": False}).
