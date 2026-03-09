from settings import site
from pydantic import BaseModel, SecretStr


class URLFilterUnit(BaseModel):
    categories: str = 'entertainment.museum'
    lat: float = 55.755864
    lon: float = 37.617698
    limit: int = 5
    radius: int = 5000
    conditions: str = "access"
    lang: str = "ru"
    apiKey: SecretStr = site.geo_api_key
    sort: str = "desc"


class URLFilter:
    def __init__(self):
        self.user_settings = {}

user_settings = {}

params_2 = {'center': {'lat': 55.755864, 'lon': 37.617698},
 'height': 400,
 'markers': [{'color': '#ff0000',
              'contentsize': '22',
              'lat': 55.7594987,
              'lon': 37.6109983,
              'size': '42',
              'text': '1'},
             {'color': '#ff0000',
              'contentsize': '22',
              'lat': 55.7592282,
              'lon': 37.6247043,
              'size': '42',
              'text': '2'},
             {'color': '#ff0000',
              'contentsize': '22',
              'lat': 55.7549621,
              'lon': 37.6218197,
              'size': '42',
              'text': '3'},
             {'color': '#ff0000',
              'contentsize': '22',
              'lat': 55.75466315,
              'lon': 37.61296673603541,
              'size': '42',
              'text': '4'},
             {'color': '#ff0000',
              'contentsize': '22',
              'lat': 55.7445247,
              'lon': 37.6130408,
              'size': '42',
              'text': '5'}],
 'scaleFactor': 2,
 'style': 'osm-bright',
 'width': 600,
 'zoom': 14}
