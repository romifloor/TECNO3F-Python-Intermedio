import tkinter as tk
from tkinter import ttk , messagebox
import modelo.consultas_dao as consulta

class Frame(tk.Frame):  
    def __init__(self, root = None):    
        super().__init__(root,width=480,height=320)    
        self.root = root    
        self.pack()
        self.id_peli = None
        self.fondo = "#FBFCDD"   
        self.config(bg = self.fondo) # se pueden usar clores hexa o el nombre

        self.label_form()
        self.input_form()
        self.botones_principales()
        self.mostrar_tabla()

    def label_form(self):    
        self.label_nombre = tk.Label(self, text="Nombre: ")
        self.label_nombre.config(font=('Arial',12,'bold'),bg="#FBFCDD",fg="#1931E8")
        self.label_nombre.grid(row= 0, column=0,padx=10,pady=10)

        self.label_nombre = tk.Label(self, text="Duración: ")    
        self.label_nombre.config(font=('Arial',12,'bold'),bg="#FBFCDD",fg="#1931E8")    
        self.label_nombre.grid(row= 1, column=0,padx=10,pady=10)  

        self.label_nombre = tk.Label(self, text="Genero: ")    
        self.label_nombre.config(font=('Arial',12,'bold'),bg="#FBFCDD",fg="#1931E8")    
        self.label_nombre.grid(row= 2, column=0,padx=10,pady=10)

    def input_form(self):   
        self.nombre = tk.StringVar() 
        self.entry_nombre = tk.Entry(self,textvariable=self.nombre)    
        self.entry_nombre.config(width=50, state='disabled')    
        self.entry_nombre.grid(row= 0, column=1,padx=10,pady=10)    
        
        self.duracion = tk.StringVar()
        self.entry_duracion = tk.Entry(self, textvariable=self.duracion)    
        self.entry_duracion.config(width=50, state='disabled')    
        self.entry_duracion.grid(row= 1, column=1,padx=10,pady=10) 

        x = consulta.listar_generos()
        y = []
        for i in x:
            y.append(i[1])

        self.generos = ['Selecione Uno'] + y
        self.entry_genero = ttk.Combobox(self, state="readonly")    
        self.entry_genero.config(width=25, state='disabled')
        self.entry_genero['values'] = self.generos
        self.entry_genero.current(0)  
        self.entry_genero.bind("<<ComboboxSelected>>")    
        self.entry_genero.grid(row= 2, column=1,padx=10,pady=10)
    
    def botones_principales(self):    
        self.btn_alta = tk.Button(self, text='Nuevo', command=self.habilitar_campos)    
        self.btn_alta.config(width= 20,font=('Arial', 12,'bold'),fg ='#FFFFFF' , bg='#1C500B',cursor='hand2',activebackground='#3FD83F',activeforeground='#000000')    
        self.btn_alta.grid(row= 3, column=0,padx=10,pady=10)   

        self.btn_modi = tk.Button(self, text='Guardar', command=self.guardar_campos)    
        self.btn_modi.config(width= 20,font=('Arial', 12,'bold'),fg ='#FFFFFF' ,bg='#0D2A83',cursor='hand2',activebackground='#7594F5',activeforeground='#000000', state='disabled')    
        self.btn_modi.grid(row= 3, column=1,padx=10,pady=10) 

        self.btn_cance = tk.Button(self, text='Cancelar', command=self.bloquear_campos)    
        self.btn_cance.config(width= 20,font=('Arial', 12,'bold'),fg ='#FFFFFF' ,bg='#A90A0A',cursor='hand2',activebackground='#F35B5B',activeforeground='#000000', state='disabled')    
        self.btn_cance.grid(row= 3, column=2,padx=10,pady=10)
    
    def mostrar_tabla(self):

        self.lista_p = consulta.listar_peli()

        self.lista_p.reverse()

        self.tabla = ttk.Treeview(self, columns=('Nombre','Duracion','Genero'))
        self.tabla.grid(row=4, column=0, columnspan=4, sticky='nse')

        self.scroll = ttk.Scrollbar(self, orient='vertical', command= self.tabla.yview)
        self.scroll.grid(row=4,column=4, sticky='nse')
        self.tabla.configure(yscrollcommand=self.scroll.set)

        self.tabla.heading('#0', text='ID')
        self.tabla.heading('#1', text='Nombre')
        self.tabla.heading('#2', text='Duracion')
        self.tabla.heading('#3', text='Genero')

        for p in self.lista_p:
            self.tabla.insert('',0,text=p[0],
                              values=(p[1],p[2],p[3]))

        self.btn_editar = tk.Button(self, text='Editar', command= self.editar_registro)    
        self.btn_editar.config(width= 20,font=('Arial', 12,'bold'),fg ='#FFFFFF' ,bg='#1C500B',cursor='hand2',activebackground='#3FD83F',activeforeground='#000000')    
        self.btn_editar.grid(row= 5, column=0,padx=10,pady=10)    
        
        self.btn_delete = tk.Button(self, text='Delete', command= self.eliminar_regristro)    
        self.btn_delete.config(width= 20,font=('Arial', 12,'bold'),fg ='#FFFFFF' ,bg='#A90A0A',cursor='hand2',activebackground='#F35B5B',activeforeground='#000000')    
        self.btn_delete.grid(row= 5, column=1,padx=10,pady=10)

    def editar_registro(self):
        try:
            self.id_peli = self.tabla.item(self.tabla.selection())['text']

            self.nombre_peli = self.tabla.item(self.tabla.selection())['values'][0]
            self.dura_peli = self.tabla.item(self.tabla.selection())['values'][1]
            self.gene_peli = self.tabla.item(self.tabla.selection())['values'][2]

            self.habilitar_campos()
            self.nombre.set(self.nombre_peli)
            self.duracion.set(self.dura_peli)
            self.entry_genero.current(self.generos.index(self.gene_peli))
        except:
            pass  
    
    def eliminar_regristro(self):
        self.id_peli = self.tabla.item(self.tabla.selection())['text']

        response = messagebox.askyesno("Confirmar","Desea borrar el registro ?")
        
        if response:    
            consulta.borrar_peli(int(self.id_peli))
        else:
            messagebox.showinfo("MIRA BIEN", "CASI BORRAS ALGO EQUIVOCADO")
        
        self.id_peli = None
        self.mostrar_tabla()

    

    def guardar_campos(self):
        pelicula = consulta.Peliculas(
            self.nombre.get(),
            self.duracion.get(),
            self.entry_genero.current()
        )

        if self.id_peli == None:
            consulta.guardar_peli(pelicula)
        else:
            consulta.editar_peli(pelicula,int(self.id_peli))
        
        self.mostrar_tabla()
        self.bloquear_campos()
        


    def habilitar_campos(self):    
        self.entry_nombre.config(state='normal')    
        self.entry_duracion.config(state='normal')    
        self.entry_genero.config(state='normal')    
        self.btn_modi.config(state='normal')    
        self.btn_cance.config(state='normal')    
        self.btn_alta.config(state='disabled')

    def bloquear_campos(self):    
        self.entry_nombre.config(state='disabled')
        self.entry_duracion.config(state='disabled')    
        self.entry_genero.config(state='disabled')    
        self.btn_modi.config(state='disabled')    
        self.btn_cance.config(state='disabled')    
        self.btn_alta.config(state='normal')
        self.nombre.set('')
        self.duracion.set('')
        self.entry_genero.current(0)
        self.id_peli = None


