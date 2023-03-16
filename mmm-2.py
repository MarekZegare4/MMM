import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button

g = 9.89 #przyspieszenie grawitacyjne
T = 18 # okres
h = 0.001 #krok symulacji
precyzja =3 #zaokrąglanie wartości

zainicjalizowano = False

t = np.linspace(0, T, int(T/h))

fig, axs = plt.subplots(3)
fig.suptitle('Wykresy x(t) i y(t)')
fig.subplots_adjust(bottom=0.2)
fig.set_figwidth(12)
fig.set_figheight(10)

v0  =   100    #prędkość początkowa
m   =   2      #masa
b   =   0.3    #współczynnik liniowego oporu powietrza
fi  =   40     #kąt wystrzału (w stopniach)

opt_kat = 0

xmax= ymax= tmax= tc= float(0)

x = np.zeros(int(T/h))
x1p = np.zeros(int(T/h))
x2p =  np.zeros(int(T/h))
y = np.zeros(int(T/h))
y1p = np.zeros(int(T/h))
y2p = np.zeros(int(T/h))

class wykresOblicz():
    def __init__(self, v0, m, b, fi):

        global T, h, g

        self.v0    = v0
        self.m     = m
        self.b     = b
        self.fi    = fi

        self.xmax  = float(0)
        self.ymax  = float(0)
        self.tmax  = float(0)
        self.tc    = float(0)

        self.x     = np.zeros(int(T/h))
        self.x1p   = np.zeros(int(T/h))
        self.x2p   = np.zeros(int(T/h))
        self.y     = np.zeros(int(T/h))
        self.y1p   = np.zeros(int(T/h))
        self.y2p   = np.zeros(int(T/h))

        self.x1p[0] = v0*np.cos(np.deg2rad(fi))
        self.y1p[0] = v0*np.sin(np.deg2rad(fi))


        for i in range(int(T/h) - 1):
            self.x2p[i]    = ( -1 * b * self.x1p[i] ) / m
            self.x1p[i+1]  = self.x1p[i] + h * self.x2p[i]
            self.x[i+1]    = self.x[i] + h * self.x1p[i] + ( h * h / 2 ) * self.x2p[i]
         
            self.y2p[i]    = -g - b * self.y1p[i] / m
            self.y1p[i+1]  = self.y1p[i] + h * self.y2p[i]
            self.y[i+1]    = self.y[i] + h * self.y1p[i] + ( h * h / 2) * self.y2p[i]
        
            if self.y[i]   >= self.ymax:
                self.ymax  = self.y[i]
                self.tmax  = i * h
            
            if self.y[i]   < 0:
                self.xmax  = self.x[i]
                self.tc    = i*h
                for k in range(i,int(T/h)):
                    self.x[k]   = self.x[i]
                    self.x1p[k] = self.x2p[k] = 0
    
                break   
            plt.draw()

    def zeruj(self):
            self.x     = np.zeros(int(T/h))
            self.x1p   = np.zeros(int(T/h))
            self.x2p   = np.zeros(int(T/h))
            self.y     = np.zeros(int(T/h))
            self.y1p   = np.zeros(int(T/h))
            self.y2p   = np.zeros(int(T/h))

obliczonyWykres = wykresOblicz(v0, m, b, fi)

def wykresRysuj():
    global wykres1, wykres2, wykres3
    global zainicjalizowano
    global obliczonyWykres


    wykres1, = axs[0].plot(t, obliczonyWykres.x)
    wykres2, = axs[1].plot(t, obliczonyWykres.y)
    wykres3, = axs[2].plot(obliczonyWykres.x, obliczonyWykres.y)


#
    podpis_1 = f"Trajektoria x(t):\nZasięg:{round(obliczonyWykres.xmax,precyzja)}m"
    podpis_2 = f"Trajektoria y(t):\nSzczytowa wysokość : {round(obliczonyWykres.ymax,precyzja)}m\nCzas wznoszenia:{round(obliczonyWykres.tmax,precyzja)}s "
    podpis_3 = '\n'.join((
    f"Czas lotu: {round(obliczonyWykres.tc,precyzja)}s",
    f"Optymalny kąt: "+str(opt_kat)))

    props = dict(boxstyle='round', facecolor='wheat', alpha=0.7)

    axs[0].text(0.05, 0.95, podpis_1, transform=axs[0].transAxes, fontsize=14, verticalalignment='top', bbox=props)
    axs[1].text(0.05, 0.95, podpis_2, transform=axs[1].transAxes, fontsize=14, verticalalignment='top', bbox=props)
    axs[2].text(0.05, 0.95, podpis_3, transform=axs[2].transAxes, fontsize=14, verticalalignment='top', bbox=props)

    print('----------------------------------------------')
    print('Szczytowa wysokość : ' , round(obliczonyWykres.ymax,1), '[m]')
    print('Czas wznoszenia: ' , round(obliczonyWykres.tmax,1) , '[s]')
    print('Zasięg : ' , round(obliczonyWykres.xmax,1) , ' [m]')
    print('Czas lotu: ' , round(obliczonyWykres.tc,1) ,' [s]')
    print('----------------------------------------------')
    
    if(zainicjalizowano == False):

        v0Pudlo = fig.add_axes([0.1, 0.05, 0.1, 0.075])
        v0_okno = TextBox(v0Pudlo, "v0 : ", textalignment="center")
        v0_okno.set_val(v0)  # Trigger `submit` with the initial string.
        v0_okno.on_submit(getv0)
       
        mPudlo = fig.add_axes([0.3, 0.05, 0.1, 0.075])
        m_okno = TextBox(mPudlo, "m : ", textalignment="center")
        m_okno.set_val(m)
        m_okno.on_submit(getm)

        bPudlo = fig.add_axes([0.5, 0.05, 0.1, 0.075])
        b_okno = TextBox(bPudlo, "b : ", textalignment="center")
        b_okno.set_val(b)
        b_okno.on_submit(getb)

        fiPudlo = fig.add_axes([0.7, 0.05, 0.1, 0.075])
        fi_okno = TextBox(fiPudlo, "fi : ", textalignment="center")
        fi_okno.set_val(fi)
        fi_okno.on_submit(getfi)

        obliczKatPudlo = plt.axes([0.85, 0.05, 0.1, 0.075])
        przyciskKat = Button(obliczKatPudlo, 'Oblicz kąt',color="yellow")
        przyciskKat.on_clicked(guzik)
    
    zainicjalizowano=True

    plt.show()

def guzik(expression):
    optymalnyKat()
    wykresUaktualnij()

def getv0(expression):
    global v0  
    v0 = eval(expression) 
    wykresUaktualnij()

def getm(expression):
    global m  
    m = eval(expression) 
    wykresUaktualnij()

def getb(expression):
    global b  
    b = eval(expression) 
    wykresUaktualnij()

def getfi(expression):
    global fi  
    fi = eval(expression) 

    wykresUaktualnij()  


def wykresUaktualnij():  
    global obliczonyWykres

    obliczonyWykres.zeruj
    obliczonyWykres = wykresOblicz(v0, m, b, fi)
    
    wykres1.set_ydata(obliczonyWykres.x)
    wykres2.set_ydata(obliczonyWykres.y)
    wykres3.set_ydata(obliczonyWykres.y)

    for k in range(3):
        axs[k].cla()
        axs[k].relim()
        axs[k].autoscale_view()    

    wykresRysuj()


def optymalnyKat():
    global v0, m, b, opt_kat
    xmax_kat = [None] * 900
    for x in range(900):
        kat = x/10
        obliczOptKat = wykresOblicz(v0, m, b, kat)
        xmax_kat[x] = obliczOptKat.xmax
    opt_kat = (xmax_kat.index(max(xmax_kat))) / 10
    
wykresRysuj()





