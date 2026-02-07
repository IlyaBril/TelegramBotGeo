from json import JSONDecoder, JSONEncoder

import requests


def _make_response(method: str, url: str, headers: dict,
                   timeout: int, params=None, success=200):
    """
    Function makes request to url and returns response if success
    or error code
    """
    try:
        response = requests.request(
            method,
            url,
            headers=headers,
            params=params,
            timeout=timeout
        )

    except Exception as err:  #ReadTimeout
        print('response no places', err)
        return 400

    status_code = response.status_code

    if status_code == success:
        return response

    return status_code


class SiteApiInterface:
    @staticmethod
    def get_tourist_places():
        return _make_response
