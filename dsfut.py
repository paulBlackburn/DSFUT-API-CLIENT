import requests
import time
import hashlib
import sys

class DSFUT:
    def __init__(self, console, partner_id, secret_key, max_buy, min_buy):
        assert isinstance(console, str)
        assert isinstance(partner_id, str)
        assert isinstance(secret_key, str)
        assert isinstance(max_buy, int)
        assert isinstance(min_buy, int)
        self.console = console
        self.partner_id = partner_id
        self.secret_key = secret_key
        self.max_buy = max_buy  
        self.min_buy = min_buy      

    def hash(self):
        str2hash = self.partner_id + self.secret_key + self.timestamp
        result = hashlib.md5(str2hash.encode())
        return result.hexdigest()
    
    def get(self):
        self.timestamp = str(int(time.time()))
        signature = self.hash()
        url = "https://dsfut.net/api/21/" + self.console + "/" + self.partner_id + "/" + str(self.timestamp) +  "/" + signature + "/"
        params = {
            "min_buy": self.min_buy,
            "max_buy": self.max_buy
            }
        response = requests.get(url, params=params)
        print(response.url)
        assert response
        d = response.json()
        error = d["error"]
        if error == "throttle":
            print(d)
            time.sleep(30)
        elif error != "empty":
            print(d)
            return False
        return True

if __name__ == "__main__":
    assert len(sys.argv) >= 5
    console = sys.argv[1]
    assert console in ["ps", "xb", "pc"]
    partner_id = sys.argv[2]
    secret_key = sys.argv[3]
    max_buy = int(sys.argv[4])
    min_buy = 0
    if len(sys.argv) >= 6:
        min_buy = int(sys.argv[5])
    dsfut = DSFUT(console, partner_id, secret_key, max_buy, min_buy)
    while dsfut.get():
        time.sleep(.25)