import requests


def _make_response(method: str, url: str, headers: dict,
                   params: dict, timeout: int, success=200):
    try:
        response = requests.request(
            method,
            url,
            headers=headers,
            params=params,
            timeout=timeout
        )
    except Exception as err:
        print('response no places', response)
        return 

    status_code = response.status_code

    if status_code == success:
        return response
    print(url)
    print(headers)

    return status_code


def _tourist_places(method: str, url: str, headers: dict,
                    timeout: int, func=_make_response):

    response = func(method, url, headers=headers,
                    params=None, timeout=timeout)
    return response


class SiteApiInterface():

    @staticmethod
    def get_tourist_places():
        return _tourist_places