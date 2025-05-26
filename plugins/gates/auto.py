import requests

def check_and_add_site(card, site_url, email=None, proxy="prox-au.pointtoserver.com:10799:purevpn0s9161585:E7n0nNSvISnTr7", shipping=False):
    try:
        url = "https://api.voidapi.xyz/v2/shopify_graphql"
        payload = {
            "key": "VDX-SHA2X-NZ0RS-O7HAM",
            "data": {
                "card": card,
                "product_url": site_url,
                "email": email,  
                "proxy": proxy,
                "ship_address": None,
                "is_shippable": shipping
            }
        }

        response = requests.post(url, json=payload, timeout=30)
        data = response.json()

        status = data.get("status", "").lower()
        msg = data.get("message") or data.get("response") or data.get("error") or "No response"

        if "processedreceipt" in status or "charged" in msg.lower():
            return True, msg, data
        else:
            return False, msg, data

    except Exception as e:
        return False, f"Request failed: {e}", {}
