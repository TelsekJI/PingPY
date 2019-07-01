import subprocess
import tkinter
from tkinter import *
from tkinter import messagebox
from datetime import datetime
from subprocess import CREATE_NO_WINDOW

LOG = open('ping.txt', 'w') # создаём лог файл
LOG.close()                 # в каталоге откуда запускается скрипт

HOSTNAME = "192.168.5.194"  # Имя или ip адрес хоста, который будем пинговать

FLAG_GOOD = True            # Начальные значения для флагов индикации изменения состояния хоста
FLAG_BAD = True

txt = HOSTNAME + " доступен."   # Начальное сообщение
bgc = "green"                   # Начальный цвет фона окна сообщения
fgc = "black"                   # Начальный цвет шрифта окна сообщения

###############################################################################################
# Функция pinging осуществляет проверку удалённого хоста путём посыла одного пинга. В каждом  #
# из возможных случаев она обновляет настройки окна и вызывает сама себя. Таким образом мы    #
# получаем бесконечный цикл, который завершается с закрытием окна.                            #
###############################################################################################
def pinging():
    global FLAG_GOOD, FLAG_BAD, txt, bgc, fgc
    LOG = open('ping.txt', 'a')
    response = subprocess.run(['ping', '-n', '1', HOSTNAME], creationflags = CREATE_NO_WINDOW,)
    now = datetime.now()
    if response.returncode == 0:
        if FLAG_GOOD:
            txt = HOSTNAME + " доступен."
            bgc = "green"
            LOG.write(HOSTNAME + ' is up! ' + str(now) + '\n')
            FLAG_GOOD = False
            FLAG_BAD = True
            lbl.config(text = txt, bg = bgc)
    else:
        if FLAG_BAD:
            txt = HOSTNAME + " недоступен."
            bgc = "red"
            LOG.write(HOSTNAME + ' is down! ' + str(now) + '\n')
            FLAG_BAD = False
            FLAG_GOOD = True
            lbl.config(text = txt, bg = bgc)
    root.after(5, pinging)
    LOG.close()
    
def destr():
    ent.destroy()

# Основная часть программы
ent = Tk()

message = StringVar()

L1 = Label(text = "Hostname")
L1.pack(side = LEFT)

message_entry = Entry(textvariable=message)
message_entry.pack(side = LEFT)

message_button = Button(text="Ok", command = destr)
message_button.pack(side = LEFT)

ent.mainloop()

HOSTNAME = str(message.get())

root = Tk()
lbl = Label(root, text = txt, width = 30, height = 5, bg = bgc, fg = fgc)
lbl.pack()
pinging()
root.mainloop()
