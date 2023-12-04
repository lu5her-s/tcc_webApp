import requests

class LineNotify:

    def __init__(self, token: str) -> None:
        self.token = token
        self.url = "https://notify-api.line.me/api/notify"
        self.headers = {
            "Authorization": "Bearer " + token
        }

    def send_message(self, message: str) -> requests.models.Response:
        payload = {"message": message}
        r = requests.post(self.url, headers=self.headers, data=payload)
        return r

    def send_image(self, image_path: str, message=' ') -> requests.models.Response:
        files = {
            'imageFile': open(image_path, 'rb')
        }
        payload = {
            "message": message,
        }
        session = requests.Session()
        r = session.post(self.url, headers=self.headers, data=payload, files=files)
        # r = requests.Session.post(self.url, headers=self.headers, files=files, data=payload)
        return r
