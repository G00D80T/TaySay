import control
import matplotlib.pyplot as pyplot
import numpy as np

ispolnitel = control.tf([23], [8, 1])
turbine = control.tf([2], [4, 1])
generator = control.tf([1], [10, 1])
obrat_sv = control.tf([6, 0], [1, 1])
print(ispolnitel, turbine, generator, obrat_sv)
poln_function = (ispolnitel * turbine * generator) / (1 + ispolnitel * turbine * generator * obrat_sv)  # Замкнутая САУ
vnut_function= ispolnitel * turbine * generator * obrat_sv  # Замкнутая САУ в разомкнутом состоянии


# print(vnut_function, poln_function)


def Perehod(func):
    time = []
    for i in range(0, 1000000):
        time.append(i / 100)
    [x, y] = control.step_response(func, time)
    pyplot.plot(x, y)
    pyplot.grid(True)
    pyplot.title('Переходная характеристика')
    pyplot.xlabel('Time, с')
    pyplot.ylabel('Амплитуда')
    pyplot.xlim(-1, 10000)
    pyplot.ylim(-100, 200)
    pyplot.show()


def Polus(func):
    pyplot.grid(True)
    control.pzmap(func)
    pyplot.title('Полюсы и нули функции')
    pyplot.xlabel('Re')
    pyplot.ylabel('I(')
    pyplot.show()


def critGurvits(func):
    (num, den) = control.tfdata(func)
    denA = den[0][0]
    gurvit = []
    # Создаю матрицу
    for i in range(len(denA) - 1):
        gurvit.append([])
        for j in range(len(denA) - 1):
            index = (j * 2) + 1 - i
            if (index > (len(denA) - 1)) or (index < 0):
                gurvit[i].append(0)
            else:
                gurvit[i].append(denA[index])
    # Ищу определители
    det = []
    while (len(gurvit) > 0):
        det.append(np.linalg.det(gurvit))
        for i in range(len(gurvit) - 1):
            gurvit[i].pop(len(gurvit) - 1)
        gurvit.pop(len(gurvit) - 1)
    # Проверяю устойчивость
    count = int(0)
    for i in range(len(det)):
        if det[i] > 0:
            count = count + 1
    if (count == len(det)):
        print('Система устойчива!')
        return True
    else:
        print('Система не устойчива!')
        return False


def critRaus(func):
    (num, den) = control.tfdata(func)
    den_arr = den[0][0]
    # Создаю матрицу
    raus_column = []
    Rij = []
    for i in range(len(den_arr)):
        raus_column.append([])
        if (i <= 1):
            Rij.append(0)
            for j in range(len(den_arr)):
                index_raus = (2 * j) + i
                if (index_raus >= (len(den_arr)) or (index_raus < 0)):
                    raus_column[i].append(0)
                else:
                    raus_column[i].append(den_arr[index_raus])
        else:
            Rij.append((raus_column[i - 2][0]) / (raus_column[i - 1][0]))
            for j in range(len(den_arr)):
                if (j > len(den_arr) - 2):
                    raus_column[i].append(0)
                else:
                    raus_column[i].append(raus_column[i - 2][j + 1] - Rij[i] * raus_column[i - 1][j + 1])
    # Выделяем первый столбец Рауса
    one_column = []
    for i in range(len(raus_column)):
        one_column.append(raus_column[i][0])
    # Проверим, что все элементы первого столбца положительные
    count = int(0)
    flag = False
    for i in range(len(one_column)):
        if (one_column[i] < 0):
            flag = True
            break
        else:
            if (one_column[i] > 0):
                count += 1
            else:
                count += 0
    # Проверяю устойчивость
    if (flag == True):
        print('Система не устойчива!')
    elif ((flag == False) and (count == len(one_column))):
        print('Система устойчива!')
    else:
        print('Система находится на границе устойчивости!')
    # print('Матрица Рауса: ', raus_column)


# Критерий Найквиста
def critNaiquist(func):
    control.nyquist(func)
    pyplot.grid(True)
    pyplot.title("Критерий Найквиста")
    pyplot.xlabel('Re')
    pyplot.ylabel('Im')
    pyplot.show()


def critMichailov(func):
    (num, den) = control.tfdata(func)
    den_arr = den[0][0]
    level = []
    for i in range(len(den[0][0])):
        level.insert(0, i)

    Um = []
    Ulev = []
    Vm = []
    Vlev = []
    if ((len(den[0][0]) - 1) % 2 == 0):
        for i in range(0, (len(den[0][0])), 2):
            Um.append(den_arr[i])
            Ulev.append(level[i])
            if i == (len(den[0][0]) - 1):
                Vm.append(0)
                Vlev.append(0)
            else:
                Vm.append(den_arr[i + 1])
                Vlev.append(level[i + 1])
    else:
        for i in range(0, (len(den[0][0]) - 1), 2):
            Vm.append(den_arr[i])
            Vlev.append(level[i])
            if i == (len(den[0][0]) - 1):
                Um.append(0)
                Ulev.append(0)
            else:
                Um.append(den_arr[i + 1])
                Ulev.append(level[i + 1])

    for i in range(len(Um)):
        if (Ulev[i] % 4 == 0):
            Um[i] = Um[i] * (1)
        else:
            Um[i] = Um[i] * (-1)
    for i in range(len(Vm)):
        if ((Vlev[i] - 1) % 4 == 0):
            Vm[i] = Vm[i] * (1)
        else:
            Vm[i] = Vm[i] * (-1)

    U_Mik = []
    V_Mik = []
    time = []
    for i in range(0, 10000):
        time.append(i / 10)
    # Расчет значений для графика
    for i in range(0, 10000):
        u = 0
        v = 0
        for j in range(len(Um)):
            u = u + (Um[j] * (time[i] ** Ulev[j]))
            v = v + (Vm[j] * (time[i] ** Vlev[j]))
        U_Mik.append(u)
        V_Mik.append(v)

    pyplot.plot(U_Mik, V_Mik)
    pyplot.grid(True)
    pyplot.title("Критерий Михайлова")
    pyplot.xlabel('Re')
    pyplot.ylabel('Im')
    pyplot.show()


# ЛАЧХ и ЛФЧХ
def Log_character(func):
    time = []
    for i in range(0, 1000000):
        time.append(i / 1000)
    control.bode(func, time)
    pyplot.grid(True)
    pyplot.show()


# Запас устойчивости логарифмическим функциям
def stability_margin_check():
    straight = ispolnitel * turbine * generator
    control.bode(straight, dB=True, deg=True, margins=True, color='black')
    gm, pm, wcg, wcp = control.margin(straight)
    print("Запас по амплитуде ", f'{gm:.2f}')
    print("Запас по амплитуде  ", f'{20 * np.log10(gm):.2f}', ", дБ")
    print("Частота wcp ", f'{wcp:.2f}', ", рад/с")
    print("Запас по фазе ", f'{pm:.2f}', ", град.")
    print("Частота wcg ", f'{wcg:.2f}', ", рад/с")
    pyplot.grid(True)
    pyplot.show()


# Определение коэффициента, при котором САУ находится на границе устойчивости
def stability_check_Gurvits():
    k = float(input("Задайте начальный коэффициент k: "))
    step = 0.1
    count = 0
    straight = ispolnitel * turbine * generator

    flag = True
    while (flag == True):
        nexus_feed_link_K = control.tf([k, 0], [1, 1])
        full = control.feedback(straight, nexus_feed_link_K)
        if (critGurvits(full) == False):
            k = k - step
        else:
            k = k + step
            step = step / 10
            count = count + 1
            if (count == 5):
                flag = False
    print("Коэффициент обратной связи, при котором САУ находится на границе устойчивости: ", k)
    # Вывод переходной характеристики
    nexus_feed_link_K = control.tf([k, 0], [1, 1])
    full = control.feedback(straight, nexus_feed_link_K)
    Perehod(full)


# D-разбиение
def d_stabil():
    denum_Str = [46, 0, 0]
    numerU = [-472, -23]
    numer_level_U = [4, 2]
    numerV = [-320, 174, -1]
    numer_level_V = [5, 3, 1]

    list_U = []
    list_V = []

    omega = []
    for i in range(-150, 150):
        omega.append(i / 1000)

    for i in range(len(omega)):
        valU = 0
        valV = 0
        for j in range(len(numerU)):
            valU = valU + (numerU[j] * (omega[i] ** numer_level_U[j])) / (
                    denum_Str[0] + denum_Str[1] * omega[i] * omega[i])
        list_U.append(valU)

        for k in range(len(numerV)):
            valV = valV + (numerV[k] * (omega[i] ** numer_level_V[k])) / (
                    denum_Str[0] + denum_Str[1] * omega[i] * omega[i])
        list_V.append(valV)

    pyplot.plot(list_U, list_V)
    pyplot.grid(True)
    pyplot.text(list_U[0], list_V[0], "w = - бесконечность")
    pyplot.text(list_U[len(list_U) - 1], list_V[len(list_V) - 1], "w = + бесконечность")
    markers = [0, 149, 299]
    pyplot.plot(list_U, list_V, '-bo', markevery=markers)
    pyplot.title("D - разбиение")
    pyplot.xlabel('Re')
    pyplot.ylabel('Im')
    pyplot.show()


critMichailov(poln_function)
critNaiquist(vnut_function)
critGurvits(poln_function)
critRaus(poln_function)
stability_margin_check()
d_stabil()
stability_check_Gurvits()