import tkinter as tk
from tkinter import ttk
from google import genai

def main():
    client = genai.Client(api_key="AIzaSyAQrSJYCcjgeAEXp_i1M9BcOfQheP6rHog")
    system_prompt = ""

    def configurar_system_prompt():
        def guardar_prompt():
            global system_prompt
            system_prompt = prompt_texto.get("1.0", tk.END).strip()
            ventana_prompt.destroy()

        ventana_prompt = tk.Toplevel()
        ventana_prompt.title("Configurar System Prompt")
        ventana_prompt.geometry("400x300")
        ventana_prompt.configure(background="#2e2e2e")
        
        etiqueta = tk.Label(ventana_prompt, text="Escribe el System Prompt:", bg="#2e2e2e", fg="#ffffff", font=('Segoe UI', 12, 'bold'))
        etiqueta.pack(pady=10)
        
        prompt_texto = tk.Text(ventana_prompt, width=40, height=10, wrap=tk.WORD, bg="#3e3e3e", fg="#ffffff", font=('Segoe UI', 12, 'bold'), relief=tk.FLAT, bd=5)
        prompt_texto.pack(fill="both", expand=True, padx=20, pady=10)
        
        boton_guardar = tk.Button(ventana_prompt, text="Guardar", command=guardar_prompt, bg="#1e1e1e", fg="#ffffff", font=('Segoe UI', 12, 'bold'))
        boton_guardar.pack(pady=10)

    def mostrar_salida(event=None):
        entrada = entrada_texto.get("1.0", tk.END).strip()
        # Incluir el system prompt en el contenido enviado
        contenido = f"{system_prompt}\n\n{entrada}"
        response = client.models.generate_content(model="gemini-2.0-flash", contents=contenido)
        salida = response.text
        salida_texto.config(state=tk.NORMAL)
        salida_texto.delete("1.0", tk.END)
        salida_texto.insert(tk.END, f"System Prompt:\n{system_prompt}\n\nEntrada:\n{entrada}\n\nSalida:\n")
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

    # Botón para configurar el System Prompt
    boton_configurar = tk.Button(ventana, text="Configurar System Prompt", command=configurar_system_prompt, bg="#1e1e1e", fg="#ffffff", font=('Segoe UI', 12, 'bold'))
    boton_configurar.pack(pady=10)

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


if __name__ == "__main__":
    main()