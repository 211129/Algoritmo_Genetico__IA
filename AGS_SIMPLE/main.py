# import
from tkinter import Tk,ttk, messagebox as mg
from tkinter import Toplevel
from AGS import AGS

class Interfaz:

    def __init__(self):
        self.main_Interface()

    def setVariables(self):

        self.func = self.funcion.get() 
        self.pc = float(self.prob_de_cruza.get()) 
        self.pmi = float(self.probmi.get())  
        self.pmg = float(self.probmg.get()) 
        self.po = int(self.poblacion_inicial.get()) 
        self.p_Max = int(self.poblacion_maxima.get())  
        self.rango_min = float(self.xmin.get())  
        self.rango_max = float(self.xmax.get()) 
        self.interv = 1 
        self.cantidad_gene = int(self.iter.get())




    def main_Interface(self):
        self.windows = Tk()
        self.windows.geometry('500x600')
        self.windows.title('IA-Algoritmos-Geneticos')
        self.windows.resizable(0,0)
        self.windows.config(bg="#506266")

        title_1 = ttk.Label(self.windows, text='Función f (x,y) = : ')
        title_1.place(x=20, y=34)
        title_1.config(background="#506266", foreground='white', font=('Helveica',11,'bold'))
        self.funcion = ttk.Entry(self.windows) #Función f (x,y)
        self.funcion.place(x=155, y=30, width=230, height=30)


        title_poblacion = ttk.Label(self.windows, text='Población')                                                                                                                       
        title_poblacion.place(x=20, y=90)
        title_poblacion.config(background="#506266", foreground='white', font=('Helveica',13,'bold'))

        title_cruza = ttk.Label(self.windows, text='Prob. de cruza:')
        title_cruza.place(x=20, y=110)
        title_cruza.config(background="#506266", foreground='white', font=('Helveica',11))
        self.prob_de_cruza = ttk.Entry(self.windows)
        self.prob_de_cruza.place(x=165, y=107, width=45, height=30)

        title_2 = ttk.Label(self.windows, text='Población inicial : ')
        title_2.place(x=20, y=145)
        title_2.config(background="#506266", foreground='white', font=('Helveica',11))
        self.poblacion_inicial = ttk.Entry(self.windows)
        self.poblacion_inicial.place(x=165, y=142, width=45, height=30)

        title_3 = ttk.Label(self.windows, text='Población máxima : ')
        title_3.place(x=245,    y=145)
        title_3.config(background="#506266", foreground='white', font=('Helveica',11,))
        self.poblacion_maxima = ttk.Entry(self.windows)
        self.poblacion_maxima.place(x=405, y=142, width=45, height=30)


        title_mutacion = ttk.Label(self.windows, text='Probabilidades de Mutación')
        title_mutacion.place(x=20, y=200)
        title_mutacion.config(background="#506266", foreground='white', font=('Helveica',13,'bold'))

        title_4 = ttk.Label(self.windows, text='Por Individuo : ')
        title_4.place(x=20, y=225)
        title_4.config(background="#506266", foreground='white', font=('Helveica',11))
        self.probmi = ttk.Entry(self.windows)
        self.probmi.place(x=165, y=225, width=45, height=30)

        title_5 = ttk.Label(self.windows, text='Por Gen : ')
        title_5.place(x=245, y=225)
        title_5.config(background="#506266", foreground='white', font=('Helveica',11))
        self.probmg = ttk.Entry(self.windows)
        self.probmg.place(x=405, y=225, width=45, height=30)

        title_mutacion = ttk.Label(self.windows, text='Rango de la Solución')
        title_mutacion.place(x=20, y=290)
        title_mutacion.config(background="#506266", foreground='white', font=('Helveica',13,'bold'))

        title_4 = ttk.Label(self.windows, text='X Mínima : ')
        title_4.place(x=20, y=315)
        title_4.config(background="#506266", foreground='white', font=('Helveica',11))
        self.xmin = ttk.Entry(self.windows)
        self.xmin.place(x=165, y=315, width=45, height=30)

        title_5 = ttk.Label(self.windows, text='X Máxima : ')
        title_5.place(x=245, y=315)
        title_5.config(background="#506266", foreground='white', font=('Helveica',11))
        self.xmax = ttk.Entry(self.windows)
        self.xmax.place(x=405, y=315, width=45, height=30)

        title_iteraciones = ttk.Label(self.windows, text='Iteraciones')
        title_iteraciones.place(x=20, y=370)
        title_iteraciones.config(background="#506266", foreground='white', font=('Helveica',13,'bold'))

        title_5 = ttk.Label(self.windows, text='Cant. Iteraciones : ')
        title_5.place(x=20, y=390)
        title_5.config(background="#506266", foreground='white', font=('Helveica',11))
        self.iter = ttk.Entry(self.windows)
        self.iter.place(x=165, y=390, width=45, height=30)

        
        self.btn_process = ttk.Button(self.windows, text='Iniciar Algoritmo', command=self.initLoop)
        self.btn_process.place(x=120, y=470, width=300, height=35)


        self.windows.mainloop()

    def test(self):
        self.setVariables()
        print(f''''
              Funcion: {self.func}
              Prob. Cruza: {self.pc},
              PMI: {self.pmi},
              PMG: {self.pmg},
              PO: {self.po},
              PMax: {self.p_Max},
              Rmin: {self.rango_min},
              Rmax: {self.rango_max},
              Gen: {self.cantidad_gene},
              ''')

    def initLoop(self):
        try :
            self.setVariables()
            ags = AGS(self.pc, self.pmi, self.pmg, self.po, self.p_Max, self.rango_min, self.rango_max,
                        self.interv, self.cantidad_gene, self.func)
            ags.graphi_generation()
            self.open_popup()
        except Exception as e:
            print(e,"Introduce datos validos")

    def open_popup(self):
        self.top = Toplevel(self.windows)
        self.top.geometry("460x200")
        self.top.title("Child Window")
        self.top.grab_set()
        text='Gráficas de dispersión generadas y guardadas en la carpeta images ./'
        ttk.Label(self.top, text= text, font=('Mistral 10 bold')).place(x=10,y=80)
        ttk.Button(self.top, text='OK', command=self.close_popup).place(x=200,y=110)

    def close_popup(self):
        self.top.grab_release()
        self.top.destroy()
       

if __name__ == '__main__':
    Interfaz()



