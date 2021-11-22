import math
from datetime import datetime

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass 
    return False


def haversine_distance(lat1, lon1, lat2, lon2):
    """Return the distance in km between two points around the Earth.

    Latitude and longitude for each point are given in degrees.
    """
    lat1 = math.radians(float(lat1))
    lat2 = math.radians(float(lat2))
    lon1 = math.radians(float(lon1))
    lon2 = math.radians(float(lon2))

    R = 6371
    d = 2 * R * math.asin(pow(math.sin((lat2-lat1)/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2-lon1)/2)**2, 1/2))
    return d


def validation_glacier(glacier_id, name, unit, lat, lon, code):

    if type(glacier_id) == str and type(name) == str and is_number(lat) and is_number(lon) and type(code) == int:

        if len(glacier_id) == 5 and is_number(glacier_id):
            pass
        else:
            raise ValueError('Invalid glacier id! The glacier id should be 5 digits.')

        if -90 <= int(lat) <= 90:
            pass 
        else:
            raise ValueError('Invalid latitute! The latitute should be between -90 and 90.')

        if -180 <= int(lon) <= 180:
            pass
        else:
            raise ValueError('Invalid lontitute! The lontitute should be between -180 and 180.')

        if len(unit) == 2 and (unit.isupper() or unit == '99'):
            pass
        else:
            raise ValueError('Invalid political unit! The political unit should be 2 capital letters or "99".')

    else:
        raise TypeError('Invalid datatype! The identifier, name and political unit should be passed as strings, and the latitude and longitude as numerical values. The 3-digit code should be passed as an integer.')



def validation_add_mass_balance_measurement(year, mass_balance, check_partial):

    crt_year = datetime.now().year

    if is_number(year) and int(year) <= crt_year:
        pass
    else:
        raise ValueError(f'Invalid year! The year should be less than or equal to the current year {crt_year}.')

    if is_number(mass_balance):
        pass
    else:
        raise ValueError('Invalid mass_balance! The mass_balance should be a digit.')
    
    if type(check_partial) == bool:
        pass
    else:
        raise TypeError('Invalid check_partial! The check_partial should be a bool value.')
    


def validation_collect(row_index, id, unit, lat, lon):

    if is_number(id) and len(id) == 5:
        pass
    else:
        raise ValueError(f'Invalid glacier id at row {row_index}! The glacier id should be 5 digits.')

    if -90.0 <= int(lat) <= 90.0:
        pass 
    else:
        raise ValueError(f'Invalid latitute at row {row_index}! The latitute should be between -90 and 90.')

    if -180 <= int(lon) <= 180:
        pass
    else:
        raise ValueError(f'Invalid lontitute at row {row_index}! The lontitute should be between -180 and 180.')
        
    if len(unit) == 2 and (unit.isupper() or unit == '99'):
        pass
    else:
        raise ValueError(f'Invalid political unit at row {row_index}! The political unit should be 2 capital letters or "99".')
        


def validation_read_mass_balance(row_index, id, year, annual_balance):

    crt_year = datetime.now().year

    if len(id) == 5 and is_number(id):
        pass
    else:
        raise ValueError(f'Invalid glacier id at row {row_index}! The glacier id should be 5 digits.')
        

    if int(year) <= crt_year:
        pass
    else:
        raise ValueError(f'Invalid year at row {row_index}! The year should be an integer number which is less than or equal to the current year {crt_year}.')
        

    if is_number(annual_balance):
        pass
    else:
        raise ValueError('Invalid annual balance! The annual balance should be a digit.')
        


def validation_find_nearest(lat, lon, n):

    if is_number(lat) and -90 <= int(lat) <= 90:
        pass 
    else:
        raise ValueError('Invalid latitute! The latitute should be a digit between -90 and 90.')
        
    if  is_number(lon) and -180 <= int(lon) <= 180:
        pass
    else:
        raise ValueError('Invalid lontitute! The lontitute should be a digit between -180 and 180.')
    if  type(n) == int:
        pass
    else:
        raise ValueError('Invalid n! The n should be an integer number.')


def validation_filter_by_code(code_pattern):

    if type(code_pattern) == int and len(str(code_pattern)) == 3:
        pass

    elif type(code_pattern) == str and len(code_pattern) == 3:
        cnt = 0
        for i in range(len(code_pattern)):
            if is_number(code_pattern[i]) or code_pattern[i] == '?':
                pass
            else:
                cnt += 1

        if cnt == 0:
            pass
        else:
            raise ValueError('Invalid code pattern! Every element of the code pattern should be a digit or a "?".')
            
    else:
        raise ValueError('Invalid code pattern! The code pattern should be an integer or string with a length of 3. Every element of the code pattern should be a digit or a "?".')


def validation_sort_by_latest_mass_balance(n, reverse):

    if type(n) == int:
        if type(reverse) == bool:
            pass
        else:
            raise TypeError('Invalid reverse! The reverse should be a bool value.')
            
    else:
        raise TypeError('Invalid n! The n should be an integer number.')

