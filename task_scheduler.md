``` python
print("Добро пожаловать в планировщик задач! 👋")
def print_menu():
    print('Меню:')
    print()
    print('1) Добавить задачу')
    print('2) Изменить задачу')
    print('3) Вывести список задач')
    print('4) Удалить задачу')
    print('5) Очистить список задач')
    print('6) Изменить настройки сортировки')
    print('0) Выйти из приложения')
s = []

def new_date_task(prompt = 'Введите дату задачи в формате дд.мм.гг: '):
    date = input(prompt).strip()
    if date[0:2].isdigit() and date[3:5].isdigit() and date[6:].isdigit():
        day = int(date[0:2])
        month = int(date[3:5])
        year = int(date[6:])
        month1 = [1, 3, 5, 7, 8, 10, 12]
        month2 = [4, 6, 9, 11]
        if 1 <= day <= 31 and month in month1 and 2025 <= year or 1 <= day <= 30 and month in month2 and 2025 <= year or 1 <= day <= 28 and month == 2 and 2025 <= year <= 2027:
            return date
        else:
            return "❌ Такой даты не существует! Пример: 01.01.2025"
    else:
        return "❌ Дата должна быть числом! Пример: 01.01.2025"

def new_time_task(prompt = 'Введите время задачи в формате чч:мм: '):
    time = input(prompt).strip()
    if time[0:2].isdigit() and time[3:].isdigit():
        hour = int(time[0:2])
        minute = int(time[3:])
        if 0 <= hour <= 23 and 0 <= minute <= 59:
            return time
        else:
            return "❌ Время должно не превышать допустимый диапазон! Пример: 07:30"
    else:
        return "❌ Время должно быть числом! Пример: 07:30"

def new_period_task():
    period = input('Введите период повторения задачи по дням недели (0 - не повторяем, 1 - повторяем): ').strip()
    if period.isdigit() and len(period) == 7:
        for c in period:
            if c not in ('0', '1'):
                return "❌ Ошибка, введите число 1 или 0. Пример: 0101010"
        print()
        days = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс']
        result = [days[k] for k in range(7) if period[k] == '1']
        if len(result) >= 1:
            return result
        else:
            return ['без повторений.']
    else:
        return "❌ Длина периода должна равняться 7 и он должен быть числом! Пример: 0101010"

def new_notification_task():
    notification = input('Введите время за которое нужно уведомить о задаче: \n1) 10 минут \n2) 30 минут \n3) 1 час \n4) 2 часа \n \nНапишите цифру: ').strip()  # тут нужно реализовать
    if notification.isdigit():
        notification = int(notification)
        if notification == 1:
            return '10 минут'
        elif notification == 2:
            return '30 минут'
        elif notification == 3:
            return '1 час'
        elif notification == 4:
            return '2 часа'
        else:
            return "❌ Ошибка! Такой цифры не существует!"
    else:
        return "❌ Ошибка! Нужно ввести число, а не текст!"


def append_task( name, date, time, period, notification, success_message='Задача добавлена! ✅'):
    task = {'name': name, 'date': date, 'time': time, 'period': period, 'notification': notification}
    s.append(task)
    print()
    print(success_message)

def add_task(name_prompt='Введите название задачи: ', success_message='Задача добавлена! ✅'):
    name = input(name_prompt).strip()
    if name == '':
         print()
         print('❌ Ошибка. Задача не может быть без названия!')
         return

    date = new_date_task()
    if date.startswith("❌"):
        print(date)
        return
    time = new_time_task()
    if time.startswith("❌"):
        print(time)
        return
    period = new_period_task()
    if isinstance(period, str) and period.startswith("❌"):
        print(period)
        return
    notification = new_notification_task()
    if notification.startswith("❌"):
        print(notification)
        return
    append_task(name, date, time, period, notification, success_message=success_message)

flag = 'not_sort'
while True:
     print()
     print_menu()
     print()
     num = input('Напишите цифру: ').strip()
     if num.isdigit():
         if int(num) == 1:
             print()
             add_task() #добавляем новую задачу
             while True:
                 if flag == 'not_sort':
                     print()
                     question = input('Сортировать в дальнейшем список дел по дате и времени? \n1) Да \n2) Нет \n \nВведите цифру: ').strip()
                     if question == '1':
                         flag = 'sort'
                         print()
                         print('Список ваших задач будет сортироваться!')
                         break
                     elif question == '2':
                         flag = 'stop_sort'
                         print()
                         print('Список ваших задач не будет сортироваться!')
                         break
                     else:
                         print()
                         print('❌ Ошибка! Нет такого варианта ответа')
                 if flag == 'sort':
                     s = sorted(s, key=lambda x: (int(x['date'][6:]), int(x['date'][3:5]), int(x['date'][0:2]), int(x['time'][0:2]), int(x['time'][3:])))


         elif int(num)  == 2:
             print()
             if len(s) == 0:
                 print("Список пуст! 😟")
             else:
                 print("Список дел 🤓:")
                 print()
                 for i in range(len(s)):
                    print(f'{i + 1}. {s[i]['name'].capitalize()} - {s[i]['date'][0:2]}.{s[i]['date'][3:5]}.{s[i]['date'][6:]} {s[i]['time'][0:2]}:{s[i]['time'][3:]}. Периодичность: {', '.join(s[i]['period'])}')
                 print()
                 print("Если хотите вернуться назад, введите цифру 0.")
                 j = input("Какую по счету задачу хотите поменять?: ").strip()
                 print()
                 if j.isdigit():
                     j = int(j)
                     print(f'Вы выбрали задачу: \n \n{j}. {s[j - 1]['name'].capitalize()} - {s[j - 1]['date'][0:2]}.{s[j - 1]['date'][3:5]}.{s[j - 1]['date'][6:]} {s[j - 1]['time'][0:2]}:{s[j - 1]['time'][3:]}. Периодичность: {', '.join(s[j - 1]['period'])}')
                     print()
                     if 1 <= j <= len(s):
                         request = input(f"Что именно в задаче желаете изменить? \n1) Дату \n2) Время \n3) Название \n4) Период повторения \n5) Время, через сколько напомнить \n6) Полностью изменить задачу \n7) Вернуться назад \n \nВыберите цифру: ").strip()
                         if request == '1':
                             print()
                             new_date = new_date_task("Введите новую дату в формате дд.мм.гг: ")
                             if new_date.startswith("❌"):
                                 print(new_date)
                             else:
                                 s[j - 1]['date'] = new_date
                                 print()
                                 print("Дата изменена ✅")
                         elif request == '2':
                             print()
                             new_time = new_time_task("Введите новое время в формате дд.мм.гг: ")
                             if new_time.startswith("❌"):
                                 print(new_time)
                             else:
                                 s[j - 1]['time'] = new_time
                                 print()
                                 print("Время изменено ✅")
                         elif request == '3':
                             print()
                             new_name = input('Введите новое название задачи: ').strip()
                             s[int(j) - 1]['name'] = new_name
                             print()
                             print("Название изменено ✅")
                         elif request == '4':
                             print()
                             new_period = new_period_task()
                             if isinstance(new_period, str) and new_period.startswith("❌"): #если строка
                                 print(new_period)
                             else:
                                 s[j - 1]['period'] = new_period
                                 print("Период изменен ✅")
                         elif request == '5':
                             print()
                             new_notification = new_notification_task()
                             if new_notification.startswith("❌"):
                                 print(new_notification)
                             else:
                                 s[j - 1]['notification'] = new_notification
                                 print()
                                 print("Время напоминания изменено ✅")
                         elif request == '6':
                             del s[j - 1]
                             print()
                             add_task(name_prompt='Введите новое название задачи: ', success_message=f'Задача {j} была изменена! ✅')
                             print()
                         elif request == '7':
                             print()
                             print("Возвращаемся назад...")
                         else:
                             print()
                             print("Такого варианта ответа не существует, попробуйте снова! ❌")
                     elif int(j) == 0:
                         print("Возвращаемся назад...")
                     else:
                         print()
                         print("Такая задача не существует! ❌")
                 else:
                     print()
                     print("Ошибка! Нужно ввести число, а не текст! ❌")

         elif int(num) == 3:
             print()
             if len(s) == 0:
                 print("Список пуст! 😟")
             else:
                 print("Список дел 🤓:")
                 for i in range(len(s)):
                    print(f'{i + 1}. {s[i]['name'].capitalize()} - {s[i]['date'][0:2]}.{s[i]['date'][3:5]}.{s[i]['date'][6:]} {s[i]['time'][0:2]}:{s[i]['time'][3:]}. Периодичность: {', '.join(s[i]['period'])}')
         elif int(num)  == 4:
             print()
             if len(s) == 0:
                 print("Список уже пуст! 😟")
             else:
                 print("Список дел 🤓:")
                 for i in range(len(s)):
                     print(
                         f'{i + 1}. {s[i]['name'].capitalize()} - {s[i]['date'][0:2]}.{s[i]['date'][3:5]}.{s[i]['date'][6:]} {s[i]['time'][0:2]}:{s[i]['time'][3:]}. Периодичность: {', '.join(s[i]['period'])}')
                 print()
                 print("Если хотите вернуться назад, введите цифру 0.")
                 del_text = input("Какую задачу из списка хотите удалить?: ").strip()
                 if del_text.isdigit():
                    if 1 <= int(del_text) <= len(s):
                        del s[int(del_text) - 1]
                        print()
                        print("Задача удалена! ✅")
                    elif int(del_text) == 0:
                        print()
                        print("Возвращаемся назад...")
                    else:
                        print("Такая задача не существует! ❌")
                 else:
                     print()
                     print("Ошибка! Нужно ввести число, а не текст! ❌")
         elif int(num)  == 5:
             print()
             clear_s = input("Вы уверены что хотите полностью очистить список? \n1) Да \n2) Вернуться назад \n \nВаш ответ: " ).strip()
             print()
             if clear_s == "1":
                 if len(s) >= 1:
                     s.clear()
                     print('Список был очищен! ✅')
                 else:
                     print("Список уже пуст! 👌")
             elif clear_s == "2":
                 print("Возвращаемся назад...")
             else:
                 print('Нет такого варианта ответа! ❌')
         elif int(num) == 6:
             question = input('Сортировать в дальнейшем список дел по дате и времени? \n1) Да \n2) Нет \n \nВведите цифру: ').strip()
             if question == '1':
                 flag = 'sort'
             elif question == '2':
                 flag = 'stop_sort'
         elif int(num)  == 0:
             print()
             print("До свидания! 👋")
             break
         else:
             print()
             print("Команда не существует ❌")
     else:
         print()
         print("Ошибка! Нужно ввести число, а не текст! ❌")
```
