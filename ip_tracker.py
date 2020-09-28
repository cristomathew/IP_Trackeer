import geoip2.database
import socket
import pandas as pd
import geopandas as gpd
import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import matplotlib.pyplot as plt
import plotly_express as px
import tqdm
from tqdm.notebook import tqdm_notebook

def is_valid_ipv4_address(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:  # not a valid address
        return False

    return True

def is_valid_ipv6_address(address):
    try:
        socket.inet_pton(socket.AF_INET6, address)
    except socket.error:  # not a valid address
        return False
    return True

def check_ip(ip):
    return is_valid_ipv4_address(ip) or is_valid_ipv6_address(ip)

def plot(lat,lon):
    locator = Nominatim(user_agent="myGeocoder")
    coordinates = lat, lon
    location = locator.reverse(coordinates)
    print("Address:",location.address)

reader = geoip2.database.Reader('./GeoLite2-City_20200922/GeoLite2-City.mmdb')
city = input("Enter ip:")

if check_ip(city):
    response = reader.city(city)
    print("\n****DETAILS****\n")
    print("Country iso code:",response.country.iso_code)
    print("Country.name:",response.country.name)
    print("State:",response.subdivisions.most_specific.name)
    print("State Code:",response.subdivisions.most_specific.iso_code)
    print("District:",response.city.name)
    print("Postal Code:",response.postal.code)
    print("Latitude:",response.location.latitude)
    print("Longitude:",response.location.longitude)
    plot(response.location.latitude,response.location.longitude)
else:
    print("wrong ip")
print("\n***END***\n")
reader.close()