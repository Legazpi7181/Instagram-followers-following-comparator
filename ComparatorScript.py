import json
import os
import webbrowser
import customtkinter as ctk
from tkinter import filedialog, messagebox

# Estética
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# (Funciones originales 1.0) Backend
def buscar_usuarios(datos):
    usuarios_encontrados = set()
    
    if isinstance(datos, dict):
        if "title" in datos and datos["title"]: # Seguidos se llama "title"
            usuarios_encontrados.add(datos["title"])
            
        if "string_list_data" in datos: # Seguidores se llama "string_list_data"
            for elemento in datos["string_list_data"]:
                if "value" in elemento and elemento["value"]:
                    usuarios_encontrados.add(elemento["value"])
        
        for valor in datos.values():
            usuarios_encontrados.update(buscar_usuarios(valor))
            
    elif isinstance(datos, list):
        for elemento in datos:
            usuarios_encontrados.update(buscar_usuarios(elemento))
            
    return usuarios_encontrados

def extraer_usuarios(ruta_archivo):
    usuarios = set()
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)
            usuarios = buscar_usuarios(datos)
    except Exception as e:
        print(f"Error al leer '{ruta_archivo}': {e}")
    return usuarios

# Frontend
  class AppInstagram(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configuración de la ventana principal
        self.title("Buscador Instagram")
        self.geometry("600x550")
        self.resizable(False, False)
        
        # Variables para guardar las rutas que elija el usuario
        self.ruta_followers = ""
        self.ruta_following = ""
        
        # Contenedor principal donde irán cambiando las pantallas
        self.contenedor = ctk.CTkFrame(self, fg_color="transparent")
        self.contenedor.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Iniciar mostrando el paso 1
        self.mostrar_paso_1()

    def limpiar_pantalla(self):
        """Borra los elementos visuales de la pantalla anterior"""
        for widget in self.contenedor.winfo_children():
            widget.destroy()

    def mostrar_paso_1(self):
        self.limpiar_pantalla()
        
        titulo = ctk.CTkLabel(self.contenedor, text="Paso 1: Descarga tus archivos JSON", font=("Arial", 22, "bold"))
        titulo.pack(pady=(10, 20))
        
        instrucciones = ctk.CTkLabel(
            self.contenedor, 
            text="Para proteger tu cuenta, esta app no te pide contraseñas.\n"
                 "Usa los datos oficiales que te da Instagram:\n\n"
                 "1. Haz clic en el botón de abajo para ir a Instagram.\n"
                 "2. Solicita una descarga de tu información.\n"
                 "3. Asegúrate de seleccionar el formato JSON.\n"
                 "3.1. Asegúrate de seleccionar SOLO seguidores y seguidos.\n"
                 "3.2. Asegúrate de seleccionar la fecha de tiempo desde la creación de la cuenta.\n"
                 "4. Cuando te llegue el correo, descarga y descomprime el archivo.",
            justify="left", font=("Arial", 13), wraplength=500
        )
        instrucciones.pack(pady=10)
        
        btn_web = ctk.CTkButton(self.contenedor, text="🔗 Ir a Descargas de Instagram", command=self.abrir_web)
        btn_web.pack(pady=20)
        
        btn_siguiente = ctk.CTkButton(self.contenedor, text="Ya he descomprimido mis archivos ➡️", fg_color="#1f538d", command=self.mostrar_paso_2)
        btn_siguiente.pack(side="bottom", pady=10)

    def abrir_web(self):
        webbrowser.open("https://www.instagram.com/download/request/")

    def mostrar_paso_2(self):
        self.limpiar_pantalla()
        
        titulo = ctk.CTkLabel(self.contenedor, text="Paso 2: Selecciona tus archivos", font=("Arial", 22, "bold"))
        titulo.pack(pady=(10, 30))
        
        # --- Selector de Followers ---
        self.btn_followers = ctk.CTkButton(self.contenedor, text="📂 Seleccionar followers_1.json", command=self.buscar_followers)
        self.btn_followers.pack(pady=5)
        self.lbl_followers = ctk.CTkLabel(self.contenedor, text="No seleccionado", text_color="gray")
        self.lbl_followers.pack(pady=(0, 20))
        
        # --- Selector de Following ---
        self.btn_following = ctk.CTkButton(self.contenedor, text="📂 Seleccionar following.json", command=self.buscar_following)
        self.btn_following.pack(pady=5)
        self.lbl_following = ctk.CTkLabel(self.contenedor, text="No seleccionado", text_color="gray")
        self.lbl_following.pack(pady=(0, 20))
        
        # --- Botones de Navegación Inferior ---
        btn_atras = ctk.CTkButton(self.contenedor, text="⬅️ Atrás", fg_color="gray", hover_color="#555555", command=self.mostrar_paso_1)
        btn_atras.pack(side="left", pady=10)
        
        # Botón para procesar (Empieza desactivado)
        self.btn_analizar = ctk.CTkButton(self.contenedor, text="Comprobar Seguidores ⚙️", fg_color="#E51FFF", hover_color="#71117D", state="disabled", command=self.procesar_y_mostrar_resultados)
        self.btn_analizar.pack(side="right", pady=10)

    def buscar_followers(self):
        ruta = filedialog.askopenfilename(filetypes=[("Archivo de Seguidores", "followers_1.json"), ("Archivos JSON", "*.json")])
        if ruta:
            self.ruta_followers = ruta
            self.lbl_followers.configure(text=f"✅ Cargado: {os.path.basename(ruta)}", text_color="#2fa572")
            self.verificar_botones()

    def buscar_following(self):
        ruta = filedialog.askopenfilename(filetypes=[("Archivo de Seguidos", "following.json"), ("Archivos JSON", "*.json")])
        if ruta:
            self.ruta_following = ruta
            self.lbl_following.configure(text=f"✅ Cargado: {os.path.basename(ruta)}", text_color="#2fa572")
            self.verificar_botones()

    def verificar_botones(self):
        """Activa el botón verde si ambos archivos fueron cargados"""
        if self.ruta_followers and self.ruta_following:
            self.btn_analizar.configure(state="normal")

    def procesar_y_mostrar_resultados(self):
        # Ejecutamos TU lógica matemática original
        seguidores = extraer_usuarios(self.ruta_followers)
        seguidos = extraer_usuarios(self.ruta_following)
        
        if not seguidores or not seguidos:
            messagebox.showerror("Error", "No se pudieron extraer usuarios. Asegúrate de que son los archivos correctos de Instagram.")
            return
            
        no_me_siguen = seguidos - seguidores
        
        # Cambiamos a la pantalla de resultados (Paso 3)
        self.limpiar_pantalla()
        
        titulo = ctk.CTkLabel(self.contenedor, text="Resultados del Análisis", font=("Arial", 22, "bold"))
        titulo.pack(pady=(10, 5))
        
        info_stats = ctk.CTkLabel(
            self.contenedor, 
            text=f"Seguidores: {len(seguidores)}  |  Seguidos: {len(seguidos)}\n"
                 f"No te siguen de vuelta: {len(no_me_siguen)}", 
            font=("Arial", 12, "italic"), text_color="gray"
        )
        info_stats.pack(pady=(0, 15))
        
        # Caja deslizable para mostrar la lista de forma elegante
        caja_scroll = ctk.CTkScrollableFrame(self.contenedor, width=500, height=280)
        caja_scroll.pack(pady=10, fill="both", expand=True)
        
        if no_me_siguen:
            for usuario in sorted(no_me_siguen):
                # Fila para cada usuario
                fila = ctk.CTkFrame(caja_scroll, fg_color="transparent")
                fila.pack(fill="x", padx=10, pady=4)
                
                lbl_user = ctk.CTkLabel(fila, text=f"❌ @{usuario}", font=("Arial", 13, "bold"), anchor="w")
                lbl_user.pack(side="left", padx=5)
                
                # Botón individual para ir al navegador web (Soluciona el bug de cuentas borradas)
                btn_perfil = ctk.CTkButton(
                    fila, text="🌐 Abrir Perfil", width=90, height=22, font=("Arial", 11),
                    fg_color="#3a3a3a", hover_color="#555555",
                    command=lambda u=usuario: webbrowser.open(f"https://www.instagram.com/{u}/")
                )
                btn_perfil.pack(side="right", padx=5)
        else:
            lbl_bien = ctk.CTkLabel(caja_scroll, text="🎉 ¡Felicidades! Todos los que sigues te siguen de vuelta.", font=("Arial", 14))
            lbl_bien.pack(pady=50)
            
        # Botón para volver a empezar
        btn_reiniciar = ctk.CTkButton(self.contenedor, text="🔄 Analizar otra cuenta", command=self.mostrar_paso_2)
        btn_reiniciar.pack(side="bottom", pady=(15, 0))

if __name__ == "__main__":
    app = AppInstagram()
    app.mainloop()
