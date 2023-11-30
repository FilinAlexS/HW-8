from helpers import total_memory, get_platform, my_print, get_platform_info


def scan():
    # Получаем информацию о процессах
    process_info = get_platform_info()

    # Разбиваем информацию о процессах на строки
    process_info_lines = process_info.split('\n')

    # Удаляем первую строку
    process_info_lines.pop(0)

    # Определяем количество пользователей, запущенных процессов и пользовательских процессов
    users = set()
    total_processes = 0
    user_processes = {}
    for line in process_info_lines:
        if not line:
            continue
        columns = line.split()
        user = columns[0]
        if user not in users:
            users.add(user)
        if user not in user_processes:
            user_processes[user] = 0
        user_processes[user] += 1
        total_processes += 1

    # Определяем количество используемой памяти и CPU
    memory_usage = 0
    cpu_usage = 0
    for line in process_info_lines:
        if not line:
            continue
        columns = line.split()
        memory_usage += float(columns[3])
        cpu_usage += float(columns[2])

    # Определяем процессы, которые используют больше всего памяти и CPU
    memory_usage_max = 0
    cpu_usage_max = 0
    memory_usage_process = None
    cpu_usage_process = None
    for line in process_info_lines:
        if not line:
            continue
        columns = line.split()
        memory_usage_current = float(columns[3])
        cpu_usage_current = float(columns[2])
        if memory_usage_current > memory_usage_max:
            memory_usage_max = memory_usage_current
            memory_usage_process = columns[10][:20]
        if cpu_usage_current > cpu_usage_max:
            cpu_usage_max = cpu_usage_current
            cpu_usage_process = columns[10][:20]

    # Выводим отчет о состоянии системы
    my_print(f"Отчёт о состоянии системы:")
    my_sep = "', '"
    my_print(f"Пользователи системы: '{my_sep.join(sorted(users))}'")
    my_print(f"Процессов запущено: {total_processes}")
    my_print(f"Пользовательских процессов:")
    for user, processes in sorted(user_processes.items()):
        my_print(f"{user}: {processes}")
    if get_platform() == "Linux" or get_platform() == "Darwin":
        my_print(f"Всего памяти используется: {round(total_memory() * (memory_usage / 100), 2)} mb")
    else:
        my_print(f"Всего памяти используется: {round(memory_usage, 2)} %")
        my_print(f"'Не предусмотрен подсчёт кол-во оперативной памяти в МБ для системы - {get_platform()}'")
    my_print(f"Всего CPU используется: {round(cpu_usage, 2)} %")
    my_print(f"Больше всего памяти использует: {memory_usage_process}")
    my_print(f"Больше всего CPU использует: {cpu_usage_process}")
