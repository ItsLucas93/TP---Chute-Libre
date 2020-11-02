import tkinter.messagebox
from math import cos, sin, pi, tan
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *

window = Tk()
window.title('TP - Chute libre')
window.iconbitmap('chutelibre.ico')
window.configure(background='white')

frame1 = tkinter.Frame(window)
frame2 = tkinter.Frame(window)
frame3 = tkinter.Frame(window)

CheckVar1 = IntVar()
CheckVar2 = IntVar()

vecteur = Checkbutton(frame1, text="Vecteur", variable=CheckVar1)
gravitation = Checkbutton(frame1, text="Gravitation", variable=CheckVar2)
vecteur.grid(row=0, padx=5, pady=5)
gravitation.grid(row=0, column=1, padx=5, pady=5)

e1 = tkinter.Label(frame1, text='z0 en m:').grid(row=1)
valeurz0 = tkinter.StringVar()
entryz0 = tkinter.Entry(frame1, textvariable=valeurz0)
valeurz0.set(5)
entryz0.grid(row=1, column=1)

e2 = tkinter.Label(frame1, text='aplha en *:').grid(row=2)
valeuralpha = tkinter.StringVar()
entryalpha = tkinter.Entry(frame1, textvariable=valeuralpha)
valeuralpha.set(0)
entryalpha.grid(row=2, column=1, padx=5, pady=5)

e3 = tkinter.Label(frame1, text='v0 en m/s:').grid(row=3)
valeurvitesse = tkinter.StringVar()
entryvitesse = tkinter.Entry(frame1, textvariable=valeurvitesse)
valeurvitesse.set(0)
entryvitesse.grid(row=3, column=1, padx=5, pady=5)

frame1.grid(padx=5, pady=5)

all_gf = []
bouton_start = tkinter.Button(frame1, text='Start', width=10)


def start():
    g = 9.81
    v = int(valeurvitesse.get())
    alpha = int(valeuralpha.get())
    tau = 0.1
    x = 0
    z0 = int(valeurz0.get())
    z = z0
    t = 0
    vx = v * cos(alpha * pi / 180)
    vz = v * sin(alpha * pi / 180)
    tempx = x
    tempz = z
    vx_Euler_list = [vx]
    vz_Euler_list = [vz]
    X_Euler_list = [tempx]
    Z_Euler_list = [tempz]
    time_list = [t]

    while z >= 0:
        x = x + vx * tau
        z = z + vz * tau
        t = t + tau
        vx = vx
        vz = vz - g * tau
        tempx = v * cos(alpha * pi / 180) * t
        tempz = -0.5 * g * t * t + v * sin(alpha * pi / 180) * t + z0
        vx_Euler_list = vx_Euler_list + [vx]
        vz_Euler_list = vz_Euler_list + [vz]
        Z_Euler_list = Z_Euler_list + [tempz]
        X_Euler_list = X_Euler_list + [tempx]
        time_list = time_list + [t]
    graphique1 = projectile(X_Euler_list, Z_Euler_list, tau)
    all_gf.append(graphique1)

    if CheckVar1.get() == 1 and CheckVar2.get() == 1:
        graphique4 = flecheVecGrav(g, v, alpha, X_Euler_list, Z_Euler_list)
        all_gf.append(graphique4)
    else:
        if CheckVar1.get() == 1:
            graphique2 = flecheVec(g, v, alpha, X_Euler_list, Z_Euler_list)
            all_gf.append(graphique2)

        if CheckVar2.get() == 1:
            graphique3 = GravitationGraphique(X_Euler_list, Z_Euler_list)
            all_gf.append(graphique3)
    frame2.grid(row=1, padx=5, pady=5)

    graphique5 = evolution_xy(X_Euler_list, Z_Euler_list, time_list, vx_Euler_list, vz_Euler_list)
    all_gf.append(graphique5)
    bouton_start.config(state='disabled')


bouton_start.config(command=start)


class projectile:
    def __init__(self, X_Euler_list, Z_Euler_list, tau):
        f = Figure(figsize=(3.5, 4), dpi=100)
        fig = f.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(f, frame2)
        self.canvas.get_tk_widget().grid(pady=5)
        f.suptitle('Trajectoire du projectile')
        fig.scatter(X_Euler_list, Z_Euler_list, s=1)

    def destroygf(self):
        self.canvas.get_tk_widget().destroy()


class flecheVec:
    def __init__(self, g, v, alpha, x_Euler_list, z_Euler_list):
        if v <= 0:
            f = Figure(figsize=(3.5, 4), dpi=100)
            fig = f.add_subplot(111)
            self.canvas = FigureCanvasTkAgg(f, frame2)
            self.canvas.get_tk_widget().grid(row=1, padx=5)
            f.suptitle('Vecteurs')
            fig.scatter(x_Euler_list, z_Euler_list, s=1)
            fig.quiver(x_Euler_list[::-4], z_Euler_list[::-4], 0, -1, color='red')

        else:
            derive_Euler_list = []
            for x in x_Euler_list:
                derive = -(g / (v * v * cos(alpha * pi / 180) * cos(alpha * pi / 180))) * x + tan(alpha * pi / 180)
                derive_Euler_list = derive_Euler_list + [derive]
            f = Figure(figsize=(3.5, 4), dpi=100)
            fig = f.add_subplot(111)
            self.canvas = FigureCanvasTkAgg(f, frame2)
            self.canvas.get_tk_widget().grid(row=1, padx=5)
            f.suptitle('Vecteurs')
            fig.scatter(x_Euler_list, z_Euler_list, s=1)
            fig.quiver(x_Euler_list[::-4], z_Euler_list[::-4], 1, derive_Euler_list[::-4], color='red')

    def destroygf(self):
        self.canvas.get_tk_widget().destroy()


class GravitationGraphique:
    def __init__(self, x_Euler_list, z_Euler_list):
        f = Figure(figsize=(3.5, 4), dpi=100)
        fig = f.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(f, frame2)
        self.canvas.get_tk_widget().grid(row=1, padx=5)
        f.suptitle('Gravitation')
        fig.scatter(x_Euler_list, z_Euler_list, s=1)
        fig.quiver(x_Euler_list[::-4], z_Euler_list[::-4], 0, -1)

    def destroygf(self):
        self.canvas.get_tk_widget().destroy()


class flecheVecGrav:
    def __init__(self, g, v, alpha, x_Euler_list, z_Euler_list):
        if v <= 0:
            f = Figure(figsize=(3.5, 4), dpi=100)
            fig = f.add_subplot(111)
            self.canvas = FigureCanvasTkAgg(f, frame2)
            self.canvas.get_tk_widget().grid(row=1, padx=5)
            f.suptitle('Vecteur')
            fig.scatter(x_Euler_list, z_Euler_list, s=1)
            fig.quiver(x_Euler_list[::-4], z_Euler_list[::-4], 0, -1)
            fig.quiver(x_Euler_list[::-4], z_Euler_list[::-4], 0, -1, color='green')

        else:
            derive_Euler_list = []
            for x in x_Euler_list:
                derive = -(g / (v * v * cos(alpha * pi / 180) * cos(alpha * pi / 180))) * x + tan(alpha * pi / 180)
                derive_Euler_list = derive_Euler_list + [derive]
            f = Figure(figsize=(3.5, 4), dpi=100)
            fig = f.add_subplot(111)
            self.canvas = FigureCanvasTkAgg(f, frame2)
            self.canvas.get_tk_widget().grid(row=1, padx=5)
            f.suptitle('Vecteur et gravitation')
            fig.scatter(x_Euler_list, z_Euler_list, s=1)
            fig.quiver(x_Euler_list[::-4], z_Euler_list[::-4], 0, -1)
            fig.quiver(x_Euler_list[::-4], z_Euler_list[::-4], 1, derive_Euler_list[::-4], color='green')

    def destroygf(self):
        self.canvas.get_tk_widget().destroy()


class evolution_xy:
    def __init__(self, X_Euler_list, Z_Euler_list, time_list, vx_Euler_list, vz_Euler_list):
        f = Figure(figsize=(4, 3.5), dpi=100)
        fig = f.add_subplot(111)
        self.canvasx = FigureCanvasTkAgg(f, frame2)
        self.canvasx.get_tk_widget().grid(row=0, column=1, padx=5, pady=5)
        fig.set_xlabel('Temps')
        f.suptitle('Evolution x')
        fig.plot(time_list, X_Euler_list)

        f1 = Figure(figsize=(4, 3.5), dpi=100)
        fig1 = f1.add_subplot(111)
        self.canvasy = FigureCanvasTkAgg(f1, frame2)
        self.canvasy.get_tk_widget().grid(row=0, column=2, padx=5, pady=5)
        fig1.set_xlabel('Temps')
        f1.suptitle('Evolution z')
        fig1.plot(time_list, Z_Euler_list)

        f2 = Figure(figsize=(4, 3.5), dpi=100)
        fig2 = f2.add_subplot(111)
        self.canvasvx = FigureCanvasTkAgg(f2, frame2)
        self.canvasvx.get_tk_widget().grid(row=1, column=1, padx=5, pady=5)
        fig2.set_xlabel('Temps')
        f2.suptitle('Evolution vx')
        fig2.plot(time_list, vx_Euler_list)

        f3 = Figure(figsize=(4, 3.5), dpi=100)
        fig3 = f3.add_subplot(111)
        self.canvasvy = FigureCanvasTkAgg(f3, frame2)
        self.canvasvy.get_tk_widget().grid(row=1, column=2, padx=5, pady=5)
        fig3.set_xlabel('Temps')
        f3.suptitle('Evolution vy')
        fig3.plot(time_list, vz_Euler_list)

    def destroygf(self):
        self.canvasx.get_tk_widget().destroy()
        self.canvasy.get_tk_widget().destroy()
        self.canvasvx.get_tk_widget().destroy()
        self.canvasvy.get_tk_widget().destroy()


def reset():
    for i in range(len(all_gf)):
        gf = all_gf.pop()
        gf.destroygf()
    bouton_start.config(state='normal')


bouton_start.grid(row=4, column=0, padx=5, pady=5)
reset = tkinter.Button(frame1, text='Reset', command=reset).grid(row=4, column=1, padx=5, pady=5)
window.mainloop()