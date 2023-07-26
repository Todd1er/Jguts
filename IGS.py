import array as arr
from array import *
f = open(r'C:\Users\drnks\OneDrive\Desktop\inbut', encoding='utf-8') #Файл формата igs, скопированный в txt
s = open(r'C:\Users\drnks\OneDrive\Desktop\outbut', 'w', encoding='utf-8') #Файл вывода
lines = f.readlines() #Считываем строки
#переменные
st = 0 
en = 0
k = 0
p1 = 0
p2 = 0
p3 = 0

ass = ["" for x in range(1)] #общий массив
line = ["" for x in range(1)] #массив линий
arc = ["" for x in range(1)] #массив дуг

for i in range(6, len(lines)): #Создание общего массива всех элементов
        lines[i] = " ".join(lines[i].split())
        if lines[i][3] != " " and (lines[i][:3] != "314") and (lines[i][:3] != "402"):
                ass.append(lines[i]) 
lines.clear()

for i in range(1, len(ass)-1, 2): #Добавление разделителя, костыль
        lines.append(ass[i] + "]" + ass[i+1])

for i in range(len(lines)): #Разделение на дуги и прямые
                if (lines[i][:3] == "110"):
                        line.append(lines[i])
                if (lines[i][:3] == "100"):
                        arc.append(lines[i])
#парсинг координат линий
for i in range(len(line)):
        for j in range(len(line[i])-1):
                if line[i][j] + line[i][j+1] == ", ":
                        p1 = j
                if line[i][j] == ';':
                        p2 = j
                if line[i][j] == ']':
                        p3 = j
        line[i] = line[i][4:p1] + ',' + line[i][p3+1:p2]
#парсинг координат дуг
for i in range(len(arc)):
        for j in range(len(arc[i])-1):
                if arc[i][j] + arc[i][j+1] == ", ":
                        p1 = j
                if arc[i][j] == ';':
                        p2 = j
                if arc[i][j] == ']':
                        p3 = j
        arc[i] = arc[i][4:p1] + ',' + arc[i][p3+1:p2]
  
#печать вывода
s.write("LINES:\n")
for i in range(1, len(line)):
        s.write(str(i) + ":" + line[i] + ";\n") #str(i) + ":" +
s.write("ARCS:\n")
for i in range(1, len(arc)):
        s.write(str(i) + ":" + arc[i] + ";\n")


