import random as r
import json
import requests
from colorama import Fore, Style

# load up the settings json file
with open("settings.json", "r") as f:
    settings = json.load(f)

# declare some variables for the settings
API_KEY = settings["api_key"]
HD_PHOTOS = settings["hd_photos"]
COLORED_TEXT = settings["colored_text"]

# print remaining requests
def print_remaining_requests():
    """
    Uses a dummy API o find the amount of remaining requests the specified API key has for the hour.
    :return: Number of requests left for the hour.
    """

    # use a dummy api call to find the number of requests left
    url = f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}&date=2000-01-01"

    response = requests.get(url)

    if response.status_code != 200:
        if COLORED_TEXT:
            print(Fore.RED + "Remaining requests for the hour: 0" + Style.RESET_ALL)
        else:
            print("Remaining requests for the hour: 0")
        return

    # Grab the number of requests from the response
    remaining_requests = response.headers.get("X-RateLimit-Remaining", "Unknown")

    # Print it in COLOR (if u want it of course)
    if COLORED_TEXT:
        if int(remaining_requests) >= 700:
            print(Fore.LIGHTGREEN_EX + f"Remaining requests for the hour: {remaining_requests}" + Style.RESET_ALL)
        elif int(remaining_requests) >= 500:
            print(Fore.GREEN + f"Remaining requests for the hour: {remaining_requests}" + Style.RESET_ALL)
        elif int(remaining_requests) >= 300:
            print(Fore.YELLOW + f"Remaining requests for the hour: {remaining_requests}" + Style.RESET_ALL)
        elif int(remaining_requests) > 0:
            print(Fore.LIGHTRED_EX + f"Remaining requests for the hour: {remaining_requests}" + Style.RESET_ALL)
        else:
            print(Fore.RED + "You ran out of requests for the hour." + Style.RESET_ALL)
    else:
        print(f"Remaining requests for the hour: {remaining_requests}")

# the meat and potatoes of the app - the function which fetches the data of the exoplanet
def fetch_exoplanet_data(planet_name):
    """
    Fetch data about a specific exoplanet from NASA's Exoplanet Archive API.

    :param planet_name: Name of the exoplanet to search for
    :return: Dictionary containing the planet's data or an error message
    """

    # TODO: Fix this garbage API call that doesn't work :(

    # Base URL
    url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"

    # SQL query to search for planet name
    query = f"SELECT * FROM ps WHERE TRIM(pl_name) = TRIM(f{planet_name.upper()})"
    # query = f"SELECT TOP 10 * FROM ps"

    # params to the api
    params = {
        "query": query,
        "format": "json", # we want json format bois
    }

    # data pls
    response = requests.get(url, params=params)
    print(response.text)

    print_remaining_requests()

    if response.status_code == 200:
        # oh yeah, les goooooooooo
        data = response.json()

        if len(data) > 0:
            return data[0]
        else:
            if COLORED_TEXT:
                print(Fore.YELLOW + f"No data found for the exoplanet '{planet_name}'." + Style.RESET_ALL)
            return None
    else:
        if COLORED_TEXT:
            print(Fore.RED + f"Error fetching data from NASA Exoplanet Archive API: Error {response.status_code}. Perhaps your API key is incorrect / out of requests" + Style.RESET_ALL)
        else:
            print(f"Error fetching data from NASA Exoplanet Archive API: Error {response.status_code}. Perhaps your API key is incorrect / out of requests")

# grab a sweet, sweet, apod from the nasa api
def fetch_apod():
    """
    Fetch the Astrology Photo of the Day from NASA APOD API.
    :return: The URL of the image and the explanation of the image.
    """
    url = f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}&hd={HD_PHOTOS}"
    print(url)

    response = requests.get(url)
    print_remaining_requests()

    # did it work
    if response.status_code == 200:
        # les go
        data = response.json()

        image_url = data["url"]
        explanation = data["explanation"]

        # Get remaining requests from headers

        return image_url, explanation
    else:
        # aw man, lets print some shit to the console and cry

        if COLORED_TEXT:
            print(Fore.RED + f"Error fetching data from NASA APOD API: Error {response.status_code}. Perhaps your API key is incorrect / out of requests?" + Style.RESET_ALL)
        else:
            print(f"Error fetching data from NASA APOD API: Error {response.status_code}. Perhaps your API key is incorrect / out of requests?")

        return None, None


# pick a random space fact from the txt file (yes i used chatgpt for the facts, what u gonna do)
def pick_space_fact():
    with open("data/space_facts.txt", "r") as f:
        return r.choice(f.readlines()).strip()


# Some test cases
if __name__ == "__main__":
    print(fetch_exoplanet_data("OGLE-TR-10"))