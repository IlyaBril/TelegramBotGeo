from settings import SiteSettings
from site_API.utils.site_api_handler import SiteApiInterface
from requests.structures import CaseInsensitiveDict

site = SiteSettings()

headers = {"X-RapidAPI-Key": site.api_key.get_secret_value(), "X-RapidAPI-Host": site.host_api}
url = "https://" + site.host_api + "/v1/geo/locations"
params = {"radius": "50", "limit": "5", "types": "city", "languageCode": "ru", "sort": "-population"}

site_api = SiteApiInterface()

url_geo = "https://api.geoapify.com/v2/places?&apiKey="\
          + site.geo_api_key + "&conditions=access&filter=circle:"

url_geo_rev = "https://api.geoapify.com/v1/geocode/reverse?&format=json&apiKey=3b6995fba84146909e2b65f0f8efacaf&"

params_geo = None
headers_geo = CaseInsensitiveDict()
headers_geo["Accept"] = "application/json"