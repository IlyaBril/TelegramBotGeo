import requests


def _make_response(method: str, url: str, headers: dict, params: dict,
                   timeout: int, success=200):
    try:
        response = requests.request(
            method,
            url,
            headers=headers,
            params=params,
            timeout=timeout
        )
    except Exception as err:
        return 

    status_code = response.status_code

    if status_code == success:
        return response
    print(url)
    print(headers)

    return status_code


def _cities_near_location(method: str, url: str, headers: dict, params: dict,
                          location: str, timeout: int, func=_make_response):
    location = str(location[0]) + '+' + str(location[1])

    url = "{}/{}/nearbyCities".format(url, location)
    response = func(method, url, headers=headers,
                    params=params, timeout=timeout)

    return response


def _places_near_location(method: str, url: str, headers: dict, params: dict,
                          location: tuple, timeout: int, func=_make_response):

    url = "{}/{}/nearbyPlaces".format(url, location)
    response = func(method, url, headers=headers,
                    params=params, timeout=timeout)

    return response

def _tourist_places(method: str, url: str, headers: dict,
                    timeout: int, func=_make_response):

    response = func(method, url, headers=headers,
                    params=None, timeout=timeout)
    return response


class SiteApiInterface():

    @staticmethod
    def get_cities_nearby():
        return _cities_near_location

    @staticmethod
    def get_tourist_places():
        return _tourist_places




if __name__ == "__main__":
    _make_response()
    _cities_near_location()
    _places_near_location()
    _tourist_places()

    SiteApiInterface()
