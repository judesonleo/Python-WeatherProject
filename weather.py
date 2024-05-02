import tkinter as tk
from tkinter import ttk, messagebox
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz

class WeatherApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Weather App")
        self.master.geometry("900x500+300+200")
        self.master.resizable(False, False)

        # Search box
        self.search_image = tk.PhotoImage(file="search.png")
        self.search_label = ttk.Label(image=self.search_image)
        self.search_label.place(x=20, y=20)

        self.textfield = ttk.Entry(self.master, justify="center", width=17, font=("popins", 25, "bold"), background="#404040", foreground="white")
        self.textfield.place(x=50, y=40)
        self.textfield.focus()

        self.search_icon = tk.PhotoImage(file="search_icon.png")
        self.search_button = ttk.Button(image=self.search_icon, cursor="hand2", command=self.get_weather)
        self.search_button.place(x=400, y=34)

        # Logo
        self.logo_image = tk.PhotoImage(file="logo.png")
        self.logo_label = ttk.Label(image=self.logo_image)
        self.logo_label.place(x=150, y=100)

        # Weather information
        self.weather_frame = ttk.Frame(self.master)
        self.weather_frame.place(x=30, y=170)

        self.current_weather_label = ttk.Label(self.weather_frame, text="CURRENT WEATHER", font=("Arial", 15, "bold"))
        self.current_weather_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.temp_label = ttk.Label(self.weather_frame, font=("Arial", 70, "bold"))
        self.temp_label.grid(row=1, column=0, columnspan=2)

        self.condition_label = ttk.Label(self.weather_frame, font=("Arial", 15))
        self.condition_label.grid(row=2, column=0, columnspan=2)

        self.wind_label = ttk.Label(self.weather_frame, text="Wind:", font=("Arial", 12, "bold"))
        self.wind_label.grid(row=3, column=0, padx=(0, 10))

        self.wind_speed_label = ttk.Label(self.weather_frame, text="...", font=("Arial", 12))
        self.wind_speed_label.grid(row=3, column=1)

        self.humidity_label = ttk.Label(self.weather_frame, text="Humidity:", font=("Arial", 12, "bold"))
        self.humidity_label.grid(row=4, column=0, padx=(0, 10))

        self.humidity_value_label = ttk.Label(self.weather_frame, text="...", font=("Arial", 12))
        self.humidity_value_label.grid(row=4, column=1)

        self.description_label = ttk.Label(self.weather_frame, text="Description:", font=("Arial", 12, "bold"))
        self.description_label.grid(row=5, column=0, padx=(0, 10))

        self.description_value_label = ttk.Label(self.weather_frame, text="...", font=("Arial", 12))
        self.description_value_label.grid(row=5, column=1)

        self.pressure_label = ttk.Label(self.weather_frame, text="Pressure:", font=("Arial", 12, "bold"))
        self.pressure_label.grid(row=6, column=0, padx=(0, 10))

        self.pressure_value_label = ttk.Label(self.weather_frame, text="...", font=("Arial", 12))
        self.pressure_value_label.grid(row=6, column=1)

   
    def get_weather(self):
        try:
            city = self.textfield.get()

            geolocator = Nominatim(user_agent="geoapiExercises")
            location = geolocator.geocode(city)
            latitude = location.latitude
            longitude = location.longitude

            obj = TimezoneFinder()
            timezone_str = obj.timezone_at(lng=longitude, lat=latitude)

            # Convert timezone string to a tzinfo object
            timezone = pytz.timezone(timezone_str)

            home = datetime.now(timezone)
            current_time = home.strftime("%I:%M %p")

            api_key = "67b0882b042b7fb96669fa1a487a9788"  # Replace with your OpenWeatherMap API key
            url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}"
            print(url)
            response = requests.get(url)
            data = response.json()

            temp = int(data['main']['temp'] - 273.15)
            condition = data['weather'][0]['main']
            description = data['weather'][0]['description']
            pressure = data['main']['pressure']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']

            self.temp_label.config(text=f"{temp} °C")
            self.condition_label.config(text=condition)
            self.wind_speed_label.config(text=f"{wind_speed} m/s")
            self.humidity_value_label.config(text=f"{humidity}%")
            self.description_value_label.config(text=description)
            self.pressure_value_label.config(text=f"{pressure} hPa")
        except Exception as e:
            messagebox.showerror("Weather App", "Invalid Entry!!")
            print("Exception:", e)


def main():
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
