import ttkbootstrap as ttk
from ttkbootstrap.toast import ToastNotification
import threading
import requests
import json
from PIL import Image, ImageTk

class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("Piep´s, Piepsiges Wetter")
        self.root.maxsize(635, 500)
        self.root.minsize(635, 500)

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 1400
        window_height = 800
        
        x_coordinate = (screen_width / 2) - (window_width / 2)
        y_coordinate = (screen_height / 2) - (window_height / 2)

        self.root.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))

        self.window_width = window_width
        self.window_height = window_height
        self.screen_width = screen_width
        self.screen_height = screen_height


        self.image = Image.open("Logo.png").resize((200, 150))
        self.photo = ImageTk.PhotoImage(self.image)

        self.navbar = ttk.Frame(root, padding="5 10", style="TButton", height=10)
        self.navbar.pack(side="top", fill="x")

        self.navbar_button = ttk.Menubutton(self.navbar, text="Menu")
        self.navbar_button.pack(side="left")
        self.create_dropdown(self.navbar_button)

        self.refresh_button = ttk.Button(self.navbar, padding="5,10", text="Aktualiesieren", command=self.get_entry_data)
        self.refresh_button.pack(side="left")

        self.entry = ttk.Entry(self.navbar)
        self.entry.pack(side="right")
        self.entry.focus_set()
        self.entry.bind("<Return>", self.key_press_handler)

        self.entry_button = ttk.Button(self.navbar, text="Suchen", command=self.get_entry_data)
        self.entry_button.pack(side="right")

        self.meter = ttk.Frame(root, padding="20")
        self.meter.pack(side="top", fill="x")

        photo_label = ttk.Label(self.meter, image=self.photo, text="by Freelance Archery", compound="top")
        photo_label.config()
        photo_label.grid(column=0, row=1)

        self.hum_data = None
        self.meter_hum = ttk.Meter(self.meter, amountused=self.hum_data, textright="%", subtext="Luftfeuchtigkeit", subtextstyle="warning",subtextfont="bolt")
        self.meter_hum.grid(column=1, row=0)

        self.temp_data = None
        self.meter_temp = ttk.Meter(self.meter, amountused=self.temp_data, subtext="Temperatur", textright="°C", subtextstyle="warning",subtextfont="bolt")
        self.meter_temp.grid(column=0, row=0)

        self.datapressure = None
        self.meter_pressure = ttk.Meter(self.meter, amounttotal=1500, amountused=self.datapressure, subtext="Luftdruck", textright="hPa", subtextstyle="warning",subtextfont="bolt")
        self.meter_pressure.grid(column=1, row=1)

        self.wind_data = None
        self.meter_wind = ttk.Meter(self.meter, amountused=self.wind_data, textleft="Wind" ,subtext="Richtung", textright="m/s", subtextstyle="warning",subtextfont="bolt")
        self.meter_wind.grid(column=2, row=1)

        self.view_data = None
        self.view = ttk.Meter(self.meter, amounttotal=100, amountused=self.view_data, subtext="Sichtweite", textright="km", subtextstyle="warning",subtextfont="bolt")
        self.view.grid(column=2, row=0)

        self.data_thread = None

    def get_entry_data(self):
        entry_data = self.entry.get()
        self.citydata = entry_data
        if self.data_thread is not None and self.data_thread.is_alive():
            return
        self.get_data_thread()

    def key_press_handler(self, event):
        if event.keysym == "Return":
            self.get_entry_data()

    def get_data_thread(self):
        self.data_thread = threading.Thread(target=self.get_data)
        self.data_thread.start()

    def get_data(self):
        lang = "de"
        api_key = "546fc8e5dd93bceaedc42572eee7749a"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={self.citydata},de&APPID={api_key}&lang={lang}"
        response = requests.get(url)
        data = json.loads(response.text)

        self.root.after(0, lambda: self.process_data(data))


    def process_data(self, data):
        if "main" in data:
            kelvin = data["main"]["temp"]
            self.temp_data = int(kelvin) - int(273.15)
            self.datapressure = data["main"]['pressure']
            self.hum_data = data["main"]['humidity']
            self.wind_data = data["wind"]["speed"]
            self.view_data = data["visibility"]
            self.view_data = self.view_data / 1000
            self.wind_direction = data["wind"]["deg"]

            if self.wind_direction == 0:
                self.output = f"N, {self.wind_direction}°"
            elif self.wind_direction >= 0 and self.wind_direction <= 90:
                self.output = f"NO, {self.wind_direction}°"
            elif self.wind_direction == 90:
                self.output = f"O, {self.wind_direction}°"
            elif self.wind_direction >= 90 and self.wind_direction <= 180:
                self.output = f"SO, {self.wind_direction}°"
            elif self.wind_direction == 180:
                self.output = f"S, {self.wind_direction}°"
            elif self.wind_direction >= 180 and self.wind_direction <= 270:
                self.output = f"SW, {self.wind_direction}°"
            elif self.wind_direction == 270:
                self.output = f"W, {self.wind_direction}°"
            elif self.wind_direction >= 270 and self.wind_direction <= 0:
                self.output = f"NW, {self.wind_direction}°"
            else:
                self.output = "No Data"

            
            self.meter_hum.configure(amountused=self.hum_data)
            self.meter_temp.configure(amountused=self.temp_data)
            self.meter_pressure.configure(amountused=self.datapressure)
            self.meter_wind.configure(amountused=self.wind_data, subtext=f"Richtung - {self.output}")
            self.view.configure(amountused=self.view_data)

            self.show_toast_in(data)
        else:
            self.show_toast_in(data)

    def show_toast_in(self, data):
        data = data
        print(data)
        if "main" in data:
            toast = ToastNotification(
                title=f"Wetterdaten Gefunden für {self.citydata}",
                message="Daten wurden geladen",
                duration=3000,
                )
            toast.show_toast()
        else:
            toast = ToastNotification(
                title=f"Wetterdaten für {self.citydata} nicht gefunden",
                message="Daten konnten nicht geladen werden",
                duration=3000,
                bootstyle="danger",
                alert=True
                )
            toast.show_toast()
    

    def create_dropdown(self, button):
        dropdown = ttk.Menu(button, tearoff=False)
        dropdown.add_command(label="Öffnen")
        dropdown.add_command(label="Beenden", command=self.exit_program)

        button["menu"] = dropdown

    def exit_program(self):
        self.root.destroy()

root = ttk.Window(themename="solar")
app = Main(root)
root.mainloop()
