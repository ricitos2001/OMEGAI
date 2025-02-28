'''
Crear un analizador de codigo que optimize codigo utilizando una IA
Se debe usar como una extension de una IDE
Dicho programa tendra una entrada de datos para introducir el codigo fuente y mostrara por pantalla el codigo optimizado
Si se pide crear codigo la IA mostrara varios ejemplos de codigo
Una vez le des a un boton que pone aceptar el codigo se pegara en editor de codigo de la IDE
El proyecto debe utilizar una nube
'''

import tkinter as tk
from tkinter import ttk
from google import genai

client = genai.Client(api_key="AIzaSyAQrSJYCcjgeAEXp_i1M9BcOfQheP6rHog")

def mostrar_salida(event=None):
    entrada = entrada_texto.get("1.0", tk.END).strip()
    response = client.models.generate_content(model="gemini-2.0-flash", contents=entrada)
    salida = response.text
    salida_texto.config(state=tk.NORMAL)
    salida_texto.delete("1.0", tk.END)
    salida_texto.insert(tk.END, f"Entrada:\n{entrada}\n\nSalida:\n")
    entrada_texto.delete("1.0", tk.END)
    escribir_texto(salida)

def escribir_texto(texto, indice=0):
    if indice < len(texto):
        salida_texto.insert(tk.END, texto[indice])
        salida_texto.see(tk.END)
        ventana.after(50, escribir_texto, texto, indice + 1)
    else:
        salida_texto.config(state=tk.DISABLED)

def insertar_nueva_linea(event=None):
    entrada_texto.insert(tk.INSERT, '\n')
    return 'break'

ventana = tk.Tk()
ventana.title("OMEGAI")
ventana.geometry("550x600")
ventana.configure(background="#2e2e2e")

style = ttk.Style()
style.configure('TText', background='#2e2e2e', foreground='#ffffff', font=('Segoe UI', 12))
style.configure('Vertical.TScrollbar', background='#3e3e3e', troughcolor='#3e3e3e', arrowcolor='#ffffff', relief='flat')


salida_texto = tk.Text(ventana, width=40, height=20, wrap=tk.WORD, state=tk.DISABLED, bg="#1e1e1e", fg="#ffffff", font=('Segoe UI', 12, 'bold'), relief=tk.FLAT, bd=5)
salida_texto.pack(fill="both", expand=True, padx=20, pady=10)
salida_texto.tag_configure('left', justify='left')

entrada_texto = tk.Text(ventana, width=40, height=2, wrap=tk.WORD, bg="#3e3e3e", fg="#ffffff", font=('Segoe UI', 12, 'bold'), relief=tk.FLAT, bd=5)
entrada_texto.pack(fill="both", expand=False, padx=20, pady=10)
entrada_texto.bind("<Return>", mostrar_salida)
entrada_texto.bind("<Shift-Return>", insertar_nueva_linea)

scrollbar = ttk.Scrollbar(entrada_texto, command=entrada_texto.yview, style='Vertical.TScrollbar')
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
entrada_texto['yscrollcommand'] = scrollbar.set

ventana.mainloop()
