import time
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

dataLists = [[], [], []] 
selectedSensor = 0 

root = tk.Tk()
root.title("Aplicatie senzori Arduino")
root.geometry("800x600")
root.configure(bg='#acdfe6')

bg_image = Image.open('D:/practica/gui.jpg')
bg_image = bg_image.resize((800, 500), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

# create label with image
bg_label = tk.Label(root, image=bg_photo)
bg_label.pack(side='top',fill='y',expand=True)

plt.style.use('plotTheme')
fig = plt.figure()
ax = fig.add_subplot(111)
ax.grid(color='grey', linestyle='-', linewidth=0.5)

canvas = FigureCanvasTkAgg(fig, master=root)
frameButtons=tk.Frame(root,width=800, height=100,bg='#212946')
frameButtons.pack(side=tk.BOTTOM,fill='both',expand=True)

ser = serial.Serial('COM9', 9600)
time.sleep(2)

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
    global selectedSensor,canvas
    selectedSensor = 0
    bg_label.pack_forget()
    ax.clear()
    canvas.draw()
    canvas.get_tk_widget().pack(side='top',fill='y',expand=True)
    root.configure(bg='#212946')
def buttonFunctionGaz():
    global selectedSensor,canvas
    selectedSensor = 1
    bg_label.pack_forget()
    ax.clear()
    canvas.draw()
    canvas.get_tk_widget().pack(side='top',fill='y',expand=True)
    root.configure(bg='#212946')
def buttonFunctionLumina():
    global selectedSensor,canvas
    selectedSensor = 2
    bg_label.pack_forget()
    ax.clear()
    canvas.draw()
    canvas.get_tk_widget().pack(side='top',fill='y',expand=True)
    root.configure(bg='#212946')

sunet_image = Image.open('D:/practica/sunet.png').resize((40, 40), Image.Resampling.LANCZOS)
gaz_image = Image.open('D:/practica/gaz.png').resize((40, 40), Image.Resampling.LANCZOS)
lumina_image = Image.open('D:/practica/lumina.png').resize((40, 40), Image.Resampling.LANCZOS)

sunet_icon = ImageTk.PhotoImage(sunet_image)
gaz_icon = ImageTk.PhotoImage(gaz_image)
lumina_icon = ImageTk.PhotoImage(lumina_image)


button_sunet = tk.Button(frameButtons,height= 30, width=150,fg='black', relief=tk.RAISED, bg='#caf0f8', activebackground='#ef233c',activeforeground='black',image=sunet_icon,text="SUNET",font =('Verdana', 12,'bold'),compound=tk.LEFT, command=buttonFunctionSunet)
button_sunet.pack(side="left", padx=10, pady=10, expand=True)
button_sunet.bind("<Enter>", lambda e: button_sunet.config(fg='white', bg='#2a3459'))
button_sunet.bind("<Leave>", lambda e: button_sunet.config(fg='black', bg='#caf0f8'))

button_gaz = tk.Button(frameButtons,height= 30, width=150,fg='black', relief=tk.RAISED, bg='#caf0f8', activebackground='#ef233c',activeforeground='black',image=gaz_icon,text="GAZ",font =('Verdana', 12,'bold'),compound=tk.LEFT, command=buttonFunctionGaz)
button_gaz.pack(side="left", padx=10, pady=10, expand=True)
button_gaz.bind("<Enter>", lambda e: button_gaz.config(fg='white', bg='#2a3459'))
button_gaz.bind("<Leave>", lambda e: button_gaz.config(fg='black', bg='#caf0f8'))

button_lumina = tk.Button(frameButtons,height= 30, width=150,fg='black', relief=tk.RAISED, bg='#caf0f8', activebackground='#ef233c',activeforeground='black',image=lumina_icon,text="LUMINA",font =('Verdana', 12,'bold'),compound=tk.LEFT, command=buttonFunctionLumina)
button_lumina.pack(side="left", padx=10, pady=10, expand=True)
button_lumina.bind("<Enter>", lambda e: button_lumina.config(fg='white', bg='#2a3459'))
button_lumina.bind("<Leave>", lambda e: button_lumina.config(fg='black', bg='#caf0f8'))

ani = animation.FuncAnimation(fig, animate, fargs=(ser,), interval=10)
root.mainloop()