#!python2.7
#ver. 2
from Tkinter import *
import base64
import ttk
import os
import sys
import time
from datetime import datetime

class Aplicacion:

    def __init__(self):
        self.horamax = 5
        self.minumax = 59
        self.sec = 00
        self.minu = 0
        self.horas = 0
        self.now = ""
        self.flag = True

        self.h = 240
        self.w = 220
        
        self.window = Tk()
        self.window.geometry('{}x{}+550+230'.format(self.h, self.w))
        self.window.minsize(self.h, self.w)
        self.window.maxsize(int(self.h*1.2), int(self.w*1.2))

        self.window.title('SleepScript')
        self.window.iconbitmap('img/icono.ico')

        #self.img = PhotoImage(file='img/ScreenSaver.gif')  #height: 768px width: 1364px
        
        style = ttk.Style()
        style.configure("BW.TLabel", foreground="black", background="#F0F0F0")

        self.lHora = ttk.Label(text="Hora: ", style="BW.TLabel")
        self.lHora.pack(pady=5)

        self.sHora = Spinbox(self.window,from_=0, to=self.horamax)
        self.sHora.pack(pady=0)


        self.lMin = ttk.Label(text="Minutos: ", style="BW.TLabel")
        self.lMin.pack(pady=5)

        self.sMin = Spinbox(self.window, from_=1, to=self.minumax)
        self.sMin.pack()

        self.btnQuit = ttk.Button(self.window, text='Salir', command=self.quit)
        #self.btnQuit.pack(side=BOTTOM)
        self.btnQuit.place(x = self.h/2 - 81,y = 187)

        self.btnSS = ttk.Button(self.window, text='ScreenSaver', command=self.screenSaver)
        #self.btnSS.pack(side=BOTTOM)
        self.btnSS.place(x = self.h/2,y = 187)

        self.btnAnular = ttk.Button(self.window, text='Anular', command=self.anular)
        #self.btnLoad.pack(side=BOTTOM)
        self.btnAnular.place(x = self.h/2 - 81,y = 162)

        self.btnLoad = ttk.Button(self.window, text='Programar', command=self.load)
        #self.btnLoad.pack(side=BOTTOM)
        self.btnLoad.place(x = self.h/2,y = 162)
        
        self.msg = ttk.Label(text="", style="BW.TLabel")
        self.msg.pack(side=TOP, pady=15)

    def quit(self):
        sys.exit()

    def loop(self):
        self.window.mainloop()

    def update_clock(self):
        #self.msg.configure(text="Se apagara en: {}.".format(self.now))
        self.timer()
        self.msg.configure(text="{}".format(self.now))
        if(self.flag):
            self.window.after(1000, self.update_clock)
        else:
            self.msg.config(text="Anulado.")

        self.msg.pack(side=TOP, pady=15)

    def update_ssclock(self):
        if(self.r.winfo_exists()):
            self.msg1.configure(text="{}".format(self.msg['text']))
            self.window.after(1000, self.update_ssclock)
            self.msg1.place(x=650, y=300)

    def screenSaver(self):
        #print("imagen negra full")
        
        self.r = Toplevel()
        self.r.title("Screen Saver")
        self.r.iconbitmap('img/icono.ico')
        #self.r.state('zoomed')
        self.r.attributes('-fullscreen',True)
        self.r.configure(bg='#000000')
        self.r.focus()

        self.r.bind('<Key>', self.test)
        self.r.bind('<Button-1>', self.test)

        self.msg1 = Label(self.r, text="" ,bg ='#000000', fg='#444444')
        self.msg2 = Label(self.r, text="Toque cualquier tecla para cerrar." ,bg ='#000000', fg='#444444')

        if(not self.flag):
            self.msg1.configure(text="No se ha programado el apagado.")

        self.msg1.place(x=562, y=300)
        self.msg2.place(x=562, y=300+21)

        self.r.after(1500, self.update_ssclock)
        
        self.r.after(1500, self.anon)

        self.r.mainloop()

    def anon(self):
        self.msg2.configure(text="")
        self.msg2.pack()


    def test(self,evet):
        self.r.destroy()

    def timer(self):
        #os.system('cls')
        #print("minu {}".format(self.minu))
        #print("sec {}".format(self.sec))
        #print("horas {}".format(self.horas))
        
        if(self.horas != 0 and self.minu == 0 and self.sec == 0):
            self.horas -= 1
            self.minu = 59
            self.sec = 59
        elif(self.minu == 0 and self.sec == 0):
            #self.horas -= 1
            self.minu = 59
            self.sec = 59
            #print("se apago")
        elif(self.sec != 0):
            self.sec -= 1
        else:
            self.sec = 59
            self.minu -= 1

        timer = "{}:{}:{}".format(self.horas, self.minu, self.sec)
        self.now = datetime.strptime(timer,'%H:%M:%S').time()
        #print(datetime.strptime(timer,'%H:%M:%S').time())

    def load(self):
        self.sec = 00
        self.flag = True
        self.horas = int(self.sHora.get())
        self.minu = int(self.sMin.get())
        self.verificarh(int(self.horas))
        self.verificarm(int(self.minu))

        self.cmd("{}".format((int(self.horas)*3600)+(int(self.minu)*60)))
        self.msg.config(text="")
        self.msg.pack(side=TOP, pady=15)
        self.update_clock()

    def anular(self):
        self.flag = False
        #print ("anulado")
        os.system("shutdown -a")
        self.msg.config(text="Se anulo.")
        self.msg.pack(side=TOP, pady=15)

    def verificarh(self, h):
        if h <= 0:
            self.horas=int("00")
        elif h >self.horamax:
            self.horas = int("0{}".format(self.horamax))

    def verificarm(self, m):
        if m < 0:
            self.minu = int("00")
        if m > 0 or m < 10:
            self.minu = int("0{}".format(str(m)))
        if m > self.minumax:
            self.minu = int("{}".format(self.minumax))

    def cmd(self, tiempo):
        self.comando = "shutdown -s -t "+tiempo
        os.system(str(self.comando))
        #print("apagando en {}".format(tiempo))


app = Aplicacion()

app.loop()