import random as r
import json
import requests
import pandas as pd
import os
from datetime import datetime

from PIL import Image, ImageDraw, ImageFont, ImageTk
from colorama import Fore, Style

# load up the settings json file
with open("../settings.json", "r") as f:
    settings = json.load(f)

# declare some variables for the settings
API_KEY = settings["api_key"]
HD_PHOTOS = settings["hd_photos"]
COLORED_TEXT = settings["colored_text"]

def print_colored(text, color):
    """
    Print text in a specific color, if enabled in settings.json.
    :param text: The text which needs to be printed.
    :param color: The color in which the text needs to be printed.
    :return: Absolutely, completely, utterly, entirely, wholly, purely, altogether, downright, flat-out, unconditionally, unmistakably, and indisputably nothing.
    """
    if COLORED_TEXT:
        print(color + text + Style.RESET_ALL)
    else:
        print(text)


# print remaining requests
def print_remaining_requests():
    """
    Uses a dummy API call find the amount of remaining requests the specified API key has for the hour.
    :return: Number of requests left for the hour.
    """

    # use a dummy api call to find the number of requests left
    url = f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}&date=2000-01-01"

    response = requests.get(url)

    if response.status_code != 200:
        print_colored("Remaining requests for the hour: 0", Fore.RED)
        return

    # Grab the number of requests from the response
    remaining_requests = response.headers.get("X-RateLimit-Remaining", "Unknown")

    # Print it
    if int(remaining_requests) >= 700:
        print_colored(f"Remaining requests for the hour: {remaining_requests}", Fore.LIGHTGREEN_EX)
    elif int(remaining_requests) >= 500:
        print_colored(f"Remaining requests for the hour: {remaining_requests}", Fore.GREEN)
    elif int(remaining_requests) >= 300:
        print_colored(f"Remaining requests for the hour: {remaining_requests}", Fore.YELLOW)
    elif int(remaining_requests) > 0:
        print_colored(f"Remaining requests for the hour: {remaining_requests}", Fore.LIGHTRED_EX)
    else:
        print_colored("You ran out of requests for the hour.", Fore.RED)

# pick a random space fact from the txt file (yes i used chatgpt for the facts, what u gonna do)
def pick_space_fact():
    with open("../data/space_facts.txt", "r") as f:
        return r.choice(f.readlines()).strip()

# get current date (this is honestly just bc im too lazy hehe)
def get_current_date():
    return datetime.now().strftime("%d %B %Y")
