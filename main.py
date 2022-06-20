from tkinter.filedialog import askopenfilename

import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import FormatStrFormatter
import tkinter as tk
from PIL import ImageTk, Image
import numpy as np

ser = serial.Serial('COM3', 115200, timeout=3)

# create figure
figure = plt.figure(figsize=(5, 5), dpi=100)
figure.patch.set_edgecolor('royalblue')
figure.patch.set_linewidth(1)
f = figure.add_subplot(111)

x = []
y = []


def start_connection():
    ser.open()
    x.clear()
    y.clear()



def stop_connection():
    ser.close()


def animate(i):
    try:
        line = str(ser.readline())
        read_data = line[2:len(line) - 5].split(';')
        x.append(int(read_data[0]))
        y.append(float(read_data[1]))
        f.cla()
        f.plot(x, y)
        f.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        plt.xlabel("Czas [s]")
        plt.ylabel("pH")
        plt.title("Pomiar pH")
    except:
        nic = 1


ani = FuncAnimation(plt.gcf(), animate, interval=1000)

# interface
root = tk.Tk()
root.title("Jak pech to pH-metr")
root.configure(bg="#daedf4")


# logo
# image = Image.open("logo1.png")
# image = image.resize((350, 100))
# photo = ImageTk.PhotoImage(image, master=root)
# panel = tk.Label(root, image=photo)
# panel.configure(bg="#daedf4")
# panel.grid(row=0, column=0)
# chart = FigureCanvasTkAgg(figure, root)
# chart.get_tk_widget().grid(row=1, column=0, padx=25)

def save_file():
    file = askopenfilename(parent=root, title="Wybierz plik", filetypes=[("Text file", "*.txt")])

    maxPh = max(y)
    mean = np.mean(y)

    str1 = "czas[s];pH; max pH = "+str(maxPh) +"; mean pH = " + str(mean) + "\n"
    if file:
        file = open(file, "w")
        for index, elem in enumerate(x):
            line = str(elem) + ";" + str(y[index]) + "\n"
            str1 += line
        file.write(str1)
        file.close()


fr = tk.Frame(root)
fr.configure(bg="#daedf4")
fr.grid(row=2, column=0, padx=5, pady=5)

start_btn = tk.Button(fr, text="Start", command=lambda: start_connection(), font="Raleway", bg="#1f456e", fg="white",
                      height=1, width=10)

start_btn.grid(column=0, row=0, padx=2.5, pady=5)

stop_btn = tk.Button(fr, text="Stop", command=lambda: stop_connection(), font="Raleway", bg="#1f456e", fg="white",
                     height=1, width=10)

stop_btn.grid(column=1, row=0, padx=2.5, pady=5)

save_btn = tk.Button(fr, text="Zapisz", command=lambda: save_file(), font="Raleway", bg="#1f456e", fg="white", height=1,
                     width=10)

save_btn.grid(column=2, row=0, padx=2.5, pady=5)

plt.show()

root.mainloop()
