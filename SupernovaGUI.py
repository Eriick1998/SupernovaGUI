import tkinter as tk
from tkinter import ttk
import requests

class SupernovaChargerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Supernova Charger")
        self.geometry("640x400")

        # Etiquetas
        ttk.Label(self, text="Part number:").place(x=40, y=40)
        ttk.Label(self, text="SW:").place(x=40, y=230)
        ttk.Label(self, text="Serial:").place(x=40, y=200)
        ttk.Label(self, text="Select Type").place(x=190, y=80)
        ttk.Label(self, text="Select Configuration").place(x=220, y=120)
        ttk.Label(self, text="Color / Brand").place(x=190, y=160)
        ttk.Label(self, text="Vector Configuration").place(x=440, y=40)

        self.configs_entry = []

        self.create_entries()
        self.create_comboboxes()
        self.create_dynamic_labels()
        self.create_done_button()


        self.sn = ""  # Atributo sn
        self.pn = ""  # Atributo pn
        self.sw = ""  # Atributo sw


    def create_entries(self):
        font_size = 10  # Tamaño de la fuente
        self.config_supernova = ["PRD", "PW1", "PW2", "MC2", "MD1","MD2",
                            "MET", "OU1", "OU2", "PC1", "PC2","PMV",
                            "ESB", "PVA", "IDV", "MC1", "RFV", "TMP",
                            ] # Valores vector config
        
        label_list = [ttk.Label(self, 
                                text=self.config_supernova[e],
                                font=("Arial", font_size)) 
                                for e in range(len(self.config_supernova))
                                ]
        

        self.mensajes = {
            label_list[0]: "Product: 1, 2",
            label_list[1]: "Outlet max. power: 150, 60",
            label_list[2]: "Outlet max. power: 150, 60",
            label_list[3]: "Outlet max. current: 40, 15",
            label_list[4]: "Outlet DC Meter: 0, 1",
            label_list[5]: "Outlet DC Meter: 0, 1",
            label_list[6]: "AC Meter: 0, 1, 2",
            label_list[7]: "Outlet type: 0, 3, 4",
            label_list[8]: "Outlet type: 0, 3, 4",
            label_list[9]: "Outlet power config: 2",
            label_list[10]: "Outlet power config: 2",
            label_list[11]: "Power module version: 1, 2",
            label_list[12]: "Emergency Stop Button: 0, 1",
            label_list[13]: "Product variant: 0 Standar, 2 Split",
            label_list[14]: "Isolation detector version: 0, 1",
            label_list[15]: "Outlet max. current: 40, 15",
            label_list[16]: "Refrigeration version: 0, 1, 2, 3",
            label_list[17]: "Temperature Probes: 0, 1",
            }
        
        x_pos, y_pos = 430, 70  # Inicializar las posiciones x e y

        for e in range(len(self.config_supernova)):
            if e == (len(self.config_supernova))/2:
                x_pos = 520
                y_pos = 70
            label_list[e].pack()
            label_list[e].place(x=x_pos, y=y_pos)
            y_pos += 30  # Incrementar la posición y para la siguiente etiqueta
            label_list[e].bind("<Enter>", self.mostrar_informacion)
            label_list[e].bind("<Leave>", self.ocultar_informacion)

        x_pos, y_pos = 470, 70

        for e in range(len(self.config_supernova)):
            if e == (len(self.config_supernova))/2:
                x_pos = 560
                y_pos = 70
            valor_config = tk.StringVar()
            self.configs_entry.append(valor_config)
            cuadro_config = ttk.Entry(self, width=3, textvariable=self.configs_entry[e])
            cuadro_config.place(x=x_pos, y=y_pos)
            cuadro_config.bind("<KeyRelease>", self.capturar_seleccion)
            y_pos += 30

        # Etiquetas de SW y SN
        self.valor_texto_2 = tk.StringVar()
        self.cuadro_texto_2 = ttk.Entry(self, width=15, textvariable=self.valor_texto_2)
        self.cuadro_texto_2.place(x=130, y=230)
        self.cuadro_texto_2.bind("<KeyRelease>", self.capturar_seleccion)

        self.valor_texto = tk.StringVar()
        self.cuadro_texto = ttk.Entry(self, width=15, textvariable=self.valor_texto)
        self.cuadro_texto.place(x=130, y=200)
        self.cuadro_texto.bind("<KeyRelease>", self.capturar_seleccion)

        self.mensaje_label = tk.Label(self, relief=tk.RAISED)
        self.mensaje_label.pack(fill=tk.X)

        

    def create_comboboxes(self):
        self.combo = ttk.Combobox(self, state="readonly", values=["DCF1", "DCF2"], width=5)
        self.combo.place(x=130, y=40)
        self.combo.bind("<<ComboboxSelected>>", self.capturar_seleccion)

        self.combo_2 = ttk.Combobox(self, state="readonly", values=["211", "212", "213", "214", "901", "902", "223", "225"], width=5)
        self.combo_2.place(x=130, y=80)
        self.combo_2.bind("<<ComboboxSelected>>", self.capturar_seleccion)

        self.combo_3 = ttk.Combobox(self, state="readonly", values=["84600000", "84000000", "84E00000", "84080000", "84400000"], width=8)
        self.combo_3.place(x=130, y=120)
        self.combo_3.bind("<<ComboboxSelected>>", self.capturar_seleccion)

        self.combo_4 = ttk.Combobox(self, state="readonly", values=["WB1", "BC1", "WV2", "WV3"], width=5)
        self.combo_4.place(x=130, y=160)
        self.combo_4.bind("<<ComboboxSelected>>", self.capturar_seleccion)

    def create_dynamic_labels(self):
        self.etiqueta_generacion = ttk.Label(self, text="Select Supernova")
        self.etiqueta_generacion.place(x=190, y=40)

        self.etiqueta_type = ttk.Label(self, text="Select Type")
        self.etiqueta_type.place(x=190, y=80)

        self.etiqueta_config = ttk.Label(self, text="Select Configuration")
        self.etiqueta_config.place(x=220, y=120)

    def create_done_button(self):
        ttk.Button(self, text="Done", command=self.mostrar_resultado, style="Green.TButton").place(x=295, y=350)

    def capturar_seleccion(self, event):
        valor_1 = self.combo.get()
        valor_2 = self.combo_2.get()
        valor_3 = self.combo_3.get()
        valor_4 = self.combo_4.get()

        self.sn = self.valor_texto.get()
        self.sw = self.valor_texto_2.get()
        self.pn = f'{valor_1}-{valor_2}-{valor_3}-{valor_4}-00-00-00'

        if valor_1 == "DCF1":
            self.etiqueta_generacion.config(text="60 Kw")
        elif valor_1 == "DCF2":
            self.etiqueta_generacion.config(text="150 Kw")

        if valor_2 in ["212", "225"]:
            self.etiqueta_type.config(text="CCS-CCS 5m")
        elif valor_2 in ["211", "223"]:
            self.etiqueta_type.config(text="CCS-CCS 3m")
        elif valor_2 in ["901", "902"]:
            self.etiqueta_type.config(text="CCS-CHADEMO 3.8m")
        elif valor_2 == "213":
            self.etiqueta_type.config(text="CCS-CHADEMO 3m")
        elif valor_2 == "214":
            self.etiqueta_type.config(text="CCS-CHADEMO 5m")

        if valor_3 == "84600000":
            self.etiqueta_config.config(text="Split + 4G + DC + AC")
        elif valor_3 == "84000000":
            self.etiqueta_config.config(text="4G + AC MID")
        elif valor_3 == "84E00000":
            self.etiqueta_config.config(text="Split + Emergency Button")
        elif valor_3 == "84080000":
            self.etiqueta_config.config(text="Payter P66 + 4G + AC MID")
        elif valor_3 == "84400000":
            self.etiqueta_config.config(text="Split + 4G + AC MID")

    def mostrar_informacion(self, event):
        elemento = event.widget
        mensaje = self.mensajes[elemento]
        self.mensaje_label.config(text=mensaje)

    def ocultar_informacion(self, event):
        self.mensaje_label.config(text="")

    def mostrar_resultado(self):
        self.values = [ self.configs_entry[e].get() for e in range(len(self.configs_entry))]
        dic_vec_config = dict(zip(self.config_supernova, self.values))
        diccionario_sin_vacios = {clave: valor for clave, valor in dic_vec_config.items() if valor != ""}
        url = "http://localhost:10003/data"
        headers = {"Content-Type": "application/json"}
        data = {
            "sn": self.sn,
            "pn": self.pn,
            "sw": self.sw,
            "conf_vector": diccionario_sin_vacios,
            "customerConfig": {}
            }

        response = requests.post(url, headers=headers, json=data)
        print(response.status_code)
        print(response.json())


if __name__ == "__main__":
    app = SupernovaChargerApp()
    app.mainloop()
