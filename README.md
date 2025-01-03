# *THIS IS A WORK IN PROGRESS. IF YOU TRY TO INSTALL IT NOW, NOTHING WILL HAPPEN*
# CosmoLens
CosmoLens is the perfect tool for fetching exoplanet data from NASA's exoplanet archive API. <br>
It even shows you the APOD (Astrology Picture of the Day), using NASA's APOD API. <br>

## Usage
To use this application, install the following Python packages: `Colorama` (for colored text) and `Requests` (to fetch the data from the NASA APIs). <br>
Next, download the source code as ZIP or run `git clone https://github.com/hellonearth311/CosmoLens.git`. <br>
### This next step is very important:
In the main directory of the program, create a `settings.json` file and paste the following code in:
```
{
  "hd_photos": true,
  "theme": "system",
  "api_key": "YOUR_API_KEY",
  "colored_console_text": true
}
```
Now, you can customize the settings as you want. Below is the explanation for each setting. <br>
<br>
`hd_photos`: Fetch HD photos from the NASA APOD API when available. <br>
`theme`: To use dark, light, or system theme for the app. <br>
`api_key`: The most **important** setting. Paste your NASA API key here. If you don't, the app **won't** work. <br>
`colored_console_text`: Print out colored text in the debug console. <br>

### BuT wHY dOn'T yOu jUsT inCLuDe tHe sETtinGs fIlE iN tHe rEpO?
I don't include it in the repo because the settings file contains the `api_key` setting, and including it would mean giving away my API key for free, which is NOT happening.

### What next?
Now, just run `main.py`, and you should be good to go!
