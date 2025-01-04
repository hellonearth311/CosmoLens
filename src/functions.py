import random as r
import json
import requests
from colorama import Fore, Style
import pandas as pd
import os

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

# the meat and potatoes of the app - the function which fetches the data of the exoplanet
def fetch_all_exoplanet_data_to_csv(output_file="all_exoplanets.csv", clean_data=True):
    """
    Fetch all exoplanet data from the NASA Exoplanet Archive API and save it to a CSV file.
    :param output_file: Filename to save the data (default is all_exoplanets.csv).
    :param clean_data: Clean the data which has been fetched from the NASA API to only include relevant columns.
    :return: None
    """

    if os.path.exists(output_file):
        print_colored(f"Data already exists. If you are confident it does not, delete the {output_file} file.", Fore.CYAN)
        print_remaining_requests()
        return
    else:
        print_colored("Path doesn't exist. Creating new data...", Fore.CYAN)
        # Base URL for the API
        url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"

        # SQL query to fetch all exoplanet data
        query = "SELECT * FROM ps"

        # Parameters to send with the request
        params = {
            "query": query,
            "format": "json",
        }

        try:
            # Send the GET request
            print_colored("Fetching data from API...", Fore.CYAN)
            response = requests.get(url, params=params)
            print_remaining_requests()  # Monitor API usage

            # Check response status
            if response.status_code == 200:
                print_colored("Data fetched!", Fore.GREEN)
                # Parse JSON response into a Python list of dictionaries
                data = response.json()

                if data:
                    # Convert data to a Pandas DataFrame
                    df = pd.DataFrame(data)

                    print_colored("Writing data to CSV file...", Fore.CYAN)

                    # Save the DataFrame to a CSV file
                    df.to_csv(output_file, index=False)

                    print_colored(f"Data for all exoplanets saved to {output_file}. Total records: {len(data)}", Fore.GREEN)
                else:
                    print_colored("No data found in the NASA Exoplanet Archive.", Fore.LIGHTRED_EX)
            else:
                print_colored(f"Error fetching data: Status code {response.status_code}. Perhaps your API key is incorrect / out of requests?", Fore.RED)
        except Exception as e:
            print_colored(f"An error occurred while fetching data: {str(e)}. Perhaps your API key is incorrect / out of requests?", Fore.RED)

def clean_exoplanet_data(input_file="all_exoplanets.csv", output_file="all_exoplanets.csv"):
    """
    Clean the exoplanet data by keeping only relevant columns and save it to a new CSV file.
    :param input_file: The CSV file containing the full exoplanet dataset (default: all_exoplanets.csv).
    :param output_file: The filename to save the cleaned dataset (default: cleaned_exoplanets.csv).
    :return: None
    """

    # Relevant columns to keep
    relevant_columns = [
        'pl_name',  # Exoplanet name
        'hostname',  # Host star name
        'pl_orbper',  # Orbital period (days)
        'pl_rade',  # Planet radius (Earth radii)
        'pl_bmasse',  # Planet mass (Earth masses)
        'pl_orbsmax',  # Orbital semi-major axis (AU)
        'pl_eqt',  # Equilibrium temperature (Kelvin)
        'st_teff',  # Host star effective temperature (Kelvin)
        'st_mass',  # Host star mass (solar masses)
        'st_rad',  # Host star radius (solar radii)
        'discoverymethod',  # Discovery method
        'discoveryyear',  # Year of discovery
    ]

    try:
        # Read the input CSV into a Pandas DataFrame
        df = pd.read_csv(input_file)

        # Filter the DataFrame to include only relevant columns
        cleaned_df = df[relevant_columns]

        # Save the cleaned DataFrame to a new file
        cleaned_df.to_csv(output_file, index=False)

        print_colored(f"Cleaned data has been saved to {output_file}. Total records: {len(cleaned_df)}", Fore.GREEN)
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' does not exist.", Fore.YELLOW)
    except KeyError as e:
        print(f"Error: Some columns were not found in the dataset. Missing column(s): {str(e)}", Fore.LIGHTYELLOW_EX)
    except Exception as e:
        print(f"An error occurred while cleaning the data: {str(e)}", Fore.RED)


# grab a sweet, sweet, apod from the nasa api
def fetch_apod():
    """
    Fetch the Astrology Photo of the Day from NASA APOD API.
    :return: The URL of the image and the explanation of the image.
    """
    url = f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}&hd={HD_PHOTOS}"
    print(url)

    print_colored("Fetching data...", Fore.CYAN)

    response = requests.get(url)
    print_remaining_requests()

    # did it work
    if response.status_code == 200:
        print_colored("Data fetched!", Fore.GREEN)
        # les go
        data = response.json()

        image_url = data["url"]
        explanation = data["explanation"]

        # Get remaining requests from headers

        return image_url, explanation
    else:
        # aw man, lets print some shit to the console and cry
        print_colored(f"Error fetching data from NASA APOD API: Error {response.status_code}. Perhaps your API key is incorrect / out of requests?", Fore.RED)

        return None, None


# pick a random space fact from the txt file (yes i used chatgpt for the facts, what u gonna do)
def pick_space_fact():
    with open("../data/space_facts.txt", "r") as f:
        return r.choice(f.readlines()).strip()


# Some test cases
if __name__ == "__main__":
    fetch_all_exoplanet_data_to_csv("../data/exoplanets.csv")