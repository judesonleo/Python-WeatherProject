from tkinter import *
from tkinter import ttk, messagebox
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz
from colorss import colors
root = Tk()
style = ttk.Style()
root.title("Weather App")
root.geometry("1200x700+100+200")
root.configure(bg=colors["background-color"]) 
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

        # Weather
        api = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=7aecb547118d7e5638a3bd8a0a251a0f"
        print(api)
        json_data = requests.get(api).json()
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

    except Exception as e:
        print("Exception:", e)  # Print the exception message for debugging
        messagebox.showerror("Weather App", "Invalid Entry!!")
#Left Navbar

left_navbar= Frame(root, bg=colors["background-color"] , width=200, height=300)
left_navbar.pack(side="left", fill="y")
left_title = Label(left_navbar, text= "Weather App",bg=colors["background-color"] , font=('Caveat',20, "bold"), fg=colors["text-color"])
left_title.pack(pady=10, padx=10)


#Right Frame

frame = Frame(root, bg=colors["card-color"])
frame.pack(side="right",fill="y")

right_navbar= Frame(frame, bg=colors["background-color"])
right_navbar.pack(side="right", fill="y")

search_image = PhotoImage(file="icon1.png")
resized_image = search_image.subsample(20, 20)
myimage = Label(right_navbar, image=resized_image, cursor="hand2",bg=colors["card-color"] )
myimage.place(x=1080, y=10)
right_title = Label(right_navbar, text= "Search",bg=colors["card-color"] , font=('Caveat',20, "bold"), fg=colors["text-color"])
right_title.pack(pady=10, padx=10)
right_navbar.pack(padx=20,pady=20)



# Search box
# search_image = PhotoImage(file="search.png")
# myimage = Label(image=search_image)
# myimage.place(x=40, y=70)

# textfield = Entry(root, justify="center", width=17, font=("popins", 25, "bold"), bg="#404040", border=0, fg="white")
# textfield.place(x=50, y=70)
# textfield.focus()

# search_icon = PhotoImage(file="search_icon.png")
# myimage_icon = Button(image=search_icon, borderwidth=0, cursor="hand2", bg="#404040", command=getweather)
# myimage_icon.place(x=400, y=34)

# Logo
# Logo_image = PhotoImage(file="logo.png")
# logo = Label(image=Logo_image)
# logo.place(x=150, y=100)

# Bottom box
# Frame_image = PhotoImage(file="box.png")
# frame_myimage = Label(image=Frame_image)
# frame_myimage.pack(padx=5, pady=5, side=BOTTOM)

# Time
# name = Label(root, font=("arial", 15, "bold"))
# name.place(x=30, y=100)
# clock = Label(root, font=("Helvetica", 20))
# clock.place(x=30, y=130)

# Labels
# label1 = Label(root, text="WIND", font=("Helvetica", 15, 'bold'), fg="white", bg="#1ab5ef")
# label1.place(x=120, y=400)

# label2 = Label(root, text="HUMIDITY", font=("Helvetica", 15, 'bold'), fg="white", bg="#1ab5ef")
# label2.place(x=250, y=400)

# label3 = Label(root, text="DESCRIPTION", font=("Helvetica", 15, 'bold'), fg="white", bg="#1ab5ef")
# label3.place(x=430, y=400)

# label4 = Label(root, text="PRESSURE", font=("Helvetica", 15, 'bold'), fg="white", bg="#1ab5ef")
# label4.place(x=650, y=400)

# t = Label(root, font=("arial", 70, "bold"), fg="#ee666d")
# t.place(x=400, y=150)
# c = Label(root, font=("arial", 15, 'bold'))
# c.place(x=400, y=250)

# w = Label(root, text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
# w.place(x=120, y=430)
# h = Label(root, text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
# h.place(x=280, y=430)
# d = Label(root, text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
# d.place(x=450, y=430)
# p = Label(root, text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
# p.place(x=670, y=430)

root.mainloop()
