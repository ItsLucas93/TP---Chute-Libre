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
frame3 = tkinter.Canvas(window)

CheckVar1 = IntVar()
CheckVar2 = IntVar()
CheckVar3 = IntVar()

vecteur = Checkbutton(frame1, text="Vecteur", variable=CheckVar1)
gravitation = Checkbutton(frame1, text="Gravitation", variable=CheckVar2)
simulation = Checkbutton(frame1, text="Simulation", variable=CheckVar3)
vecteur.grid(row=0, padx=5, pady=5)
gravitation.grid(row=0, column=1, padx=5, pady=5)
simulation.grid(row=0, column=2, padx=5, pady=5)

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
    graphique1 = Projectile(X_Euler_list, Z_Euler_list, tau)
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

    if CheckVar3.get() == 1:
        global window_simulation
        window_simulation = Tk()
        window_simulation.title('Simulation')
        window_simulation.configure(background='white')
        can = Canvas(window_simulation, width=720, height=480, background="black")
        simulation = Simulation(can, 50, 100)
        simulation.vitesse(v)
        simulation.orientation(alpha)
        simulation.lance()
        can.grid(row=2, column=6, columnspan=1, rowspan=10, sticky="N", padx=1, pady=1)
        Button(window_simulation, text='Simulation', command=simulation.lance).grid(row=5, column=3, columnspan=1, rowspan=1, padx=5, pady=5)
        a = ["Ball on the ground in ", str(t), " sec"]
        b = ["Coords \n x =", str(round(X_Euler_list[-1])), " m"]
        c = ["High max reach in z =", str(round(max(Z_Euler_list))), " m"]
        txt1 = Label(window_simulation, text="".join(a), bg="green", fg="white").grid(row=6, column=3, columnspan=1, rowspan=1, padx=5, pady=5)
        txt2 = Label(window_simulation, text="".join(b), bg="green", fg="white").grid(row=7, column=3, columnspan=1, rowspan=1, padx=5, pady=5)
        txt3 = Label(window_simulation, text="".join(c), bg="green", fg="white").grid(row=8, column=3, columnspan=1, rowspan=1, padx=5, pady=5)
        window_simulation.mainloop()

    bouton_start.config(state='disabled')


bouton_start.config(command=start)


class Projectile:
    def __init__(self, X_Euler_list, Z_Euler_list, tau):
        f = Figure(figsize=(3.5, 4), dpi=100)
        f.patch.set_color("#f0f0f0")
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
            f.patch.set_color("#f0f0f0")
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
            f.patch.set_color("#f0f0f0")
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
        f.patch.set_color("#f0f0f0")
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
            f.patch.set_color("#f0f0f0")
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
            f.patch.set_color("#f0f0f0")
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
        f.patch.set_color("#f0f0f0")
        fig = f.add_subplot(111)
        self.canvasx = FigureCanvasTkAgg(f, frame2)
        self.canvasx.get_tk_widget().grid(row=0, column=1, padx=5, pady=5)
        fig.set_xlabel('Temps')
        f.suptitle('Evolution x')
        fig.plot(time_list, X_Euler_list)

        f1 = Figure(figsize=(4, 3.5), dpi=100)
        f1.patch.set_color("#f0f0f0")
        fig1 = f1.add_subplot(111)
        self.canvasy = FigureCanvasTkAgg(f1, frame2)
        self.canvasy.get_tk_widget().grid(row=0, column=2, padx=5, pady=5)
        fig1.set_xlabel('Temps')
        f1.suptitle('Evolution z')
        fig1.plot(time_list, Z_Euler_list)

        f2 = Figure(figsize=(4, 3.5), dpi=100)
        f2.patch.set_color("#f0f0f0")
        fig2 = f2.add_subplot(111)
        self.canvasvx = FigureCanvasTkAgg(f2, frame2)
        self.canvasvx.get_tk_widget().grid(row=1, column=1, padx=5, pady=5)
        fig2.set_xlabel('Temps')
        f2.suptitle('Evolution vx')
        fig2.plot(time_list, vx_Euler_list)

        f3 = Figure(figsize=(4, 3.5), dpi=100)
        f3.patch.set_color("#f0f0f0")
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


class Simulation:
    def __init__(self, ref, x, y):
        self.ref = ref
        self.x1 = x
        self.y1 = y
        self.lbu = 10
        self.x2 = x + self.lbu
        self.y2 = y
        self.buse = ref.create_line(self.x1, self.y1, self.x2, self.y2, width=15)
        self.ob = ref.create_oval(x - 15, y - 15, x, y, fill='green')
        self.animation = False
        self.xMax = int(ref.cget('width'))
        self.yMax = int(ref.cget('height'))

    def orientation(self, angle):
        self.angle = (float(angle) * 2 * pi / 360)
        self.x2 = self.x1 + self.lbu * cos(self.angle)
        self.y2 = self.y1 - self.lbu * sin(self.angle)
        self.ref.coords(self.buse, self.x1, self.y1, self.x2, self.y2)

    def vitesse(self, v0):
        if v0 > 20:
            self.v = v0 * 0.2
        elif v0 > 10:
            self.v = v0 * 0.4
        else:
            self.v = v0 * 0.6

    def lance(self):
        if not self.animation:
            self.animation = True
            self.ref.coords(self.ob, self.x2 - 15, self.y2 - 15, self.x2, self.y2)
        v = self.v
        self.vy = -v * sin(self.angle)
        self.vx = v * cos(self.angle)
        self.animationob()

    def animationob(self):
        if self.animation:
            self.ref.move(self.ob, int(self.vx), int(self.vy))
        temp = tuple(self.ref.coords(self.ob))
        xo, yo = temp[0] + 3, temp[1] + 3
        if yo > self.yMax - 10 or xo > self.xMax - 10:
            self.animation = False
        else:
            self.vy += 0.2
            self.ref.after(30, self.animationob)


def reset():
    for i in range(len(all_gf)):
        gf = all_gf.pop()
        gf.destroygf()
        try:
            window_simulation.destroy()
        except:
            pass
    bouton_start.config(state='normal')


bouton_start.grid(row=4, column=0, padx=5, pady=5)
reset = tkinter.Button(frame1, text='Reset', command=reset).grid(row=4, column=1, padx=5, pady=5)
window.mainloop()
