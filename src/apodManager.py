from functions import *

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

def download_image_from_url(url, file_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(file_path, 'wb') as f:
            for chunk in response:
                f.write(chunk)
    else:
        raise Exception(f"Failed to download image with status code {response.status_code}")
