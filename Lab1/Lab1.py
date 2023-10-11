import matplotlib.pyplot as pyplot
import control.matlab as matlab
import numpy
import math
import colorama

INERTIALESS_UNIT_NAME = 'Безынерционное звено'
APERIODIC_UNIT_NAME = 'Апериодическое звено'
INTEGRATING_UNIT_NAME = 'Интегрирующее звено'
IDEAL_DIFFERENTIATING_UNIT_NAME = 'Идеальное дифференцирующее звено'
REAL_DIFFERENTIATING_UNIT_NAME = 'Реальное дифференцирующее звено'

def choice():
    need_new_choice = True
    while need_new_choice:
        print(colorama.Style.RESET_ALL)
        user_input = input('Введите номер команды: \n'
                        '1 - ' + INERTIALESS_UNIT_NAME + '\n'
                        '2 - ' + APERIODIC_UNIT_NAME + '\n'
                        '3 - ' + INTEGRATING_UNIT_NAME + '\n'
                        '4 - ' + IDEAL_DIFFERENTIATING_UNIT_NAME + '\n'
                        '5 - ' + REAL_DIFFERENTIATING_UNIT_NAME + '\n')

        if user_input:
            need_new_choice =False
            if user_input == '1':
                name = INERTIALESS_UNIT_NAME
            elif user_input == '2':
                name = APERIODIC_UNIT_NAME
            elif user_input == '3':
                name = INTEGRATING_UNIT_NAME
            elif user_input == '4':
                name = IDEAL_DIFFERENTIATING_UNIT_NAME
            elif user_input == '5':
                name = REAL_DIFFERENTIATING_UNIT_NAME
            else:
                need_new_choice = True
                print(colorama.Fore.RED + '\n Недопустимое значение!')
        else:
            print(colorama.Fore.RED + '\n Введите числовое значение!')
    return name
def get_unit(unit_name):
    need_new_choice = True
    while need_new_choice:
        need_new_choice = False
        print(colorama.Style.RESET_ALL)
        if unit_name == INERTIALESS_UNIT_NAME:
            k = input('Введите коэффициент передачи звена (k): ')
            if k.isdigit():
                k = int(k)
                if unit_name == INERTIALESS_UNIT_NAME:
                    unit = matlab.tf([k], [1])
                else:
                    print(colorama.Fore.YELLOW + '\nНе реализовано')
            else:
                print(colorama.Fore.YELLOW + '\nПжалуйста, введите числовое значение')
        elif unit_name == APERIODIC_UNIT_NAME:
            k = input('Введите коэффициент передачи звена (k): ')
            t = input('Введите постоянную времени звена (T): ')
            if k.isdigit() and t.isdigit():
                k = int(k)
                t = int(t)
                if unit_name == APERIODIC_UNIT_NAME:
                    unit = matlab.tf([k],  [t, 1])
                    need_new_choice = False
                else:
                    print(colorama.Fore.YELLOW + '\nНе реализовано')
            else:
                print(colorama.Fore.RED + '\n Пожалуйста, введите числовое значение!')
                need_new_choice = True
        elif unit_name == INTEGRATING_UNIT_NAME:
            t = input('Введите постоянную времени звена (Т): ')
            if t.isdigit:
                t = int(t)
                if unit_name == INTEGRATING_UNIT_NAME:
                    unit = matlab.tf([1], [t, 0])
                    need_new_choice = False
                else:
                    print(colorama.Fore.YELLOW + '\n Не реализовано')
            else:
                print(colorama.Fore.RED + '\n Пожалуйса, введите числовое значение!')
                need_new_choice = True
        elif unit_name == IDEAL_DIFFERENTIATING_UNIT_NAME:
            k = input('Введите коэффициент передачи звена (k): ')
            t = float(0.000001)
            if k.isdigit():
                k = int(k)
                t = float(0.000001)
                if unit_name == IDEAL_DIFFERENTIATING_UNIT_NAME:
                    unit = matlab.tf([k, 0], [t, 1])
                    need_new_choice = False
                else:
                    print(colorama.Fore.YELLOW + '\n Не реализовано')
            else:
                print(colorama.Fore.RED + '\n Пожалуйса, введите числовое значение!')
                need_new_choice = True
        elif unit_name == REAL_DIFFERENTIATING_UNIT_NAME:
            k = input('Введите коэффициент передачи звена (k): ')
            t = input('Введите постоянную времени звена (T): ')
            if k.isdigit() and t.isdigit():
                k = int(k)
                t = int(t)
                if unit_name == REAL_DIFFERENTIATING_UNIT_NAME:
                    unit = matlab.tf([k, 0], [t, 1])
                    need_new_choice = False
                else:
                    print(colorama.Fore.YELLOW + '\nНе реализовано')
            else:
                print(colorama.Fore.RED + '\n Пожалуйста, введите числовое значение!')
                need_new_choice = True
        else:
            print(colorama.Fore.YELLOW + '\n Недопустимое значение!')
    return unit
def graph(num, title, y, x):
    pyplot.subplot(3, 2, num)
    pyplot.grid(True)
    if title == 'Переходная характеристика':
        pyplot.plot(x, y, 'red')
    elif title == 'Импульсная характеристика':
        pyplot.plot(x, y, 'black')
    elif title == 'АЧХ':
        pyplot.plot(x, y, 'green')
    elif title == 'ФЧХ':
        pyplot.plot(x, y, 'yellow')
    elif title == 'АФХ':
        pyplot.plot(x, y, 'blue')
    elif title == 'ЛАЧХ':
        pyplot.plot(x, y, 'orange')
    pyplot.title(title)
    if title == 'Переходная характеристика' or title == 'Импульсная характеристика':
        pyplot.xlabel('Время, с')
    else:
        pyplot.xlabel('Омега, рад/с')
    pyplot.ylabel('Амплитуда')


unit_name = choice()
unit = get_unit(unit_name)
print(unit)

time_line = []
for i in range(0, 10000):
    time_line.append(i/1000)
ow_line = []
for i in range(0, 10000):
    ow_line.append(i/10)

[y, x] = matlab.step(unit, time_line)
graph(1, 'Переходная характеристика', y,x)
[y, x] = matlab.impulse(unit, time_line)
graph(2, 'Импульсная характеристика',y,x)
[y, x, z] = matlab.freqresp(unit, ow_line)
graph(3, 'АЧХ', y, z)
[y, x, z] = matlab.freqresp(unit, ow_line)
graph(4, 'ФЧХ', x, z)
graph(5, 'АФХ', 0, 0)
[y, x, z] = matlab.nyquist(unit, ow_line)
graph(6, '', 0,0)# костыль
pyplot.show()
[y, x, z] = matlab.bode(unit, ow_line)
graph(6, 'ЛАЧХ', y, ow_line)
pyplot.show()