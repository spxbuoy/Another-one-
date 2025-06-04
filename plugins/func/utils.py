import random
import string

def randgen(length=10):
    """Generate a random alphanumeric string (uppercase letters + digits)."""
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=length))

def luhn_verify(card_number: str) -> bool:
    num = [int(d) for d in str(card_number)]
    check_digit = num.pop()
    num.reverse()
    total = 0
    for i, digit in enumerate(num):
        if i % 2 == 0:
            digit *= 2
        if digit > 9:
            digit -= 9
        total += digit
    total *= 9
    return (total % 10) == check_digit

def cc_gen(bin_base, mes='x', ano='x', cvv='x'):
    cards = []

    while len(cards) < 10:
        cc = bin_base
        while len(cc) < 15:
            cc += str(random.randint(0, 9))

        for i in range(10):
            cc_full = cc[:-1] + str(i)
            if luhn_verify(cc_full):
                break
        else:
            continue

        mes_gen = str(random.randint(1, 12)).zfill(2) if mes == 'x' else mes
        ano_gen = str(random.randint(25, 30)) if ano == 'x' else ano
        cvv_gen = str(random.randint(100, 999)) if cvv == 'x' else cvv

        card = f"{cc_full}|{mes_gen}|{ano_gen}|{cvv_gen}"
        if card not in cards:
            cards.append(card)

    return cards

# plugins/func/utils.py

async def error_log(error_msg):
    print(f"[ERROR] {error_msg}")  # Simple logging to console
import requests

def get_bin_info(bin_code):
    try:
        response = requests.get(f"https://bins.antipublic.cc/bins/{bin_code}")
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "vendor": "Unknown",
                "type": "Unknown",
                "level": "Unknown",
                "bank_name": "Unknown",
                "country": "Unknown",
                "flag": "🏳"
            }
    except:
        return {
            "vendor": "Unknown",
            "type": "Unknown",
            "level": "Unknown",
            "bank_name": "Unknown",
            "country": "Unknown",
            "flag": "🏳"
        }
async def fetch_plan(user_id: int) -> str:
    # Example dummy function. You can connect it to a real DB if needed.
    # For now, always return "FREE"
    return "FREE"