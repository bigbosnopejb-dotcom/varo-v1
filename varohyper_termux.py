#!/usr/bin/env python3
"""
VaroHyper (Termux) - Menu terminal untuk Termux (Android)

Perubahan:
- Angka menu diwarnai merah.
- Judul "Tols" dipindahkan ke posisi di atas kotak/pembatas menu.
- Kotak menu tetap berwarna hijau; jarak antar item dipertahankan.
- ASCII art di atas menu diganti sesuai input baru dan dicetak dengan setengah merah / setengah putih (horizontal).
- Menambahkan fitur beralih otomatis ke tols2 saat memilih menu 3 dan 6.
"""
import os
import random
import sys
import time
import webbrowser
import shutil
import subprocess
import json
import re
from pathlib import Path

BG_JOBS_FILE = os.path.expanduser("~/.varohyper_bg.json")

try:
    import colorama
    colorama.init()
except Exception:
    pass

# ANSI color codes
COLORS = [
    "\033[91m",  # red
    "\033[92m",  # green
    "\033[93m",  # yellow
    "\033[94m",  # blue
    "\033[95m",  # magenta
    "\033[96m",  # cyan
    "\033[97m",  # white
    "\033[90m",  # gray
]
RESET = "\033[0m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
WHITE = "\033[97m"

# ASCII art baru (diganti sesuai permintaan)
TOLS_ASCII_BIG = """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀���⠀⠀⠀⠀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠤⣤⣄⣀⠀⢸⣿⡀⠀⠀⣀⣤⣤⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⣿⣶⣶⣶⣶⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣶⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠿⣿⣿⠿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⡿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢻⣿⣆⠀⠀⠀⠀⠀⢀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣿⣿⣿⣿⣿⣿⣇⢀⠀⠀⠀⠀⠀⢀⣾⢿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣷⣴⣀⣴⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣻⣿⣿⣿⣿⣿⢠⣁⠢⣴⣦⣴⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⡇⣿⣷⣌⠹⣿⡯⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣦⣼⠇⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠏⡿⣿⣿⣿⣿⢇⢻⣧⣼⣷⡌⠢⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠾⠛⣋⣭⣭⣶⡞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⢀⣀⣠⣤⣤⣤⣿⣿⣿⣿⣿⣿⣿⣶⣿⣭⣽⣛⠦⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣶⣿⣿⠿⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⢿⣟⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠰⣝⠛⠉⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠋⠙⠃⠑⠘⠛⡉⣹⣷⣿⡻⠿⢿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣥⡨⢁⠓⠷⢟⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢛⡅⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⠃⠀⠀⠂⠀⡈⠁⡈⠂⠀⠀⠀⠀⠀⠀⣠⢤⣤⣂⣤⣦⣤⣿⣿⣿⣿⣿⣿⣿⢿⠿⠛⠋⢩⢱⣾⣿⣿⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢀⣤⣤⣤⣤⣤⣤⣤⣤⣤⣶⣶⣿⣿⣿⠿⣿⠘⣦⣤⣤⣿⢷⠁⣷⣇⠀⠀⠀⠀⠀⣰⢦⢰⣶⡆⡴⡀⠀⠀⠀⠀⠀⡶⣼⠄⠿⣷⣤⣤⣾⠈⣿⠿⣿⣿⣿⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⡀⠀⠀
⠀⠙⠛⠛⠛⠛⠉⠛⠛⠋⠛⠛⠻⡿⢿⣿⣶⣿⠈⡟⠛⠛⣿⠂⣰⣿⣿⣗⣠⢠⠒⡉⠑⢿⢷⣿⣿⡞⠋⢟⠒⠠⣄⣺⣿⣿⣔⢰⡿⠛⠛⢿⢈⣿⣶⣿⣿⣿⠻⠟⠉⠙⠛⠛⠛⠛⠛⠛⠋⠁⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⡄⡄⠀⠀⠀⡞⠉⠉⠉⠁⢇⠉⢀⢀⠛⢻⣿⣿⡿⠞⠃⡀⠀⠪⡀⠈⠉⠉⠌⡸⠀⠀⠀⠸⢸⣿⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⢸⣿⣿⣧⠱⠀⠀⠀⠹⣌⠐⠐⠊⠀⠠⡘⡋⣒⡁⢌⡉⠀⠀⠀⠹⢈⠀⠈⠑⠂⡂⣰⠃⠀⠀⢀⠆⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⢻⣿⣿⣆⢀⠀⠀⠀⠹⢰⡀⡄⠆⠀⠾⠣⣿⢿⢢⡠⣠⡷⣓⢽⡳⠤⠰⡠⢰⡇⠁⠀⠀⠀⠎⡼⠿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠚⠷⡖⣶⣶⣴⣦⣤⣤⣤⣄⣀⣀⣛⣛⣿⣆⣡⡀⠀⠈⠸⠆⠣⠀⠀⠀⡒⠰⠦⢶⣠⣶⠶⠆⣂⣀⣀⠀⡇⣘⣃⣀⣀⣀⣊⣘⣼⡼⠎⠩⡀⢢⠢⠆⠒⠔⠒⠉⠋⠀⠈⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠙⠛⠛⠛⢛⠛⣟⣿⣿⡟⢿⣿⠿⣿⠿⢿⠿⠿⢿⠿⠿⣿⢿⣿⠿⠿⡿⠿⠿⠿⠿⢿⢿⣿⠟⣿⣿⣿⡛⠇⠀⠀⠀⠀��⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠈⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠢⡙⢿⡟⢻⣦⣉⠢⠘⡄⢿⣦⡀⢘⠿⢛⠮⠭⢷⡛⢟⡁⢀⣴⡟⣰⠃⠜⣡⣾⡛⢻⣿⣷⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣹⣷⣄⡙⢿⣿⣿⣷⣤⠀⢄⡉⠛⣃⣀⡴⠒⢛⠲⢤⣀⠘⠋⢉⡠⢁⣴⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⡿⠋⠛⠋⠂⢈⠛⠿⣿⣷⣤⣉⠻⠟⢁⢀⣠⣤⣄⣀⠉⠿⢛⣁⣤⣾⣿⣿⣿⠿⠋⠹⠛⢿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⡿⠏⠀⠀⠀⠀⠀⠀⠁⠀⠬⣉⠛⠻⢿⣿⣿⣿⣿⣉⣿⣿⣿⣿⣿⣿⣿⠿⠟⠉⠁⠀⠀⠀⠀⠀⠈⠿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠒⠨⢭⣭⣿⣿⠟⠛⠛⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡼⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⣿⣿⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
���⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""

# tols commands (exact as requested)
WA_TOLS = """
apt update && apt upgrade -y
pkg install python git -y
pip install colorama
git clone https://github.com/XPH4N70M/WA_CRASHER
cd WA_CRASHER
python3 WA_CRASHER.py
"""

HXP_TOLS = """
pkg update && pkg upgrade -y
pkg install git -y
pkg install lolcat -y
git clone https://github.com/hackerxphantom/HXP-DUCKY
cd $HOME
cd HXP-DUCKY
ls
bash hxp_ducky.sh
"""


def rand_color():
    return random.choice(COLORS)


def colored(text):
    return f"{rand_color()}{text}{RESET}"


def clear_screen():
    os.system("clear")


def strip_ansi(s: str) -> str:
    """Remove ANSI escape sequences for correct width calculation."""
    return re.sub(r'\x1b\[[0-9;]*m', '', s)


def open_url_termux(url):
    if shutil.which("termux-open-url"):
        cmd = f"termux-open-url '{url}'"
        code = os.system(cmd)
        if code == 0:
            print(colored(f"[✓] Membuka: {url} (termux-open-url)"))
            return
    if shutil.which("am"):
        cmd = f'am start -a android.intent.action.VIEW -d "{url}" >/dev/null 2>&1'
        code = os.system(cmd)
        if code == 0:
            print(colored(f"[✓] Membuka: {url} (Android intent)"))
            return
    try:
        webbrowser.open_new_tab(url)
        print(colored(f"[✓] Membuka via webbrowser: {url}"))
    except Exception as e:
        print(colored(f"[!] Gagal membuka URL: {e}"))


def run_cmd(cmd, cwd=None):
    print(colored(f"[> ] {cmd}"))
    try:
        completed = subprocess.run(cmd, shell=True, cwd=cwd)
        return completed.returncode
    except KeyboardInterrupt:
        print(colored("[!] Dibatalkan oleh pengguna."))
        return 130
    except Exception as e:
        print(colored(f"[!] Error menjalankan perintah: {e}"))
        return 1


def run_bash_commands_background(commands: str):
    """Start commands in a detached background process and return immediately.
    Uses setsid so the process is detached from this terminal. Prints PID.
    """
    try:
        proc = subprocess.Popen(["bash", "-lc", commands], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, preexec_fn=os.setsid)
        print(colored(f"[→] Tols2 sedang berjalan di background (PID: {proc.pid}). Anda kembali ke menu."))
        return proc.pid
    except Exception as e:
        print(RED + f"[!] Gagal memulai proses background: {e}" + RESET)
        return None


# Helper: warna separuh ASCII art (horizontal/vertical)
def color_ascii_half(ascii_art: str, first_color: str = RED, second_color: str = WHITE, mode: str = "horizontal") -> str:
    """
    Warnai ascii_art menjadi dua bagian:
      - mode="horizontal" : baris atas = first_color, baris bawah = second_color
      - mode="vertical"   : kolom kiri = first_color, kolom kanan = second_color (approx; memotong pada tengah panjang baris terpanjang)
    Mengembalikan string dengan kode ANSI warna dan reset setiap baris.
    """
    if not ascii_art:
        return ""
    if mode == "horizontal":
        lines = ascii_art.splitlines(True)
        n = len(lines)
        half = n // 2
        out_lines = []
        for i, ln in enumerate(lines):
            color = first_color if i < half else second_color
            if ln.endswith("\n"):
                content = ln[:-1]
                out_lines.append(f"{color}{content}{RESET}\n")
            else:
                out_lines.append(f"{color}{ln}{RESET}")
        return "".join(out_lines)
    elif mode == "vertical":
        lines = ascii_art.splitlines()
        maxw = max((len(ln) for ln in lines), default=0)
        mid = maxw // 2
        out_lines = []
        for ln in lines:
            padded = ln.ljust(maxw)
            left = padded[:mid]
            right = padded[mid:]
            out_lines.append(f"{first_color}{left}{RESET}{second_color}{right}{RESET}\n")
        return "".join(out_lines)
    else:
        return ascii_art

# (Background/job helpers and other functions unchanged — keep as in previous script)
# For brevity in this message I keep other functions (load_bg_jobs, save_bg_jobs, start_bg_process, list_bg_jobs,
# stop_bg_job, install_and_run_otp, run_video_downloader, etc.) unchanged. They should be copied verbatim from your existing file.
# --- START copy the rest of your previous helper functions here (unchanged) ---
# (Place the functions load_bg_jobs, save_bg_jobs, start_bg_process, list_bg_jobs, stop_bg_job,
#  install_and_run_otp, run_video_downloader exactly as in your current script)
# --- END copy ---

def print_menu():
    clear_screen()
    # Title
    print(colored("=== VaroHyper (Termux) ==="))
    menu_items = [
        ("1", "Tiktok Varo", "https://www.tiktok.com/@_rohyper"),
        ("2", "Tols Otp (install & run)", None),
        ("3", "Wa Crasher", None),
        ("4", "Video Downloader", None),
        ("5", "Crash Virus", None),
        ("6", "Virus Duck", None),
        ("7", "HackMenu", None),
    ]

    # Print ASCII art (now using color split: atas merah, bawah putih)
    if TOLS_ASCII_BIG:
        print(color_ascii_half(TOLS_ASCII_BIG, first_color=RED, second_color=WHITE, mode="horizontal"))

    # Print the TOLS title above the menu box
    print(f"{GREEN}Tols{RESET}")
    print()  # small gap

    # Build box lines. We include ANSI for the bracketed number (red), but strip_ansi() will remove it when measuring width.
    box_lines = []
    box_lines.append("Menu Utama")
    box_lines.append("")  # blank line inside box after header

    for key, name, url in menu_items:
        colored_key = f"{RED}{key}{RESET}"
        line = f"[{colored_key}] {name}"
        box_lines.append(line)
        box_lines.append("")  # paragraph gap after each menu item

    colored_zero = f"{RED}0{RESET}"
    box_lines.append(f"[{colored_zero}] Keluar / q")

    # determine width using strip_ansi to ignore color codes
    visible_widths = [len(strip_ansi(line)) for line in box_lines]
    maxw = max(visible_widths) if visible_widths else 0
    padding = 2
    inner_width = maxw + padding * 2

    # draw top border (green)
    print(f"{GREEN}┌{'─' * inner_width}┐{RESET}")
    # draw each line with green vertical borders
    for ln in box_lines:
        content = " " * padding + ln.ljust(maxw) + " " * padding
        print(f"{GREEN}│{RESET}{content}{GREEN}│{RESET}")
    # bottom border (green)
    print(f"{GREEN}└{'─' * inner_width}┘{RESET}")
    print()  # spacing after box

    # Footer divider (green)
    print(f"{GREEN}{'═' * (inner_width + 2)}{RESET}")
    print()
    print(f"{GREEN}Idea{RESET} : {WHITE}Varo4Cee{RESET}")
    print()
    print(f"{GREEN}Creating{RESET} : githubcopilot")
    print()
    note_lines = [
        "note : Jika ingin kembali ke menu utama saat memilih tols:",
        "  - Tekan Ctrl+Z untuk menghentikan sementara tool",
        "  - Lalu jalankan kembali: python varohyper_termux.py"
    ]
    for ln in note_lines:
        print(YELLOW + ln + RESET)
    print()


def main_loop():
    while True:
        print_menu()
        try:
            choice = input(colored("Pilih menu (1-7) > ")).strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\n" + colored("Dihentikan oleh pengguna."))
            break
        if choice in ("0", "q", "exit"):
            print(colored("Keluar..."))
            time.sleep(0.3)
            break
        if choice == "1":
            open_url_termux("https://www.tiktok.com/@_rohyper")
        elif choice == "2":
            install_and_run_otp()
        elif choice == "3":
            # Auto-switch to tols2: run WA_TOLS in background
            print(colored("[~] Mengalihkan ke Tols2 (WA_CRASHER) — memulai..."))
            pid = run_bash_commands_background(WA_TOLS)
            if pid:
                print(colored(f"[→] WA_CRASHER berjalan di PID {pid} (background)."))
                time.sleep(1)
        elif choice == "4":
            run_video_downloader()
        elif choice == "5":
            print(RED + "[!] Crash Virus - Fitur dalam pengembangan" + RESET)
            input(colored("Tekan Enter untuk kembali ke menu..."))
        elif choice == "6":
            # Auto-switch to tols2: run HXP_TOLS in background
            print(colored("[~] Mengalihkan ke Tols2 (HXP-DUCKY) — memulai..."))
            pid = run_bash_commands_background(HXP_TOLS)
            if pid:
                print(colored(f"[→] HXP-DUCKY berjalan di PID {pid} (background)."))
                time.sleep(1)
        elif choice == "7":
            print(RED + "[!] HackMenu - Fitur dalam pengembangan" + RESET)
            input(colored("Tekan Enter untuk kembali ke menu..."))
        else:
            print(colored("[!] Pilihan tidak dikenal. Coba lagi."))
            input(colored("Tekan Enter untuk kembali ke menu..."))

if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        print("\n" + colored("Dihentikan oleh pengguna. Sampai jumpa!"))
        sys.exit(0)
