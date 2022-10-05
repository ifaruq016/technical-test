import random
import string
import jwt
import os
from datetime import datetime, timezone
basedir = os.path.abspath(os.path.dirname(__file__))


def randomString( lenstr = 10 ) :
    letters = string.ascii_lowercase
    letters += string.ascii_uppercase
    letters += string.ascii_letters
    letters += string.digits
    result = ''.join(random.choice(letters) for i in range(lenstr))

    return result

def jwtEncode( payload = {} ) :
    scrtky = str("nZR9Eh15Os0oU2Y")
    encoded = jwt.encode(payload, scrtky, algorithm="HS256")

    return encoded

def jwtDecode( encoded ) :
    scrtky = str("nZR9Eh15Os0oU2Y")
    decoded = jwt.decode(encoded, scrtky, algorithms=["HS256"])

    return decoded

def validateToken( token ) :
    dataReturn = {
        'status' : '400',
        'user_id' : ''
    }

    if not token:
        dataReturn['status'] = '401'
        return dataReturn

    try:
        # decoding the payload to fetch the stored details
        decoded = jwtDecode( token )

        if decoded :
            dataReturn['status'] = '200'
            dataReturn['user_id'] = decoded['user_id']
            return dataReturn
        
        dataReturn['status'] = '400'
        return dataReturn
    except:
        dataReturn['status'] = '500'
        return dataReturn