import requests

API_CODE = "aa18a4cc0c67e655e37ddba5915217d4"
BASE_LINK = "http://api.openweathermap.org/data/2.5/weather"

city = input("Which city do want to know the weather from?: ")
city_input = f"{BASE_LINK}?appid={API_CODE}&q={city}"
api_response = requests.get(city_input)

if api_response.status_code == 200:
    data = api_response.json()
    weather = data["weather"][0]["description"]
    temperature = round(data["main"]["temp"] - 273.15)

    print("Weather: ", weather, "\nTemperature: ", temperature, "celsius")
    
else:
    print("Something isn't right.")