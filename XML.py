from tkinter import *
from tkinter import messagebox
import array as arr
from array import *

input_path = ''
input_path_bool = False
input_path_bco = ''
input_path_bco_bool = False
output_path = ''
output_path_bool = False

def clicked_input():
    input_path = txt1.get()
    input_path_bool = True
    messagebox.showinfo('Путь входного файла', input_path)

def clicked_input2():
    input_path_bco = txt2.get()
    input_path_bco_bool = True
    messagebox.showinfo('Путь входного файла БЦО', input_path_bco)

def clicked_output():
    output_path = txt3.get()
    output_path_bool = True
    messagebox.showinfo('Путь выходного файла', output_path)

def clicked_ready():
    input_path = txt1.get()
    output_path = txt3.get()
    bco_path = txt2.get()
    d = {'' : ''}
    inp = open(input_path, encoding='utf-8')
    bco = open(bco_path, encoding='utf-8')
    out = open(output_path, 'w', encoding='utf-8')
    lines = inp.readlines()
    bco_lines = bco.readlines()
    st = 0
    en = 0
    numb = ''
    ass = []
    temp = []
    temp2 = []
    out.write("""KE_EXPORT version="1.0">
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
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if lines[i][j] == ';':
                en = j
                ass.append(lines[i][st:en])
                st = en + 2
        st = 0
        en = 0
    for i in range(0, len(ass) - 4, 4):
        for j in range(len(ass[i + 1])):
            if ass[i + 1][j] == ':':
                en = j
                temp.append(ass[i + 1][st:en])
                st = 0
                en = 0
        for j in range(len(ass[i+2])):
            if ass[i + 2][j] == ':':
                en = j
                temp.append(ass[i + 2][st:en])
                st = 0
                en = 0
        out.write("""
                <row>
                    <columns>
                        <column name="Number PU" value=""" + '"' + ass[i] + """" />
                        <column name="ID Connection" value="1" />
                        <column name="From" value=""" + '"' + ass[i+1] + """" numberOfRelatedProduct="0" />
                        <column name="To" value=""" + '"' + ass[i+2] + """" numberOfRelatedProduct="0" />
                        <column name="NumberCord" value=""" + '"' + ass[i+3] + """" />
                        <column name="LengthWire" value="0.100" />
                    </columns>
                </row>""")
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
    for x in temp:
        if x not in temp2:
            temp2.append(x)
    for i in range(len(bco_lines)):
        for j in range(len(bco_lines[j])):
            if bco_lines[i][j] == ';':
                en = j
                d1 = bco_lines[i][st:en]
                leng = len(bco_lines[j])
                d2 = bco_lines[i][en + 2:leng - 2]
                d[d1] = d2
                st = 0
                en = 0
    for i in range(len(temp2)):
        if temp2[i]:
            out.write(
                """<row>
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
    messagebox.showinfo('Готово', 'Файл готов, конвертируйте его в формат .xml')

window = Tk()
window.geometry('1000x400')
window.title("Создание XML файла")
lbl1 = Label(window, text = "Путь к вводному файлу")
lbl1.grid(column = 0, row = 0)
txt1 = Entry(window, width = 100)
txt1.grid(column = 1, row = 0)
btn1 = Button(window,text = "Принять", command = clicked_input)
btn1.grid(column = 2, row = 0)

lbl2 = Label(window, text = "Путь к вводному файлу БЦО")
lbl2.grid(column = 0, row = 1)
txt2 = Entry(window, width = 100)
txt2.grid(column = 1, row = 1)
btn2 = Button(window,text = "Принять", command = clicked_input2)
btn2.grid(column = 2, row = 1)

lbl3 = Label(window, text = "Путь к выходному файлу")
lbl3.grid(column = 0, row = 2)
txt3 = Entry(window, width = 100)
txt3.grid(column = 1, row = 2)
btn3 = Button(window,text = "Принять", command = clicked_output)
btn3.grid(column = 2, row = 2)

btn4 = Button(window,text = "Готово", command = clicked_ready)
btn4.grid(column = 1, row = 4)


window.mainloop()