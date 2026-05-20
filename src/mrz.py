import easyocr

reader = easyocr.Reader(['en'])

def parse_mrz(image_path):
    result = reader.readtext(image_path)
    mrz_lines = [line[1] for line in result if '<' in line[1]]
    
    if len(mrz_lines) < 2:
        return None
    
    line1 = mrz_lines[0]
    line2 = mrz_lines[1]
    
    # parse line 1
    doc_type = line1[0:1]
    country = line1[2:5]
    name = line1[5:44]
    
    # parse line 2
    passport_no = line2[0:9]
    nationality = line2[10:13]
    dob = line2[13:19]
    sex = line2[20:21]
    expiry = line2[21:27]
    
    # format dob
    if int(dob[0:2]) > 30:
        dob = '19' + dob
    else:
        dob = '20' + dob
    dob = f"{dob[0:4]}/{dob[4:6]}/{dob[6:8]}"
    
    # format expiry
    if int(expiry[0:2]) > 30:
        expiry = '19' + expiry
    else:
        expiry = '20' + expiry
    expiry = f"{expiry[0:4]}/{expiry[4:6]}/{expiry[6:8]}"
    
    return {
        'doc_type': doc_type,
        'country': country,
        'name': name,
        'passport_no': passport_no,
        'nationality': nationality,
        'dob': dob,
        'sex': sex,
        'expiry': expiry
    }

if __name__ == "__main__":
    result = parse_mrz("../research/psprt.jpg")
    print(result)