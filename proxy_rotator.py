import requests
from fp.fp import FreeProxy

class ProxyEngine:
    def __init__(self):
        self.proxy_list = []
        self.update_proxies()
    
    def update_proxies(self):
        """Fetch unlimited free proxies"""
        try:
            self.proxy_list = FreeProxy().get_proxy_list()
        except:
            # Fallback proxy list
            self.proxy_list = [
                'http://proxy1:8080',
                'http://proxy2:3128',
                'socks5://proxy3:9050'
            ]
    
    def get_random_proxy(self):
        """Rotate proxies for anonymity"""
        return random.choice(self.proxy_list) if self.proxy_list else None