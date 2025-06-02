import aiohttp
import asyncio

async def async_auth_func(card: str, proxy: str = None):
    url = "https://barryxapi.xyz/str_auth"
    params = {
        "key": "BRY-HEIQ7-KPWYR-DRU67",
        "card": card
    }
    if proxy:
        params["proxy"] = proxy

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=20) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "status": data.get("status", "error"),
                        "response": data.get("message", "Unknown response")
                    }
                else:
                    return {"status": "error", "response": f"HTTP {response.status}"}
    except asyncio.TimeoutError:
        return {"status": "error", "response": "Request Timeout"}
    except Exception as e:
        return {"status": "error", "response": str(e)}
