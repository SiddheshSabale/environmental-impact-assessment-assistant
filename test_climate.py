
from tools.geo import geocode_location
from tools.climate import get_climate_data

location = geocode_location("Pune, Maharashtra, India")

data = get_climate_data(
    location["latitude"],
    location["longitude"],
)

print(data)
