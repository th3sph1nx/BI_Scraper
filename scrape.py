import argparse
import urllib.parse
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup

# 1. Define our static database of cities we know the internal IDs for
CITIES = {
    "py": {
        "id": "3517",
        "code": "PUU",
        "name": "PONDICHERRY",
        "info": "3517%2CPUU%2CPONDICHERRY%2CPONDICHERRY%2CPONDICHERRY",
    },
    "kai": {
        "id": "3682",
        "code": "KAI",
        "name": "KARAIKAL",
        "info": "3682%2CKAI%2CKARAIKAL%2CKARAIKAL%2CKARAIKAL",
    },
}


def fetch_bus_data(route, journey_date_str):
    url = "https://www.busindia.com/busBooking_Availability"

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "https://www.busindia.com/",
        "Origin": "https://www.busindia.com",
        "Connection": "keep-alive",
    }

    if route == "py-to-kai":
        origin = CITIES["py"]
        dest = CITIES["kai"]
    elif route == "kai-to-py":
        origin = CITIES["kai"]
        dest = CITIES["py"]
    else:
        print("Invalid route specified.")
        return

    # Date formatting
    encoded_journey_date = urllib.parse.quote(journey_date_str, safe="")

    current_date = datetime.now()
    encoded_current_date = urllib.parse.quote(
        current_date.strftime("%d/%m/%Y"), safe=""
    )
    encoded_max_date = urllib.parse.quote(
        (current_date + timedelta(days=30)).strftime("%d/%m/%Y"), safe=""
    )

    # The payload sent to server
    raw_payload = (
        f"radOnewayOrReturnTrip=O&matchFromPlace={origin['name']}&matchToPlace={dest['name']}"
        f"&matchFromPlace1=&matchToPlace1=&matchFromPlace2=&matchToPlace2=&matchFromPlace3=&matchToPlace3="
        f"&selectOnwardTimeSlab=00%3A00-23%3A59&selectReturnTimeSlab=00%3A00-23%3A59"
        f"&selectMultiTripTimeSlab1=00%3A00-23%3A59&selectMultiTripTimeSlab2=00%3A00-23%3A59&selectMultiTripTimeSlab3=00%3A00-23%3A59"
        f"&selectCorp=0&radBookingType=BUS&selectCategory=0&txtOnwardFromTime=&txtOnwardToTime=&txtReturnToTime=&txtReturnFromTime="
        f"&txtOnwardDate={encoded_journey_date}&txtReturnDate=DD%2FMM%2FYYYY"
        f"&selectFromPlace={origin['id']}&selectToPlace={dest['id']}"
        f"&hiddenFromPlaceID={origin['id']}&hiddenToPlaceID={dest['id']}"
        f"&hiddenFromPlaceName={origin['name']}&hiddenToPlaceName={dest['name']}"
        f"&hiddenFromPlaceCode={origin['code']}&hiddenToPlaceCode={dest['code']}"
        f"&hiddenFromPlaceInfo={origin['info']}&hiddenToPlaceInfo={dest['info']}"
        f"&hiddenCategoryID=&hiddenCategoryName=&hiddenTotalAdult=&hiddenTotalChildren=&hiddenTotalPassengers=1"
        f"&hiddenMaxValidReservDate={encoded_max_date}&hiddenOnwardJourneyDate={encoded_journey_date}"
        f"&hiddenReturnJourneyDate=&hiddenOnwardSearchDay=J&hiddenReturnSearchDay=J&hiddenOnwardTimeSlab=00%3A00-23%3A59"
        f"&hiddenReturnTimeSlab=&hiddenJourneyType=O&hiddenMaxNoOfPassengers=16&hiddenBusAdvSearchFlag=N"
        f"&hiddenCurrentDate={encoded_current_date}"
        f"&selectFromPlace1=&selectFromPlace2=&selectFromPlace3=&selectToPlace1=&selectToPlace2=&selectToPlace3="
        f"&hiddenFromPlaceID1=&hiddenFromPlaceID2=&hiddenFromPlaceID3=&hiddenToPlaceID1=&hiddenToPlaceID2=&hiddenToPlaceID3="
        f"&hiddenFromPlaceName1=&hiddenFromPlaceName2=&hiddenFromPlaceName3=&hiddenToPlaceName1=&hiddenToPlaceName2=&hiddenToPlaceName3="
        f"&hiddenFromPlaceCode1=&hiddenFromPlaceCode2=&hiddenFromPlaceCode3=&hiddenToPlaceCode1=&hiddenToPlaceCode2=&hiddenToPlaceCode3="
        f"&hiddenFromPlaceInfo1=&hiddenToPlaceInfo1=&hiddenFromPlaceInfo2=&hiddenToPlaceInfo2=&hiddenFromPlaceInfo3=&hiddenToPlaceInfo3="
        f"&txtMultiTripDate1=&txtMultiTripDate2=&txtMultiTripDate3=&hiddenMultiTripDate1=&hiddenMultiTripDate2=&hiddenMultiTripDate3="
        f"&hiddenMultiTripSearchDay1=&hiddenMultiTripSearchDay2=&hiddenMultiTripSearchDay3="
        f"&hiddenMultiTripTimeSlab1=&hiddenMultiTripTimeSlab2=&hiddenMultiTripTimeSlab3="
        f"&totalTrips=&txtCheckInDate=&txtCheckOutDate=&guestCount=&hiddenSelectCity=&hiddenAdult=&hiddenChild=&roomId=&childAge="
        f"&hiddenNumberOfRooms=&hiddenRoomStays=&hiddenRoomStayAge="
    )

    session = requests.Session()

    print(
        f"Fetching buses for {origin['name']} to {dest['name']} on {journey_date_str}...\n"
    )
    session.get("https://www.busindia.com/", headers=headers)
    response = session.post(url, headers=headers, data=raw_payload)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        bus_cards = soup.find_all("div", class_="products")

        if not bus_cards:
            print("No buses found for this date and route.")
            return

        extracted_data = []
        for card in bus_cards:
            try:
                operator = card.get("data-crp", "Unknown").strip()
                price = card.get("data-price", "N/A").strip()
                bus_type = card.get("data-bst", "").strip()

                dept_li = card.find("li", class_="ft2")
                departure = (
                    dept_li.find("span", class_="size15").text.strip()
                    if dept_li
                    else "N/A"
                )

                arr_li = card.find("li", class_="ft3")
                arrival = (
                    arr_li.find("span", class_="size15").text.strip()
                    if arr_li
                    else "N/A"
                )

                seats_li = card.find("li", class_="ft6")
                seats = (
                    seats_li.find("button").text.strip()
                    if seats_li and seats_li.find("button")
                    else "Sold Out"
                )
                seats = seats.replace("\xa0", " ")

                extracted_data.append(
                    {
                        "operator": operator,
                        "type": bus_type,
                        "departure": departure,
                        "arrival": arrival,
                        "price": price,
                        "seats": seats,
                    }
                )
            except Exception:
                continue

        print("-" * 80)
        for bus in extracted_data:
            print(
                f"[{bus['operator']}] {bus['type']} | {bus['departure']} -> {bus['arrival']} | Fare: ₹{bus['price']} | {bus['seats']}"
            )
        print("-" * 80)
        print(f"Total Buses Found: {len(extracted_data)}")

    else:
        print(f"❌ Failed! Server returned status code: {response.status_code}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BusIndia Headless Scraper")

    parser.add_argument(
        "route",
        choices=["py-to-kai", "kai-to-py"],
        help="Choose the direction of travel",
    )

    parser.add_argument("date", help="Date of journey in DD/MM/YYYY format")

    args = parser.parse_args()

    fetch_bus_data(args.route, args.date)
