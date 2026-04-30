import requests
from requests.exceptions import HTTPError

class BaseAPIClient:
    """
    A generic wrapper around the requests library to handle common API operations,
    session management, and error handling.
    """

    def __init__(self, base_url: str, token: str):
        self.base_url = base_url.rstrip('/') # Ensure no trailing slash
        
        # Using a Session persists headers across all requests made by this client
        self.s = requests.Session()
        self.s.headers.update({
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.v3+json", # GitHub recommended header
            "Content-Type": "application/json"
        })

    def _handle_response(self, res: requests.Response):
        """
        Helper method to handle HTTP errors and parse JSON.
        """
        try:
            # This will raise an exception for 4xx and 5xx status codes
            res.raise_for_status()
            
            # If the response is empty (like a 204 No Content for deletion), return True
            if not res.text:
                return True
                
            return res.json()
            
        except HTTPError as e:
            # If GitHub returns an error, this captures their specific error message
            error_msg = f"HTTP Error: {e}\nResponse Body: {res.text}"
            raise Exception(error_msg)

    def get(self, endpoint: str, params: dict = None):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        res = self.s.get(url, params=params)
        return self._handle_response(res)

    def post(self, endpoint: str, payload: dict = None):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        res = self.s.post(url, json=payload)
        return self._handle_response(res)

    def delete(self, endpoint: str):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        res = self.s.delete(url)
        return self._handle_response(res)