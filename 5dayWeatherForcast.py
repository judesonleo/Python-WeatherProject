from tkinter import *
from tkinter import ttk, messagebox
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime, timedelta
import requests
import pytz

root = Tk()
root.title("Weather App")
root.geometry("900x500+300+200")
root.resizable(False, False)

def getweather():
    try:
        city = textfield.get()

        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode(city)
        obj = TimezoneFinder()
        result = obj.timezone_at(lng=location.longitude, lat=location.latitude)

        home = pytz.timezone(result)
        local_time = datetime.now(home)
        current_time = local_time.strftime("%I:%M %p")
        clock.config(text=current_time)
        name.config(text="CURRENT WEATHER")

        # Current Weather
        current_api = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=67b0882b042b7fb96669fa1a487a9788"
        json_data = requests.get(current_api).json()
        condition = json_data['weather'][0]['main']
        description = json_data['weather'][0]['description']
        temp = int(json_data['main']['temp'] - 273.15)
        pressure = json_data['main']['pressure']
        humidity = json_data['main']['humidity']
        wind = json_data['wind']['speed']

        t.config(text=str(temp) + "°C")
        c.config(text=(condition, "|", "FEELS", "LIKE", str(temp) + "°C"))
        w.config(text=wind)
        h.config(text=humidity)
        d.config(text=description)
        p.config(text=pressure)

        # 5-day Forecast (3-hour intervals)
        forecast_api = "https://api.openweathermap.org/data/2.5/forecast?q=" + city + "&appid=67b0882b042b7fb96669fa1a487a9788"
        forecast_json = requests.get(forecast_api).json()
        forecast_data = forecast_json['list']

        # Group forecast data by date
        daily_forecast = {}
        for forecast in forecast_data:
            forecast_time = datetime.fromtimestamp(forecast['dt'], tz=home)
            date_key = forecast_time.strftime('%Y-%m-%d')
            if date_key not in daily_forecast:
                daily_forecast[date_key] = []
            daily_forecast[date_key].append(forecast)

        # Display forecast for each day
        for date_key, forecasts in daily_forecast.items():
            min_temp = min([int(forecast['main']['temp_min'] - 273.15) for forecast in forecasts])
            max_temp = max([int(forecast['main']['temp_max'] - 273.15) for forecast in forecasts])
            avg_temp = (min_temp + max_temp) // 2
            forecast_label = Label(root, text=f"{date_key}: {avg_temp}°C (Min: {min_temp}°C, Max: {max_temp}°C)")
            forecast_label.pack()

    except Exception as e:
        print("Exception:", e)  
        messagebox.showerror("Weather App", "Invalid Entry!!")

# Search box
textfield = Entry(root, justify="center", width=17, font=("popins", 25, "bold"), bg="#404040", border=0, fg="white")
textfield.place(x=50, y=40)
textfield.focus()

search_icon = PhotoImage(file="search_icon.png")
myimage_icon = Button(image=search_icon, borderwidth=0, cursor="hand2", bg="#404040", command=getweather)
myimage_icon.place(x=400, y=34)

# Time
name = Label(root, font=("arial", 15, "bold"))
name.place(x=30, y=100)
clock = Label(root, font=("Helvetica", 20))
clock.place(x=30, y=130)

# Labels
t = Label(root, font=("arial", 70, "bold"), fg="#ee666d")
t.place(x=400, y=150)
c = Label(root, font=("arial", 15, 'bold'))
c.place(x=400, y=250)

w = Label(root, text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
w.place(x=120, y=430)
h = Label(root, text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
h.place(x=280, y=430)
d = Label(root, text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
d.place(x=450, y=430)
p = Label(root, text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
p.place(x=670, y=430)

root.mainloop()
