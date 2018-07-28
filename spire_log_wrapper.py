import requests

base_url = 'https://spirelogs.com/'
profile = base_url + 'pages/profile.php'
upload = base_url + 'multiupload.php'


class SpireLogWrapper:
    def __init__(self):
        self.jar = None

    def login(self, username, password):
        req = requests.post(profile, {'action': 'login', 'username': username, 'password': password})
        self.jar = req.cookies
        return True if username in req.text else False

    def upload_run(self, file):
        file = {
            'file': open(file, 'rb')}
        req = requests.post(upload, files=file, cookies=self.jar)
        if 'successfully' in req.text or 'recorded' in req.text:
            return True
        else:
            return False
