import time
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from tkinter import *
from PIL import Image, ImageTk

dataLists = [[], [], []] 
selectedSensor = 0  

import tkinter as tk
from tkinter.messagebox import showinfo


def animate(i, ser):
    global dataLists, selectedSensor  


    ser.write(bytes(str(selectedSensor) + ";\n", 'ascii'))
    arduinoData = ser.readline().decode('ascii').rstrip('\r\n')
    try:
        values = arduinoData.split(';')
        sensorValue1 = float(values[0])
        sensorValue2 = float(values[1])
        sensorValue3 = float(values[2])

        if selectedSensor == 0:
            dataLists[0].append(sensorValue1)
            dataLists[1].append(0)  
            dataLists[2].append(0)
        elif selectedSensor == 1:
            dataLists[0].append(0)
            dataLists[1].append(sensorValue2)
            dataLists[2].append(0)
        elif selectedSensor == 2:
            dataLists[0].append(0)
            dataLists[1].append(0)
            dataLists[2].append(sensorValue3)
    except (IndexError, ValueError):
        print("Eroare la citirea valorilor:", arduinoData)
    
        dataLists = [l[-50:] for l in dataLists]

   
    ax.clear()
    ax.set_ylim([0, 1200])

    y = dataLists[selectedSensor][-50:]
    colors = []
    for val in y:
        if val <= 400:
            colors.append('green')
        elif val <= 800:
            colors.append('yellow')
        else:
            colors.append('red')

    x = np.arange(len(y))
    for j in range(len(y)-1):
        if colors[j] != colors[j+1]:
            ax.plot(x[j:j+2], y[j:j+2], color=colors[j], linewidth=2)
        else:
            ax.plot(x[j:j+2], y[j:j+2], color=colors[j], linewidth=2)

    sensor = ''
    if selectedSensor == 0 :
        sensor="Sunet"
    if selectedSensor == 1 :
        sensor="Gaz"
    if selectedSensor == 2:
        sensor="Lumina"

    ax.set_title(f'Sensor {sensor} Data')
    ax.set_ylabel('Value')

def buttonFunctionSunet():
    global selectedSensor 
    selectedSensor = 0
def buttonFunctionGaz():
    global selectedSensor 
    selectedSensor = 1 
def buttonFunctionLumina():
    global selectedSensor 
    selectedSensor = 2 


plt.style.use('plotTheme')

fig = plt.figure()
ax = fig.add_subplot(111)
ax.grid(color='grey', linestyle='-', linewidth=0.5)
ser = serial.Serial('COM9', 9600)
time.sleep(2)

ani = animation.FuncAnimation(fig, animate, fargs=(ser,), interval=10)

sunet_image = Image.open('D:/practica/sunet.png').resize((40, 40), Image.ANTIALIAS)
gaz_image = Image.open('D:/practica/gaz.png').resize((40, 40), Image.ANTIALIAS)
lumina_image = Image.open('D:/practica/lumina.png').resize((40, 40), Image.ANTIALIAS)

sunet_icon = ImageTk.PhotoImage(sunet_image)
gaz_icon = ImageTk.PhotoImage(gaz_image)
lumina_icon = ImageTk.PhotoImage(lumina_image)


button_sunet = tk.Button(height= 30, width=150,fg='black', relief=tk.RAISED, bg='#caf0f8', activebackground='#ef233c',activeforeground='black',image=sunet_icon,text="SUNET",font =('Verdana', 12,'bold'),compound=LEFT, command=buttonFunctionSunet)
button_sunet.pack(side=tk.LEFT,anchor=tk.CENTER,fill=tk.X, expand=True)
button_sunet.bind("<Enter>", lambda e: button_sunet.config(fg='white', bg='#2a3459'))
button_sunet.bind("<Leave>", lambda e: button_sunet.config(fg='black', bg='#caf0f8'))

button_gaz = tk.Button(height= 30, width=150,fg='black', relief=tk.RAISED, bg='#caf0f8', activebackground='#ef233c',activeforeground='black',image=gaz_icon,text="GAZ",font =('Verdana', 12,'bold'),compound=LEFT, command=buttonFunctionGaz)
button_gaz.pack(side=tk.LEFT,anchor=tk.CENTER,fill=tk.X, expand=True)
button_gaz.bind("<Enter>", lambda e: button_gaz.config(fg='white', bg='#2a3459'))
button_gaz.bind("<Leave>", lambda e: button_gaz.config(fg='black', bg='#caf0f8'))

button_lumina = tk.Button(height= 30, width=150,fg='black', relief=tk.RAISED, bg='#caf0f8', activebackground='#ef233c',activeforeground='black',image=lumina_icon,text="LUMINA",font =('Verdana', 12,'bold'),compound=LEFT, command=buttonFunctionLumina)
button_lumina.pack(side=tk.LEFT,anchor=tk.CENTER,fill=tk.X, expand=True)
button_lumina.bind("<Enter>", lambda e: button_lumina.config(fg='white', bg='#2a3459'))
button_lumina.bind("<Leave>", lambda e: button_lumina.config(fg='black', bg='#caf0f8'))


plt.show()
ser.close()


