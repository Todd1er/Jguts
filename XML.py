from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import Checkbutton
from tkinter import ttk
import array as arr
from array import *

error_to_catch = getattr(__builtins__,'FileNotFoundError', IOError) #две ошибки по цене одной

def cables_gen(ass,cable): #генерация cable.ini
    text = """<Root kd="1.2" kr="3.5" include="1" dopm="1" dopmData="0.1" dopp="1" m="0" pData="5" mData="" color="0" Path3DModel="" LineEnter="1"><Chains>"""
    for i in range(0, len(ass) - 8, 4):
        text += "<Chain Name=" + '"' + ass[i] + '"' + "/>"
        print(ass[i])
    text += "</Chains></Root>"
    cable.write(text)

def count(ass,help): #генерация help.txt
                     #не дописывает последний жгут в списке, вроде не сильная проблема, так как он последний,но TO FIX!
    help.write(ass[3] + " - " + ass[0])
    for i in range(0, len(ass) - 8, 4):
        j = i + 4
        if int(ass[i+3][-1]) < int(ass[j+3][-1]):
            help.write(":" + ass[i] + "\n" + ass[j+3] + " - " + ass[j])

def bubble(ass): #пузыревка (соединений вряд ли будет больше нескольких тысяч, так что так проще)
                 #сортирую по значению последней цифры в списке жгута, может быть проблема, TO FIX!
    swap = TRUE
    while swap:
        swap = FALSE
        for i in range(0, len(ass) - 8, 4):
            j = i + 4
            if int(ass[i+3][-1]) > int(ass[j+3][-1]):
                buff = [ass[i], ass[i+1], ass[i+2], ass[i+3]]
                ass[i] = ass[j]
                ass[i+1] = ass[j+1]
                ass[i+2] = ass[j+2]
                ass[i+3] = ass[j+3]
                ass[j] = buff[0]
                ass[j+1] = buff[1]
                ass[j+2] = buff[2]
                ass[j+3] = buff[3]
                swap = TRUE

def print_ending(out): #Можно будет объеденить с остальными дефолт принтами (но на производительность не влияет)
    out.write("""
                </rows>
            </table>   
        </tables>
    </KE_EXPORT>
                        """)

def print_middle(out): #Можно будет объеденить с остальными дефолт принтами (но на производительность не влияет)
    out.write("""
                    </rows>
                </table>
                <table name="Lugs">
                    <rows />
                </table>
                <table name="Others">
                    <rows />
                </table>
                <table name="Apparatus">
                    <rows>
                        """)

def print_connect(out, a, b, c, d): #Принт коннектов
        out.write("""
                            <row>
                                <columns>
                                    <column name="Number PU" value=""" + '"' + a + """" />
                                    <column name="ID Connection" value="1" />
                                    <column name="From" value=""" + '"' + b + """" numberOfRelatedProduct="0" />
                                    <column name="To" value=""" + '"' + c + """" numberOfRelatedProduct="0" />
                                    <column name="NumberCord" value=""" + '"' + d + """" />
                                    <column name="LengthWire" value="0.100" />
                                </columns>
                            </row>""")

def print_start(out): #Можно будет объеденить с остальными дефолт принтами (но на производительность не влияет)
    out.write("""<KE_EXPORT version="1.0">
            <tables>
                <table name="Boxes">
                    <rows>
                        <row>
                            <columns>
                                <column name="ID_Box" value="1" />
                                <column name="Alias" value="Оболочка" />
                                <column name="Group" value="" />
                                <column name="Name" value="" />
                                <column name="GOST" value="" />
                                <column name="DocumentName" value="" />
                                <column name="DocumentFormat" value="" />
                                <column name="Type" value="Сборочные единицы" />
                                <column name="Path3DModel" value="" />
                            </columns>
                        </row>
                    </rows>
                </table>
                <table name="Surfaces">
                    <rows>
                        <row>
                            <columns>
                                <column name="ID_Surf" value="1" />
                                <column name="ID_Box" value="1" />
                                <column name="Alias" value="Поверхность" />
                                <column name="Group" value="" />
                                <column name="Name" value="" />
                                <column name="GOST" value="" />
                                <column name="DocumentName" value="" />
                                <column name="DocumentFormat" value="" />
                                <column name="Type" value="Сборочные единицы" />
                                <column name="Path3DModel" value="" />
                                <column name="xPoint" value="" />
                                <column name="yPoint" value="" />
                            </columns>
                        </row>
                    </rows>
                </table>
                <table name="Connections">
                    <rows>""")

def chk_click(): #Функция чекбоксов
    if chk_state.get() == 0:
        txt2.config(state=DISABLED)
        btn2.config(state=DISABLED)
    else:
        txt2.config(state=NORMAL)
        btn2.config(state=NORMAL)

    if chk_state_cable.get() == 0:
        txt3.config(state=DISABLED)
        btn3.config(state=DISABLED)
    else:
        txt3.config(state=NORMAL)
        btn3.config(state=NORMAL)

    if chk_state_sort.get() == 0:
        txt4.config(state=DISABLED)
    else:
        txt4.config(state=NORMAL)

def clicked_input(): #Обзор файла ввода
    file = filedialog.askopenfilename(filetypes = (("Текстовый файл","*.txt"),))
    txt1.delete(0, END)
    txt1.insert(0, file)

def clicked_input2(): #Обзор файла БЦО
    file = filedialog.askopenfilename(filetypes=(("Текстовый файл", "*.txt"),))
    txt2.delete(0, END)
    txt2.insert(0, file)

def clicked_input3(): #Обзор файла Calbe.ini
    file = filedialog.askopenfilename(filetypes=(("Файл Cable3D.ini", "*.ini"),))
    txt3.delete(0, END)
    txt3.insert(0, file)

def clicked_ready(): #Основная функция

    input_path = txt1.get() #Путь беру из текстового вводного поля.
    if chk_state.get == 1: #Если включено БЦО
        bco_path = txt2.get()
    if chk_state_cable.get == 1: #Если включен CABLE.ini
        cable_path = txt3.get()

    d = {'' : ''} #Инициализация словаря

    #Ловлю ошибки в вводе пути
    try:
        inp = open(input_path, encoding='utf-8')
    except error_to_catch:
        messagebox.showinfo('Ошибка', 'Неверный путь к файлу ввода.')
        inp.close()
        return 0
    if chk_state.get == 1:  # Если включено БЦО
        try:
            bco = open(bco_path, encoding='utf-8')
        except error_to_catch:
            messagebox.showinfo('Ошибка', 'Неверный путь к файлу БЦО.')
            bco.close()
            return 0

    if chk_state_cable == 1:
        try:
            cable = open(cable_path, 'r+', encoding='utf-8')
        except error_to_catch:
            messagebox.showinfo('Ошибка', 'Неверный путь к файлу cable3D.ini')
            cable.close()
            return 0

    out_path = filedialog.asksaveasfilename(title="Сохранить файл", defaultextension=".xml",
                                            filetypes=(("XML файл", "*.xml"),)) #Сохраняю путь вывода
    out = open(out_path, 'w', encoding='utf-8') #Открываю путь

    if chk_state_sort.get() == 0: #Если один жгут, то в файле help нет смысла
        help_path = filedialog.asksaveasfilename(title="Сохранить файл справки", defaultextension=".txt",
                                                filetypes=(("TXT файл", "*.txt"),)) #Сохраняю путь help
        help = open(help_path, 'w', encoding='utf-8')

    lines = inp.readlines() #Читаем все линии
    #Проверяю на пустые файлы
    if len(lines) < 1:
        messagebox.showinfo('Ошибка', 'Пустой файл ввода.')
        inp.close()
        out.close()
        bco.close()
        return 0
    if chk_state.get() == 1: #Если включен файл БЦО
        bco_lines = bco.readlines()
        if len(bco_lines) < 1:
            messagebox.showinfo('Ошибка', 'Пустой файл БЦО.')
            inp.close()
            out.close()
            bco.close()
            return 0

    #Инициализация переменных/массивов
    st = 0
    ass = []
    temp = []
    temp2 = []

    print_start(out) #Начало принта

    for i in range(len(lines)): #В массиве строк
        for j in range(len(lines[i])): #В строке
            #Добавляю в основной массив все что между ; по порядку, тогда каждая строка занимает 4 ячейки в массиве
            #Тогда однотипные данные в одной и той же клетке по делимости на 4 (i%4 +0 +1 +2 +3)
            if lines[i][j] == ';':
                en = j
                ass.append(lines[i][st:en])
                st = en + 2
        st = 0

    #Если спецификация по нашим правилам, то эту функцию можно будет убрать
    for i in range(0, len(ass) - 4, 4): #Прохожу основной массив с шагом в 4
        #Заменяю все - на _
        for j in range(len(ass[i+1])):
            if ass[i + 1][j] == '-':
                ass[i + 1] = ass[i+1][:j] + '_' + ass[i+1][j+1:]
        for j in range(len(ass[i+2])):
            if ass[i + 2][j] == '-':
                ass[i + 2] = ass[i+2][:j] + '_' + ass[i+2][j+1:]

    if chk_state_cable.get == 1: #Если включен Cable.ini
        cable.truncate(0) #Очищаю изначальный Cable.ini
        cables_gen(ass, cable) #Генерация Cable.ini
    bubble(ass) #Пузыревка
    if chk_state_sort.get == 0: #Если один жгут, то в файле help нет смысла
        count(ass, help)


    for i in range(0, len(ass) - 4, 4):
        #Добавление всех БЦО в массив temp
        for j in range(len(ass[i + 1])):
            if ass[i + 1][j] == ':':
                en = j
                temp.append(ass[i + 1][st:en])
                st = 0

        for j in range(len(ass[i+2])):
            if ass[i + 2][j] == ':':
                en = j
                temp.append(ass[i + 2][st:en])
                st = 0
        #Генерация всех соединений
        if chk_state_sort.get() == 1:
            if txt4.get() == ass[i+3]:
                print_connect(out, ass[i], ass[i+1], ass[i+2], ass[i+3])
        else:
            print_connect(out, ass[i], ass[i+1], ass[i+2], ass[i+3])

    print_middle(out) #Печать середины

    #Убираю повторные БЦО
    for x in temp: #Перебор всех БЦО
        if x not in temp2: #Если нет в temp2, то добавляем. В temp2 уникальные значения
            temp2.append(x)

    if chk_state.get() == 1: #Если используем файлы БЦО
        for i in range(len(bco_lines)):
            for j in range(len(bco_lines[i])):
                if bco_lines[i][j] == ';':
                    en = j
                    d1 = bco_lines[i][st:en]
                    leng = len(bco_lines[i])
                    d2 = bco_lines[i][en + 2:leng - 2]
                    d[d1] = d2
                    st = 0

    #Наверное можно спихнуть в одну функцию, TO FIX!
    if chk_state.get() == 1: #Если используем файлы БЦО
        for i in range(len(temp2)):
            if temp2[i]:
                out.write(
                    """ <row>
                            <columns>
                                <column name="BCO apparatus" value=""" + '"' + temp2[i] + """" />
                                <column name="ID_Surf" value="1" />
                                <column name="ID_Box" value="1" />
                                <column name="Group" value="Элемент" />
                                <column name="Name" value="Компонент" />
                                <column name="GOST" value="" />
                                <column name="DocumentName" value="" />
                                <column name="DocumentFormat" value="" />
                                <column name="Type" value="Прочие изделия" />
                                <column name="Flag isRelatedProduct" value="0" />
                                <column name="POLINOM_ID" value="" />
                                <column name="Path3DModel" value=""" + '"' + d[temp2[i]] + """" />
                                <column name="xPoint" value="" />
                                <column name="yPoint" value="" />
                            </columns>
                        </row>
                    """)
    else:
        for i in range(len(temp2)):
            if temp2[i]:
                out.write(
                    """ <row>
                            <columns>
                                <column name="BCO apparatus" value=""" + '"' + temp2[i] + """" />
                                <column name="ID_Surf" value="1" />
                                <column name="ID_Box" value="1" />
                                <column name="Group" value="Элемент" />
                                <column name="Name" value="Компонент" />
                                <column name="GOST" value="" />
                                <column name="DocumentName" value="" />
                                <column name="DocumentFormat" value="" />
                                <column name="Type" value="Прочие изделия" />
                                <column name="Flag isRelatedProduct" value="0" />
                                <column name="POLINOM_ID" value="" />
                                <column name="Path3DModel" value="" />
                                <column name="xPoint" value="" />
                                <column name="yPoint" value="" />
                            </columns>
                        </row>
                    """)

    print_ending(out) #Принт конца

    #Закрытие файлов
    out.close()
    inp.close()
    if chk_state.get() == 1:  # Если используем файлы БЦО
        bco.close()
    messagebox.showinfo('Готово', 'Файл успешно сохранен.')

window = Tk()
window.geometry('1000x400') #Размер окна
window.title("Создание XML файла")

#Первая строчка
lbl1 = Label(window, text = "Таблица соединений")
lbl1.grid(column = 0, row = 0)
txt1 = Entry(window, width = 100)
txt1.grid(column = 1, row = 0)
btn1 = Button(window,text = "Обзор", command = clicked_input)
btn1.grid(column = 2, row = 0)

#Вторая строчка
lbl2 = Label(window, text = "Обозначения БЦО")
lbl2.grid(column = 0, row = 1)
txt2 = Entry(window, width = 100)
txt2.grid(column = 1, row = 1)
btn2 = Button(window,text = "Обзор", command = clicked_input2)
btn2.grid(column = 2, row = 1)

#Третья строчка
lbl3 = Label(window, text = "Файл Cable3D.ini")
lbl3.grid(column = 0, row = 2)
txt3 = Entry(window, width = 100)
txt3.grid(column = 1, row = 2)
btn3 = Button(window,text = "Обзор", command = clicked_input3)
btn3.grid(column = 2, row = 2)

#Четвертая строчка
lbl4 = Label(window, text = "БЦО жгута")
lbl4.grid(column = 0, row = 3)
txt4 = Entry(window, width = 100, state=DISABLED)
txt4.grid(column = 1, row = 3)

#Галочки
chk_state = IntVar()
chk_state.set(1)
chk = Checkbutton(window, text='Использовать список БЦО', var=chk_state, command=chk_click)
chk.grid(column=3, row=1)

chk_state_cable = IntVar()
chk_state_cable.set(1)
chk_cable = Checkbutton(window, text='Создавать файл Cable3D.ini', var=chk_state_cable, command=chk_click)
chk_cable.grid(column=3, row=2)

chk_state_sort = IntVar()
chk_state_sort.set(0)
chk_sort = Checkbutton(window, text='Файл для отдельного жгута', var=chk_state_sort, command=chk_click)
chk_sort.grid(column=3, row=3)

#Кнопка готово
btn4 = Button(window,text = "Готово", command = clicked_ready)
btn4.grid(column = 1, row = 4)

window.mainloop()
