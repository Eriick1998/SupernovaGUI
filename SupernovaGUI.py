import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import requests


class SupernovaChargerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Supernova Charger V1.1.0")
        self.geometry("880x400")
        self.url = ""

        # Etiquetas
        ttk.Label(self, text="Part number:").place(x=40, y=40)
        ttk.Label(self, text="SW:").place(x=40, y=230)
        ttk.Label(self, text="Serial:").place(x=40, y=200)
        ttk.Label(self, text="Select Type").place(x=190, y=80)
        ttk.Label(self, text="Select Config").place(x=220, y=120)
        ttk.Label(self, text="Color / Brand").place(x=190, y=160)
        ttk.Label(self, text="Vector Configuration").place(x=650, y=40)
        ttk.Label(self, text="PN Final: ").place(x=40, y=280)

        self.configs_entry = []
        self.part_name = []

        self.create_entries()
        self.create_comboboxes()
        self.create_dynamic_labels()
        self.create_done_button()

        self.sn = ""  # Atributo sn
        self.pn = ""  # Atributo pn
        self.sw = ""  # Atributo sw


    def create_entries(self):
        font_size = 10
        self.config_supernova = ["PRD", "PW1", "PW2", "OU1", "OU2", "MC1", "MC2", "MD1", "MD2",
                                 "MET", "PC1", "PC2", "PMV", "ESB", "PVA", "IDV", "RFV", "TMP"]
        label_list = [ttk.Label(self,
                                text=self.config_supernova[e],
                                font=("Arial", font_size)) for e in range(len(self.config_supernova))]

        self.mensajes = {
            label_list[0]: "Product:                        1: Supernova,   2: Supernova Gen_2,    3: Hypernova",
            label_list[1]: "Outlet max. power:              150,            60",
            label_list[2]: "Outlet max. power:              150,            60",
            label_list[3]: "Outlet type:                    0: None,        3: CCS,     4: CHAdeMO",
            label_list[4]: "Outlet type:                    0: None,        3: CCS,     4: CHAdeMO",
            label_list[5]: "Outlet max. current:            40,             15",
            label_list[6]: "Outlet max. current:            40,             15",
            label_list[7]: "Outlet DC Meter:                0: None,        1: ACREL DSJF1352",
            label_list[8]: "Outlet DC Meter:                0: None,        1: ACREL DSJF1352",
            label_list[9]: "AC Meter:                       0: None,        1: Carlo Gavazzi,      2: Inepro",
            label_list[10]: "Outlet power config:           2: DC",
            label_list[11]: "Outlet power config:           2: DC",
            label_list[12]: "Power module version:          1: QPM,     2: UUGreen CPM",
            label_list[13]: "Emergency Stop Button:         0: Not installed    1: Latch",
            label_list[14]: "Product variant:               0: Standar,      2: Split",
            label_list[15]: "Isolation detector version:    0: Bender (isoGEN423,isoCHA425,isoCHA425HV) 1:Trafox",
            label_list[16]: "Refrigeration version:         0, 1, 2, 3",
            label_list[17]: "Temperature Probes:            0: None    1: 4 x NTC",
        }

        x_pos, y_pos = 650, 70  # Inicializar las posiciones x e y

        for e in range(len(self.config_supernova)):
            if e == (len(self.config_supernova)) / 2:
                x_pos = 720
                y_pos = 70
            label_list[e].pack()
            label_list[e].place(x=x_pos, y=y_pos)
            y_pos += 30  # Incrementar la posición y para la siguiente etiqueta
            label_list[e].bind("<Enter>", self.mostrar_informacion)
            label_list[e].bind("<Leave>", self.ocultar_informacion)

        x_pos, y_pos = 690, 70

        for e in range(len(self.config_supernova)):
            if e == (len(self.config_supernova)) / 2:
                x_pos = 760
                y_pos = 70
            valor_config = tk.StringVar()
            self.configs_entry.append(valor_config)
            cuadro_config = ttk.Entry(self, width=3, textvariable=self.configs_entry[e])
            cuadro_config.place(x=x_pos, y=y_pos)
            cuadro_config.bind("<KeyRelease>", self.capturar_seleccion)
            y_pos += 30

        # Etiquetas de SW y SN y PN_final
        self.valor_texto_3 = tk.StringVar()
        self.cuadro_texto_3 = ttk.Entry(self, width=30, textvariable=self.valor_texto_3)
        self.cuadro_texto_3.place(x=130, y=280)
        self.cuadro_texto_3.bind("<KeyRelease>", self.capturar_seleccion)

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

        self.combo_2 = ttk.Combobox(self, state="readonly",
                                    values=["207", "208", "211", "212", "213", "214", "222", "223", "224", "225", "901",
                                            "902"], width=5)
        self.combo_2.place(x=130, y=80)
        self.combo_2.bind("<<ComboboxSelected>>", self.capturar_seleccion)

        self.combo_3 = ttk.Combobox(self, state="readonly",
                                    values=["84000000", "84100000", "84400000", "84600000", "84680000", "84700000",
                                            "84800000", "84880000", "84E00000", "84E80000", "84F00000", "84900000",
                                            "84080000", "00000001"], width=9)
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

        self.etiqueta_config = ttk.Label(self, text="Select Config")
        self.etiqueta_config.place(x=220, y=120)

    def create_done_button(self):
        ttk.Button(self, text="Done", command=self.mostrar_resultado, style="Green.TButton").place(x=295, y=350)

    def default_values(self):
        self.configs_entry[0].set("1")
        self.configs_entry[1].set("60")
        self.configs_entry[2].set("60")
        self.configs_entry[3].set("3")
        self.configs_entry[4].set("4")
        self.configs_entry[5].set("15")
        self.configs_entry[6].set("15")
        self.configs_entry[7].set("0")
        self.configs_entry[8].set("0")
        self.configs_entry[9].set("2")
        self.configs_entry[10].set("2")
        self.configs_entry[11].set("2")
        self.configs_entry[12].set("1")
        self.configs_entry[13].set("0")
        self.configs_entry[14].set("0")
        self.configs_entry[15].set("0")
        self.configs_entry[16].set("0")
        self.configs_entry[17].set("0")

    def capturar_seleccion(self, event):
        valor_1 = self.combo.get()
        valor_2 = self.combo_2.get()
        valor_3 = self.combo_3.get()
        valor_4 = self.combo_4.get()

        self.sn = self.valor_texto.get()
        self.sw = self.valor_texto_2.get()
        self.pn = f'{valor_1}-{valor_2}-{valor_3}-{valor_4}-00-00-00'
        self.valor_texto_3.set(self.pn)
        self.default_values()

        if valor_1 == "DCF1":
            self.etiqueta_generacion.config(text="60 Kw")
            self.configs_entry[0].set("1")
            self.configs_entry[12].set("1")
        elif valor_1 == "DCF2":
            self.etiqueta_generacion.config(text="150 Kw")
            self.configs_entry[0].set("2")
            self.configs_entry[12].set("2")

        if valor_2 in ["207"]:
            self.etiqueta_type.config(text="CCS-CCS 3m 30Kw")
            self.configs_entry[1].set("30")
            self.configs_entry[2].set("30")
            self.configs_entry[4].set("3")
        elif valor_2 in ["208"]:
            self.etiqueta_type.config(text="CCS-CCS 5m 30Kw")
            self.configs_entry[1].set("30")
            self.configs_entry[2].set("30")
            self.configs_entry[4].set("3")
        elif valor_2 in ["211"]:
            self.etiqueta_type.config(text="CCS-CCS 3m 60Kw")
            self.configs_entry[4].set("3")
        elif valor_2 in ["212"]:
            self.etiqueta_type.config(text="CCS-CCS 5m 60Kw")
            self.configs_entry[4].set("3")
        elif valor_2 in ["213"]:
            self.etiqueta_type.config(text="CCS-CHADEMO 3m 60Kw")
        elif valor_2 in ["214"]:
            self.etiqueta_type.config(text="CCS-CHADEMO 5m 60Kw")
        elif valor_2 in ["222"]:
            self.etiqueta_type.config(text="CCS-CCS 3m, 150Kw, 250A")
            self.configs_entry[1].set("150")
            self.configs_entry[2].set("150")
            self.configs_entry[4].set("3")
            self.configs_entry[5].set("25")
            self.configs_entry[6].set("25")
        elif valor_2 in ["223"]:
            self.etiqueta_type.config(text="CCS-CCS 3m, 150Kw, 400A")
            self.configs_entry[1].set("150")
            self.configs_entry[2].set("150")
            self.configs_entry[4].set("3")
            self.configs_entry[5].set("40")
            self.configs_entry[6].set("40")
        elif valor_2 in ["224"]:
            self.etiqueta_type.config(text="CCS-CCS 5m, 150Kw, 250A")
            self.configs_entry[1].set("150")
            self.configs_entry[2].set("150")
            self.configs_entry[4].set("3")
            self.configs_entry[5].set("25")
            self.configs_entry[6].set("25")
        elif valor_2 in ["225"]:
            self.etiqueta_type.config(text="CCS-CCS 5m, 150Kw, 400A")
            self.configs_entry[1].set("150")
            self.configs_entry[2].set("150")
            self.configs_entry[4].set("3")
            self.configs_entry[5].set("40")
            self.configs_entry[6].set("40")
        elif valor_2 in ["901"]:
            self.etiqueta_type.config(text="CCS-CHADEMO, 3.8m, 60Kw")
        elif valor_2 in ["902"]:
            self.etiqueta_type.config(text="CCS-CHADEMO, 3.8m, 50Kw")
            self.configs_entry[1].set("50")
            self.configs_entry[2].set("50")


        if valor_3 == "84000000":
            self.etiqueta_config.config(text="AC MID + 4G")
        elif valor_3 == "84100000":
            self.etiqueta_config.config(text="AC MID + 4G + Payter Apollo C2C")
        elif valor_3 == "84400000":
            self.etiqueta_config.config(text=" Split                ")
            self.configs_entry[14].set("2")
        elif valor_3 == "84600000":
            self.etiqueta_config.config(text="AC MID + DC meters + 4G + Split")
            self.configs_entry[7].set("1")
            self.configs_entry[8].set("1")
            self.configs_entry[14].set("2")
        elif valor_3 == "84680000":
            self.etiqueta_config.config(text="AC MID + DC meters + 4G + Split + Payter P66")
            self.configs_entry[7].set("1")
            self.configs_entry[8].set("1")
            self.configs_entry[13].set("1")
            self.configs_entry[14].set("2")
        elif valor_3 == "84700000":
            self.etiqueta_config.config(text="AC MID + DC meters + 4G + Split + Payter Apollo C2C")
            self.configs_entry[7].set("1")
            self.configs_entry[8].set("1")
            self.configs_entry[14].set("2")
        elif valor_3 == "84800000":
            self.etiqueta_config.config(text="AC MID + 4G + ESB")
            self.configs_entry[13].set("1")
        elif valor_3 == "84880000":
            self.etiqueta_config.config(text="AC MID + 4G + Payter P66 + ESB")
            self.configs_entry[13].set("1")
        elif valor_3 == "84E00000":
            self.etiqueta_config.config(text="AC MID + DC meters + 4G + Split + ESB")
            self.configs_entry[7].set("1")
            self.configs_entry[8].set("1")
            self.configs_entry[13].set("1")
            self.configs_entry[14].set("2")
        elif valor_3 == "84E80000":
            self.etiqueta_config.config(text="AC MID + DC meters + 4G + Split + Payter P66 + ESB")
            self.configs_entry[7].set("1")
            self.configs_entry[8].set("1")
            self.configs_entry[13].set("1")
            self.configs_entry[14].set("2")
        elif valor_3 == "84F00000":
            self.etiqueta_config.config(text="AC MID + DC meters + 4G + Split + Payter Apollo C2C + ESB")
            self.configs_entry[7].set("1")
            self.configs_entry[8].set("1")
            self.configs_entry[13].set("1")
            self.configs_entry[14].set("2")
        elif valor_3 == "84900000":
            self.etiqueta_config.config(text="AC MID + 4G + Payter Apollo C2C + ESB")
            self.configs_entry[13].set("1")
        elif valor_3 == "84080000":
            self.etiqueta_config.config(text="AC MID Meter + 4G + Payter P66")
        elif valor_3 == "00000001":
            self.etiqueta_config.config(text="Dummy (can not charge a vehicle)")
        elif valor_3 == "84E00000":
            self.etiqueta_config.config(text="Split + ESB")
            self.configs_entry[7].set("1")
            self.configs_entry[8].set("1")
            self.configs_entry[13].set("1")
            self.configs_entry[14].set("2")
        elif valor_3 == "84080000":
            self.etiqueta_config.config(text="Payter P66 + 4G + AC MID")
        elif valor_3 == "84400000":
            self.etiqueta_config.config(text="Split + 4G + AC MID")
            self.configs_entry[14].set("2")

    def mostrar_informacion(self, event):
        elemento = event.widget
        mensaje = self.mensajes[elemento]
        self.mensaje_label.config(text=mensaje)

    def ocultar_informacion(self, event):
        self.mensaje_label.config(text="")

    def mostrar_resultado(self):
        self.values = [self.configs_entry[e].get() for e in range(len(self.configs_entry))]
        dic_vec_config = dict(zip(self.config_supernova, self.values))
        diccionario_sin_vacios = {clave: valor for clave, valor in dic_vec_config.items() if valor != ""}

        if "" in dic_vec_config.values():
            messagebox.showwarning("Alerta", "¡Hay valores vacíos en el Hardware Vector, p*to!")
        else:
            self.url = "http://localhost:10003/data"
            headers = {"Content-Type": "application/json"}
            data = {
                "sn": self.sn,
                "pn": self.pn,
                "sw": self.sw,
                "conf_vector": diccionario_sin_vacios,
                "customerConfig": {}
            }

            response = requests.post(self.url, headers=headers, json=data)
            print(response.status_code)
            print(response.json())


if __name__ == "__main__":
    app = SupernovaChargerApp()
    app.mainloop()
