import os.path

from apodManager import *
from exoplanetManager import *
from functions import *
from customtkinter import *

# tkinter boilerplate
root = CTk()
root.geometry("1150x750")

# setting theme
set_appearance_mode(settings["theme"])

# set title and icon
root.title("CosmoLens")

icon_path = "../assets/icon.png"
try:
    icon_image = Image.open(icon_path)
    icon_photo = ImageTk.PhotoImage(icon_image)
    root.iconphoto(False, icon_photo)
except Exception as e:
    print_colored(f"Error loading icon: {e}", Fore.RED)

# define colors so i don't have to fuckin suffer later :)
darkest = "#003B5C"
dark = "#005B77"
medium = "#007A8E"
light = "#009B9F"
lightest = "#00B2A9"
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------- #

titleLabel = CTkLabel(root, text="CosmoLens", text_color=medium, font=("Futura", 50))
titleLabel.place(relx=0.52, rely=0.05, anchor=CENTER)

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------- #
# Search by Name
searchByNameLabel = CTkLabel(
    root,
    text="Search exoplanets by name:",  # Label text
    text_color=medium,  # Medium color for text
    font=("Futura", 20)  # Font: Futura, size 20
)

searchByNameLabel.place(
    relx=0.2,  # X position for alignment
    rely=0.2,  # Vertical position for this section
    anchor=CENTER
)

searchByNameEntry = CTkEntry(
    root,
    width=100,  # Width of the entry box
    font=("Futura", 20),  # Font for the entry text
    text_color=dark  # Dark color for user input
)

searchByNameEntry.place(
    relx=0.43,  # X position right of the label
    rely=0.2,  # Aligned with the label vertically
    anchor=CENTER
)

searchByNameGoButton = CTkButton(
    root,
    text="Go!",  # Button text
    font=("Futura", 15),  # Font style for the button
    text_color=lightest,  # Light color for button text
    width=30  # Small button width
)

searchByNameGoButton.place(
    relx=0.52,  # Positioned right of the entry box
    rely=0.2,  # Aligned vertically with the label and entry
    anchor=CENTER
)

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------- #
# Search by Discovery Year
searchByDiscYearLabel = CTkLabel(
    root,
    text="Search exoplanets by year of discovery:",  # Label text
    text_color=medium,  # Medium text color
    font=("Futura", 20)  # Font style for the label
)

searchByDiscYearLabel.place(
    relx=0.2,  # X position for alignment
    rely=0.3,  # Positioned below the "Search by Name" section
    anchor=CENTER
)

searchByDiscYearEntry = CTkEntry(
    root,
    width=100,  # Width of the entry box
    font=("Futura", 20),  # Font style for user inputs
    text_color=dark  # Dark text color for input field
)

searchByDiscYearEntry.place(
    relx=0.43,  # Positioned right of the label
    rely=0.3,  # Aligned to the label
    anchor=CENTER
)

searchByDiscYearGoButton = CTkButton(
    root,
    text="Go!",  # Button text
    font=("Futura", 15),  # Font style for the button
    text_color=lightest,  # Lightening text color for the button
    width=30  # Width of the button
)

searchByDiscYearGoButton.place(
    relx=0.52,  # Positioned right of the entry
    rely=0.3,  # Aligned vertically with label and entry
    anchor=CENTER
)

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------- #
# Search by Host Star Name
searchByHostNameLabel = CTkLabel(
    root,
    text="Search exoplanets by host star name:",  # Label text
    text_color=medium,  # Medium color for text
    font=("Futura", 20)  # Font style for the label
)

searchByHostNameLabel.place(
    relx=0.2,  # X position for alignment
    rely=0.4,  # Positioned below the "Search by Discovery Year" section
    anchor=CENTER
)

searchByHostNameEntry = CTkEntry(
    root,
    width=100,  # Width of the entry box
    font=("Futura", 20),  # Font style for user inputs
    text_color=dark  # Dark color for text input
)

searchByHostNameEntry.place(
    relx=0.43,  # Positioned right of the label
    rely=0.4,  # Aligned with label vertically
    anchor=CENTER
)

searchByHostNameGoButton = CTkButton(
    root,
    text="Go!",  # Button text
    font=("Futura", 15),  # Font style for the button
    text_color=lightest,  # Light button text color
    width=30  # Width for smaller appearance
)

searchByHostNameGoButton.place(
    relx=0.52,  # Positioned right of the entry box
    rely=0.4,  # Aligned vertically with label and entry
    anchor=CENTER
)

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------- #
# Search by Discovery Method
searchByDiscoveryMethodLabel = CTkLabel(
    root,
    text="Search exoplanets by discovery method:",  # Label text
    text_color=medium,  # Medium text color
    font=("Futura", 20)  # Font style matching the label sizes
)

searchByDiscoveryMethodLabel.place(
    relx=0.2,  # X alignment position for labels
    rely=0.5,  # Positioned below "Search by Host Star Name" section
    anchor=CENTER
)

searchByDiscoveryMethodEntry = CTkEntry(
    root,
    width=100,  # Width of the entry box
    font=("Futura", 20),  # Font style for input field
    text_color=dark  # Dark color for input text
)

searchByDiscoveryMethodEntry.place(
    relx=0.43,  # Positioned right of the label box
    rely=0.5,  # Aligned to the label
    anchor=CENTER
)

searchByDiscoveryMethodGoButton = CTkButton(
    root,
    text="Go!",  # Button display text
    font=("Futura", 15),  # Font style for button
    text_color=lightest,  # Bright color for button text
    width=30  # Width for a compact button look
)

searchByDiscoveryMethodGoButton.place(
    relx=0.52,  # Positioned right of the input box
    rely=0.5,  # Aligned to the section vertically
    anchor=CENTER
)

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------- #
# apod

apodDescriptionLabel = CTkLabel(root, text=f"The NASA APOD for {get_current_date()}", font=("Futura", 20), text_color=medium, wraplength=450)
apodDescriptionLabel.place(relx=0.77, rely=0.65, anchor=CENTER)

# fetch and download the apod
apodImageURL, apodDesc = fetch_apod()

download_image_from_url(apodImageURL, '../assets/apod.jpeg')

# aaaah just work pls
print_colored(f"File size: {os.path.getsize(f'../assets/apod.jpeg')}", Fore.LIGHTYELLOW_EX)

# omfg the fucking apod is a YOUTUBE VIDEO BRO WHY
print_colored(apodImageURL, Fore.LIGHTBLUE_EX)

# load the downloaded image and display
try:
    apodImage = Image.open('../assets/apod.jpeg')
    apodImage = apodImage.resize((350, 350))

    apodImagePhoto = ImageTk.PhotoImage(apodImage)

    # display it
    apodImageLabel = CTkLabel(root, image=apodImagePhoto, text="")
    apodImageLabel.place(relx=0.77, rely=0.37, anchor=CENTER)
except:
    # bruh its a video :(
    print_colored(f"APOD for today is a video at URL {apodImageURL}", Fore.GREEN)

    apodImageLabel = CTkLabel(root, text=f"Today's APOD is a YouTube™ video at {apodImageURL}. Sorry!", font=("Futura", 30), text_color=darkest, wraplength=350, cursor="target")
    apodImageLabel.place(relx=0.77, rely=0.37, anchor=CENTER)
    apodImageLabel.bind("<Button-1>", lambda hehe: callback(apodImageURL))

    apodDescriptionLabel.configure(text=f"The NASA APOD for {get_current_date()}. Click it to view the video.")

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------- #
# credit label (man i just gonna fill this shiz up bro)

creditLabel = CTkLabel(root, text="Made by Swarit Narang. This work is under the MIT License.", font=("Futura", 20), text_color=medium)
creditLabel.place(relx=0.52, rely=0.9, anchor=CENTER)

root.mainloop()
