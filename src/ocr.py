import re
import easyocr

reader = easyocr.Reader(['en', 'ar'])

def extract_fields(image_path):
    result = reader.readtext(image_path)
    
    full_text = ' '.join([d[1] for d in result])
    full_text = full_text.upper()
    
    # dates
    #all_dates = re.findall(r'\d{2}[/-]\d{2}[/-]\d{4}', full_text)
    dob_match = re.search(r'(?:DOB|BIRTH|BORN|BLRTH|BIRT)\s+(\d{2}[/-]\d{2}[/-]\d{4})', full_text)    
    issue_match = re.search(r'ISSUE\s+(?:DATE\s+)?(\d{2}[/-]\d{2}[/-]\d{4})', full_text)
    expiry_match = re.search(r'(?:EXP|EXPIR|EXPIRY|EXPIRATION|EXPLRY|EXPLR)\s+(?:DATE\s+|DATA\s+)?(\d{2}[/-]\d{2}[/-]\d{4})', full_text)
    
    # name
    name_match = re.search(
    r'NAME\s+([A-Z\s]+?)(?:NATIONAL|CITIZEN|DATE|LICENSE|LICENCE|DOB|BIRTH|ISSUE|EXPIR|PLACE|ADDRESS|SEX|GENDER|AGE|NO\.|NUMBER|SIGN|$)',
    full_text
    )
    if not name_match:
        name_match = re.search(
            r'([A-Z]{2,}(?:\s+[A-Z]{2,}){1,4})\s+(?:NO|DOB|EXP)',
            full_text
        )   
    name = name_match.group(1).strip() if name_match else None
    dob = dob_match.group(1) if dob_match else None
    issue_date = issue_match.group(1) if issue_match else None
    expiry_date = expiry_match.group(1) if expiry_match else None

    return {
    'name': name,
    'dob': dob,
    'issue_date': issue_date,
    'expiry_date': expiry_date,
}
if __name__ == "__main__":
    fields = extract_fields("../research/sds.jpg")
    print(fields)
