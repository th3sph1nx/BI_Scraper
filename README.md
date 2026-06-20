A lightning-fast, headless Python CLI tool that bypasses frontend JavaScript to fetch live bus schedules, pricing, and seat availability directly from the BusIndia internal API.

Unlike traditional web scrapers that rely on slow browser automation (like Selenium or Playwright) to navigate date pickers and JavaScript rendering, this tool communicates directly with BusIndia's internal POST API. It processes the raw server response using `BeautifulSoup` to deliver instant results.

## Features

* **Lightning Fast:** Bypasses the UI entirely, returning results in milliseconds.
* **Headless:** Runs purely on Python `requests`, requiring no browser binaries.
* **CLI Interface:** Easily query routes and dates directly from the terminal.
* **Clean Data:** Extracts Operator, Bus Type, Departure, Arrival, Fare, and Live Seat Availability.

## Prerequisites

You will need Python 3.x installed. Install the required dependencies:

`pip install requests beautifulsoup4`

## Usage

Run the script from your terminal by providing the route and the journey date (`DD/MM/YYYY`).

**Basic Syntax:**

`python scraper.py <route> <date>`

**Example 1: Pondicherry to Karaikal**

`python scraper.py py-to-kai 20/06/2026`

**Example 2: Karaikal to Pondicherry**

`python scraper.py kai-to-py 25/06/2026`

## Adding New Routes

To add new cities to the scraper, you must intercept the internal `hiddenFromPlaceID` and `hiddenToPlaceID` codes from the BusIndia network tab and add them to the `CITIES` dictionary at the top of the script. 

## Disclaimer

This project is built strictly for **educational purposes** to demonstrate API reverse-engineering and headless web scraping techniques. It is not intended for commercial use. Scraping commercial booking sites may violate their Terms of Service. Use responsibly and do not spam the server.
