from requests.structures import CaseInsensitiveDict
from settings import site

url_places = "https://api.geoapify.com/v2/places"
map_static_url = "https://maps.geoapify.com/v1/staticmap?apiKey=" + site.geo_api_key

params_geo = None
headers_geo = CaseInsensitiveDict()
headers_geo["Accept"] = "application/json"
