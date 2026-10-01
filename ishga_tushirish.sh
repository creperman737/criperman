#!/bin/bash

# Dastur joylashgan papkaga o'tish
# Bu skript istalgan joydan chaqirilganda ham ishlaydi.
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

echo "Shaxsiy Kalkulyator ishga tushmoqda..."

# Agar virtual muhit (venv) ishlatsangiz, uni shu yerda faollashtiring:
# source venv/bin/activate

# Python kodini ishga tushirish
python3 kalkulyator.py

echo "Dastur tugadi."