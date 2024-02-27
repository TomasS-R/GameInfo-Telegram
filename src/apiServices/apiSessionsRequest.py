import requests

class apiSession:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'})
    
    def make_request(self, url, method="GET", **kwargs):
        response = self.session.request(method, url, **kwargs)
        return response
    
    def close(self):
        self.session.close()