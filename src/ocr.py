import re
import easyocr
reader = easyocr.Reader(['en'])

def extract_fields(image_path):
    result = reader.readtext(image_path)
    
    full_text = ' '.join([d[1] for d in result])
    full_text = full_text.upper()
    all_dates = re.findall(r'\d{2}/\d{2}/\d{4}', full_text)
    possible_names = re.findall(r'\b[A-Z]{2,}(?:\s+[A-Z]{2,})+\b', full_text)

    ignore_words = {
    "CARD", "IDENTIFICATION", "IDENTITY",
    "LICENSE", "LICENCE", "DRIVING",
    "PASSPORT", "NATIONAL",
    "GOVERNMENT", "GOVT",
    "REPUBLIC", "STATE", "COUNTRY",
    "USA", "UAE", "INDIA",
    "EMIRATES", "AUTHORITY",

    "ID", "NO", "NUMBER",
    "DOB", "EXP", "ISS",
    "SEX", "HEIGHT", "HGT",
    "EYES", "HAIR", "DOB:",
    "DATE", "BIRTH",

    "ADDRESS", "STREET", "ROAD",
    "CITY", "STATE", "ZIP",
    "POSTAL", "CODE",

    "REAL", "PURPOSES",
    "DONOR", "ORGAN",

    "MALE", "FEMALE",
    "M", "F",

    "SIGNATURE", "HOLDER",
    "NATIONALITY",

    "DEPARTMENT", "MINISTRY",
    "TRANSPORT", "TRAFFIC",

    "VISIT", "VISITOR",

    "DOCUMENT", "OFFICIAL",

    "THE", "AND", "FOR"

    }

    filtered = []

    for name in possible_names:
        words = name.split()
        if len(words) < 2 or len(words) > 4:
            continue
        if any(word in ignore_words for word in words):
            continue
        filtered.append(name)
    filtered = list(set(filtered))

    return {
    'name': filtered[0] if filtered else None,
    'dates': all_dates,
    }


if __name__ == "__main__":
    fields = extract_fields("../research/sample_card.jpg")
    print(fields)

