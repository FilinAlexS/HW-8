from subprocess import PIPE, Popen, check_output
import re
import platform
import time

report = []
this_platform = ""


def get_platform():
    global this_platform
    if this_platform != "":
        return this_platform
    else:
        this_platform = _this_platform()
        return this_platform


def _this_platform():
    return platform.system()


def get_platform_info():
    return check_output(['ps', 'aux']).decode('utf-8')


def total_memory():
    if this_platform == "Darwin":
        return float(_mac_os())
    elif this_platform == "Linux":
        return float(_linux())


def _mac_os():
    sub_process = Popen(['top', '-l 1', '-s 0'], stdout=PIPE)
    process = Popen(['grep', 'PhysMem'], stdin=sub_process.stdout, stdout=PIPE)
    mem = process.communicate()
    used_memory = int(re.split("b'|'|M", str(mem[0].split()[1]))[1])
    unused_memory = int(re.split("b'|'|M", str(mem[0].split()[5]))[1])
    return used_memory + unused_memory


def _linux():
    process = check_output(['free', '--mega']).decode('utf-8')
    proc = process.split('\n')
    proc.pop(0)
    proc.pop(1)
    memory = " ".join(str(proc).split())
    return int(memory.split()[1])


def create_report():
    # Сохраняем отчет в отдельный файл
    current_time = time.strftime("%d-%m-%Y-%H:%M:%S")
    file_name = current_time + "-scan" + ".txt"
    with open(file_name, 'w', newline='\n') as f:
        for line in report:
            f.write(line)


def my_print(string: str):
    print(string)
    report.append(string + "\n")
