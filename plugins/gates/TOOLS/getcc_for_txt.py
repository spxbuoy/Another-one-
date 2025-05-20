import re

# Regex: Matches formats like 4111111111111111|12|25|123 or with : or spaces
CC_PATTERN = re.compile(r"(\d{12,16})[|:\s](\d{1,2})[|:\s](\d{2,4})[|:\s](\d{3,4})")

async def getcc_for_txt(file_path, role):
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.read().splitlines()

        valid_ccs = []
        seen = set()

        for line in lines:
            match = CC_PATTERN.search(line)
            if match:
                cc, mes, ano, cvv = match.groups()

                # Basic validation
                mes = mes.zfill(2)
                if not 1 <= int(mes) <= 12:
                    continue
                ano = ano[-2:] if len(ano) == 4 else ano
                fullz = f"{cc}|{mes}|{ano}|{cvv}"

                if fullz not in seen:
                    valid_ccs.append({
                        "fullz": fullz,
                        "raw": line.strip()
                    })
                    seen.add(fullz)

        if not valid_ccs:
            return False, "❌ No valid CC found in your file."

        if role == "FREE":
            valid_ccs = valid_ccs[:20]

        return True, valid_ccs

    except Exception as e:
        return False, f"❌ Error reading or processing the file.\n{str(e)}"