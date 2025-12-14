import schedule
import time
import datetime
import threading
import json
#еще исправить изменение периода

print("Добро пожаловать в планировщик задач! 👋")
def print_menu():
    print()
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
s_copy = []


current_prompt = ""
current_input = ""     # что ввёл пользователь
input_active = False  # сейчас ждём ввод или нет
NOTIFY_BUFFER = []
file_tasks = 'tasks.json'
file_tasks_copy = 'tasks_copy.json'

def write_json(file_name, data):
    with open(file_name, 'w', encoding="utf8") as file:
        json_items = json.dumps(data)
        file.write(json_items)

def read_json(file_name):
    with open(file_name, 'r', encoding="utf8") as file:
        file_read = file.read()
        new_json = json.loads(file_read)
        return new_json

def safe_input(prompt):
    global current_input, current_prompt, input_active, NOTIFY_BUFFER

    current_input = ""
    current_prompt = prompt
    input_active = True

    text = input(prompt)

    # пользователь закончил ввод
    current_input = text
    input_active = False

    # если уведомления пришли во время ввода — вывести их строго ПОСЛЕ Enter
    if NOTIFY_BUFFER:
        print()
        for name in NOTIFY_BUFFER:
            print(f"🔔 Уведомление о задаче: {name}")
        print()
        NOTIFY_BUFFER = []  #  очищаем буфер
    print()
    return text

def new_date_task(prompt = 'Введите дату задачи в формате дд.мм.гг: '):
    date = safe_input(prompt).strip()
    for sep in ['/', '-', '\\', ' ', ',']:
        date = date.replace(sep, '.')
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
    time_task = safe_input(prompt).strip()
    for sep in ['.', '-', '/', '\\', ' ', ',']:
        time_task = time_task.replace(sep, ':')
    if time_task[0:2].isdigit() and time_task[3:].isdigit():
        hour = int(time_task[0:2])
        minute = int(time_task[3:])
        if 0 <= hour <= 23 and 0 <= minute <= 59:
            return time_task
        else:
            return "❌ Время должно не превышать допустимый диапазон! Пример: 07:30"
    else:
        return "❌ Время должно быть числом! Пример: 07:30"

def new_period_task():
    period = safe_input('Введите период повторения задачи по дням недели (0 - не повторяем, 1 - повторяем): ').strip()

    if period.isdigit() and len(period) == 7:
        for c in period:
            if c not in ('0', '1'):
                return "❌ Ошибка, введите число 1 или 0. Пример: 0101010"
        days = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс']
        period_day = [days[k] for k in range(7) if period[k] == '1']
        period_day.append(period) # пример: ['пн', 'вт', 'ср', '1110000']
        if len(period_day) >= 1:
            return period_day
        else:
            return ['без повторений.']
    else:
        return "❌ Длина периода должна равняться 7 и он должен быть числом! Пример: 0101011 "

def new_notification_task():
    notification = safe_input('Введите время за которое нужно уведомить о задаче: \n1) 10 минут \n2) 30 минут \n3) 1 час \n4) 2 часа \n \nНапишите цифру: ').strip()  # тут нужно реализовать
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

def get_name(name):
    global input_active, current_input, current_prompt, NOTIFY_BUFFER

    if input_active:
        NOTIFY_BUFFER.append(name)
    else:
        # можно печатать сразу
        print(f"\n🔔 Уведомление о задаче: {name}\n")

def make_job(t):
    return lambda: get_name(t['name'])

def add_notification(task):
    day, month, year = map(int, task['date'].split('.'))
    task_date = datetime.date(year, month, day)
    today = datetime.date.today()

    def job():
        get_name(task['name'])

    if task_date == today:
        schedule.every().day.at(task['time']).do(job)
    else:
        weekday = task_date.weekday()
        period = task['period_raw']
        if period[weekday] == '1':
            weekdays_map = {
                0: schedule.every().monday,
                1: schedule.every().tuesday,
                2: schedule.every().wednesday,
                3: schedule.every().thursday,
                4: schedule.every().friday,
                5: schedule.every().saturday,
                6: schedule.every().sunday,
            }
            weekdays_map[weekday].at(task['time']).do(job)

def append_task(name, date, time_task, period, notification, success_message='Задача добавлена! ✅'):
    task = {'name': name, 'date': date, 'time': time_task, 'period': period, 'notification': notification}
    period_raw = ''.join('1' if day in period else '0'
                         for day in ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс'])
    task['period_raw'] = period_raw
    s.append(task)
    write_json(file_tasks, s)
    print()
    task_copy = task.copy()
    period_raw = ''.join('1' if day in period else '0' for day in ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс'])
    task_copy['period_raw'] = period_raw
    msg = notification_time(task_copy)
    s_copy.append(task_copy)
    write_json(file_tasks_copy, s_copy)
    print(msg) #нужно сделать чтобы время менялось только в копии, а на выводе оставалось тем же
    print()
    print(success_message)
    add_notification(task)
    add_notification(task_copy)

def add_task(name_prompt='Введите название задачи: ', success_message='Задача добавлена! ✅'):
    name = safe_input(name_prompt).strip()
    if name == '':
         print()
         print('❌ Ошибка. Задача не может быть без названия!')
         return
    date = new_date_task()
    if date.startswith("❌"):
        print(date)
        return
    time_task = new_time_task()
    if time_task.startswith("❌"):
        print(time_task)
        return
    period = new_period_task()[:-1]
    if isinstance(period, str) and period.startswith("❌"):
        print(period)
        return
    notification = new_notification_task()
    if notification.startswith("❌"):
        print(notification)
        return
    append_task(name, date, time_task, period, notification, success_message=success_message)

def notification_time(task):
    if task['notification'] == '10 минут':
        if int(task['time'][3:]) >= 10:
            hours = int(task["time"][0:2])
            minutes = int(task['time'][3:]) - 10
            time_notification = f'{hours:02d}:{minutes:02d}'
            task['time'] = time_notification
            return 'Напоминание установлено!'
        elif int(task['time'][3:]) < 10:
            minutes = int(task['time'][3:]) + 50
            if int(task['time'][0:2]) == 0:
                hour = int(task['time'][0:2]) + 23
                day = int(task['date'][0:2])
                month = int(task['date'][3:5])
                new_day_date = ''
                if day == 1: #дата меняется, если время напоминание уходит в прошлый месяц
                    new_month = int(task["date"][3:5])
                    if month == 11:
                        new_day_date = f'31.{new_month - 1:02d}.{int(task["date"][6:])}'
                    elif month in [10, 12]:
                        new_day_date = f'30.{new_month - 1:02d}.{int(task["date"][6:])}'
                    elif month == 3:
                        new_day_date = f'28.{new_month - 1:02d}.{int(task["date"][6:])}'
                    elif month == 1:
                        new_day_date = f'31.12.{int(task["date"][6:]) - 1}'
                    elif month in [2, 4, 6, 8, 9]:
                        new_day_date = f'31.{new_month - 1:02d}.{int(task["date"][6:])}'
                    elif month in [5, 7]:
                        new_day_date = f'30.{new_month - 1:02d}.{int(task["date"][6:])}'

                else:
                    day = int(task["date"][0:2])
                    month = int(task['date'][3:5])
                    new_day_date = f'{day - 1:02d}.{month:02d}.{int(task["date"][6:])}'
                task['date'] = new_day_date
            else:
                hour = int(task['time'][0:2]) - 1
            time_notification = f'{hour:02d}:{minutes:02d}'
            task['time'] = time_notification
            return 'Напоминание установлено!'
        return None

    elif task['notification'] == '30 минут':
        if int(task['time'][3:]) >= 30:
            hours = int(task["time"][0:2])
            minutes = int(task['time'][3:]) - 30
            time_notification = f'{hours:02d}:{minutes:02d}'
            task['time'] = time_notification
            return 'Напоминание установлено!'
        elif int(task['time'][3:]) < 30:
            minutes = int(task['time'][3:]) + 30
            if int(task['time'][0:2]) == 0:
                hour = int(task['time'][0:2]) + 23
                day = int(task['date'][0:2])
                month = int(task['date'][3:5])
                new_day_date = ''
                if day == 1: #дата меняется, если время напоминание уходит в прошлый месяц
                    if month == 11 :
                        new_day_date = f'31.{month- 1:02d}.{int(task["date"][6:])}'
                    elif month in [10, 12]:
                        new_day_date = f'30.{month - 1:02d}.{int(task["date"][6:])}'
                    elif month == 3:
                        new_day_date = f'28.{month - 1:02d}.{int(task["date"][6:])}'
                    elif month == 1:
                        new_day_date = f'31.12.{int(task['date'][6:]) - 1}'
                    elif month in [2, 4, 6, 8, 9]:
                        new_day_date = f'31.{month - 1:02d}.{int(task["date"][6:])}'
                    elif month in [5, 7]:
                        new_day_date = f'30.{month - 1:02d}.{int(task["date"][6:])}'
                else:
                    day = int(task["date"][0:2])
                    month = int(task['date'][3:5])
                    new_day_date = f'{day - 1:02d}.{month:02d}.{int(task["date"][6:])}'
                task['date'] = new_day_date
            hours = int(task["time"][0:2])
            time_notification = f'{hours:02d}:{minutes:02d}'
            task['time'] = time_notification
            return 'Напоминание установлено!'
        return None

    elif task['notification'] == '1 час':
        if int(task['time'][:2]) > 0:
            hour = int(task["time"][0:2])
            minutes = int(task['time'][3:])
            time_notification = f'{hour - 1:02d}:{minutes:02d}'
            task['time'] = time_notification
            return 'Напоминание установлено!'
        elif int(task['time'][:2]) == 0:
            hour = int(task['time'][0:2]) + 23
            day = int(task['date'][0:2])
            month = int(task['date'][3:5])
            new_day_date = ''
            if day == 1: #дата меняется, если время напоминание уходит в прошлый месяц
                if month == 11:
                    new_day_date = f'31.{month - 1:02d}.{int(task["date"][6:])}'
                elif month in [10, 12]:
                    new_day_date = f'30.{month - 1:02d}.{int(task["date"][6:])}'
                elif month == 3:
                    new_day_date = f'28.{month - 1:02d}.{int(task["date"][6:])}'
                elif month == 1:
                    new_day_date = f'31.12.{int(task["date"][6:]) - 1}'
                elif month in [2, 4, 6, 8, 9]:
                    new_day_date = f'31.{month - 1:02d}.{int(task["date"][6:])}'
                elif month in [5, 7]:
                    new_day_date = f'30.{month - 1:02d}.{int(task["date"][6:])}'
            else:
                day = int(task["date"][0:2])
                new_day_date = f'{day - 1:02d}.{int(task["date"][3:5])}.{int(task["date"][6:])}'
            task['date'] = new_day_date
        else:
            hour = int(task['time'][0:2]) - 1
        minutes = int(task['time'][3:])
        time_notification = f'{hour:02d}:{minutes:02d}'
        task['time'] = time_notification
        return 'Напоминание установлено!'

    elif task['notification'] == '2 часа':
        if int(task['time'][:2]) > 1:
            minutes = int(task['time'][3:])
            hour = int(task["time"][0:2])
            time_notification = f'{hour - 2:02d}:{minutes:02d}'
            task['time'] = time_notification
            return 'Напоминание установлено!'
        elif int(task['time'][:2]) <= 1:
            hour = 0
            if int(task['time'][:2]) == 1:
                hour = 23
            elif int(task['time'][:2]) == 0:
                hour = 22
            day = int(task['date'][0:2])
            month = int(task['date'][3:5])
            new_day_date = ''
            if day == 1:  # дата меняется, если время напоминание уходит в прошлый месяц
                if month == 11:
                    new_day_date = f'31.{month - 1:02d}.{int(task["date"][6:])}'
                elif month in [10, 12]:
                    new_day_date = f'30.{month - 1:02d}.{int(task["date"][6:])}'
                elif month == 3:
                    new_day_date = f'28.{month - 1:02d}.{int(task["date"][6:])}'
                elif month == 1:
                    new_day_date = f'31.12.{int(task["date"][6:]) - 1}'
                elif month in [2, 4, 6, 8, 9]:
                    new_day_date = f'31.{month - 1:02d}.{int(task["date"][6:])}'
                elif month in [5, 7]:
                    new_day_date = f'30.{month - 1:02d}.{int(task["date"][6:])}'
            else:
                day = int(task["date"][0:2])
                new_day_date = f'{day - 1:02d}.{int(task["date"][3:5])}.{int(task["date"][6:])}'
            task['date'] = new_day_date
        else:
            hour = int(task['time'][0:2]) - 2
        minutes = int(task['time'][3:])
        time_notification = f'{hour:02d}:{minutes:02d}'
        task['time'] = time_notification
        return 'Напоминание установлено!'
    return None

def schedule_worker():
    while True:
        schedule.run_pending()
        time.sleep(1)

def change_task():
    global s
    global s_copy
    if len(s) == 0:
        print("Список пуст! 😟")
    else:
        print("Список дел 🤓:")
        print()
        for i in range(len(s)):
            print(
                f'{i + 1}. {s[i]['name'].capitalize()} - {s[i]['date'][0:2]}.{s[i]['date'][3:5]}.{s[i]['date'][6:]} {s[i]['time'][0:2]}:{s[i]['time'][3:]}. Периодичность: {', '.join(s[i]['period'])}')
        print()
        print("Если хотите вернуться назад, введите цифру 0.")
        print()
        j = safe_input("Какую по счету задачу хотите поменять?: ").strip()
        if j.isdigit():
            j = int(j)
            if int(j) == 0:
                print("Возвращаемся назад...")
                return
            if 1 > j or j > len(s):
                print("Такая задача не существует! ❌")
                return
            print(
                f'Вы выбрали задачу: \n \n{j}. {s[j - 1]['name'].capitalize()} - {s[j - 1]['date'][0:2]}.{s[j - 1]['date'][3:5]}.{s[j - 1]['date'][6:]} {s[j - 1]['time'][0:2]}:{s[j - 1]['time'][3:]}. Периодичность: {', '.join(s[j - 1]['period'])}')
            print()

            if 1 <= j <= len(s):
                request = safe_input(
                    f"Что именно в задаче желаете изменить? \n1) Дату \n2) Время \n3) Название \n4) Период повторения \n5) Время, через сколько напомнить \n6) Полностью изменить задачу \n7) Вернуться назад \n \nВыберите цифру: ").strip()
                if request == '1':
                    new_date = new_date_task("Введите новую дату в формате дд.мм.гг: ")
                    if new_date.startswith("❌"):
                        print(new_date)
                        return
                    else:
                        s[j - 1]['date'] = new_date
                        s_copy[j - 1]['date'] = new_date
                        print("Дата изменена ✅")
                elif request == '2':

                    new_time = new_time_task("Введите новое время в формате чч:мм: ")
                    if new_time.startswith("❌"):
                        print(new_time)
                        return
                    else:
                        s[j - 1]['time'] = new_time
                        s_copy[j - 1]['time'] = new_time
                        notification_time(s_copy[j - 1]) #меняет напоминание по новому времени

                        print("Время изменено ✅")
                elif request == '3':
                    new_name = safe_input('Введите новое название задачи: ').strip()
                    s[int(j) - 1]['name'] = new_name
                    s_copy[int(j) - 1]['name'] = new_name
                    print("Название изменено ✅")
                elif request == '4':
                    new_periods = new_period_task()
                    new_period = new_periods[:-1]
                    new_period_raw = new_periods[-1]
                    if isinstance(new_period, str) and new_period.startswith("❌"):  # если строка
                        print(new_period)
                        return
                    else:
                        s[j - 1]['period'] = new_period
                        s_copy[j - 1]['period'] = new_period
                        s[j - 1]['period_raw'] = new_period_raw
                        s_copy[j - 1]['period_raw'] = new_period_raw

                        # сделать тут чтобы если менялся период, сначала менялось старое время(из оригинала) потом применялся новый период\ хз зачем, пока пусть висит


                        print("Период изменен ✅")
                elif request == '5':
                    print()
                    new_notification = new_notification_task()
                    if new_notification.startswith("❌"):
                        print(new_notification)
                        return
                    else:
                        s[j - 1]['notification'] = new_notification
                        s_copy[j - 1]['notification'] = new_notification
                        print()
                        print("Время напоминания изменено ✅")
                elif request == '6':
                    del s[j - 1]
                    del s_copy[j - 1]
                    print()
                    add_task(name_prompt='Введите новое название задачи: ',
                             success_message=f'Задача {j} была изменена! ✅')
                    print()
                elif request == '7':
                    print()
                    print("Возвращаемся назад...")
                    return
                else:
                    print()
                    print("Такого варианта ответа не существует, попробуйте снова! ❌")
                    return

        else:
            print()
            print("Ошибка! Нужно ввести число, а не текст! ❌")
            return

    write_json(file_tasks_copy, s_copy)
    write_json(file_tasks, s)

thread = threading.Thread(target=schedule_worker, daemon=True)
thread.start()

s = read_json(file_tasks)
s_copy = read_json(file_tasks_copy)

try:
    def main():
        global s
        global s_copy
        flag = 'not_sort'
        while True:
            while True:
                if flag == 'not_sort':
                    print()
                    question = safe_input(
                        'Сортировать в дальнейшем список дел по дате и времени? \n1) Да \n2) Нет \n \nВведите цифру: ').strip()
                    if question == '1':
                        flag = 'sort'
                        print('Список ваших задач будет сортироваться!')
                        break
                    elif question == '2':
                        flag = 'stop_sort'
                        print('Список ваших задач не будет сортироваться!')
                        break
                    else:
                        print()
                        print('❌ Ошибка! Нет такого варианта ответа')
                elif flag == 'sort':
                    s = sorted(s, key=lambda x: (int(x['date'][6:]), int(x['date'][3:5]), int(x['date'][0:2]),
                                                 int(x['time'][0:2]), int(x['time'][3:])))
                    s_copy = sorted(s_copy, key=lambda x: (int(x['date'][6:]), int(x['date'][3:5]), int(x['date'][0:2]),
                                                 int(x['time'][0:2]), int(x['time'][3:])))
                    break
    
                elif flag == 'stop_sort':
                    break
                elif flag == 'stop_sort_fake':
                    print('Нет такого варианта ответа! ❌')
                    flag = 'stop_sort'
                    break
                elif flag == 'sort_fake':
                    print('Нет такого варианта ответа! ❌')
                    flag = 'sort'
                    break
            print_menu()
            print()
            num = safe_input('Напишите цифру: ').strip()
            if num.isdigit():
                if int(num) == 1:
                    add_task() #добавляем новую задачу
                elif int(num)  == 2:
                    change_task() #изменение задачи
                elif int(num) == 3: #вывести задачу
                    if len(s) == 0:
                        print("Список пуст! 😟")
                    else:
                        print("Список дел 🤓:")
                        for i in range(len(s)):
                            print(f'{i + 1}. {s[i]['name'].capitalize()} - {s[i]['date'][0:2]}.{s[i]['date'][3:5]}.{s[i]['date'][6:]} {s[i]['time'][0:2]}:{s[i]['time'][3:]}. Периодичность: {', '.join(s[i]['period'])}')
                elif int(num)  == 4: #удаление задачи
                    if len(s) == 0:
                        print("В списке нет задач! 😟")
                    else:
                        print("Список дел 🤓:")
                        for i in range(len(s)):
                            print(f'{i + 1}. {s[i]['name'].capitalize()} - {s[i]['date'][0:2]}.{s[i]['date'][3:5]}.{s[i]['date'][6:]} {s[i]['time'][0:2]}:{s[i]['time'][3:]}. Периодичность: {', '.join(s[i]['period'])}')
                        print()
                        print("Если хотите вернуться назад, введите цифру 0.")
                        print()
                        del_text = safe_input("Какую задачу из списка хотите удалить?: ").strip()
                        if del_text.isdigit():
                            if 1 <= int(del_text) <= len(s):
                                del s[int(del_text) - 1]
                                del s_copy[int(del_text) - 1]
                                print()
                                write_json(file_tasks, s)
                                write_json(file_tasks_copy, s_copy)
                                print("Задача удалена! ✅")
                            elif int(del_text) == 0:
                                print("Возвращаемся назад...")
                            else:
                                print("Такая задача не существует! ❌")
                        else:
                            print()
                            print("Ошибка! Нужно ввести число, а не текст! ❌")
                elif int(num)  == 5: #очистить список задач
                    clear_s = safe_input("Вы уверены что хотите полностью очистить список? \n1) Да \n2) Вернуться назад \n \nВаш ответ: " ).strip()
    
                    if clear_s == "1":
                        if len(s) >= 1:
                            s.clear()
                            s_copy.clear()
                            write_json(file_tasks, s)
                            write_json(file_tasks_copy, s_copy)
                            print('Список был очищен! ✅')
                        else:
                            print("Список уже пуст! 👌")
                    elif clear_s == "2":
                        print("Возвращаемся назад...")
                    else:
                        print('Нет такого варианта ответа! ❌')
                elif int(num) == 6:
                    question = safe_input('Сортировать в дальнейшем список дел по дате и времени? \n1) Да \n2) Нет \n \nВведите цифру: ').strip()
                    if question == '1':
                        flag = 'sort'
                        print('Список ваших задач теперь будет сортироваться!')
                    elif question == '2':
                        flag = 'stop_sort'
                        print('Список ваших задач больше не будет сортироваться!')
                    else:
                        if flag == 'stop_sort':
                            flag = 'stop_sort_fake'
                        else:
                            flag = 'sort_fake'
                elif int(num)  == 0:
                    print("До свидания! 👋")
                    break
                else:
                    print()
                    print("Команда не существует ❌")
            else:
                print()
                print("Ошибка! Нужно ввести число, а не текст! ❌")
except Exception:
    print('Произошла ошибка!')
main()
