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
    R = 6371
    d = 2 * R * math.asin(pow(math.sin((lat2-lat1)/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2-lon1)/2)**2, 1/2))
    return d


def validation_glacier(glacier_id, name, unit, lat, lon, code):

    error_count = 0

    if type(glacier_id) == str and type(name) == str and type(unit) == str and type(lat) == float and type(lon) == float and type(code) == int:

        if len(glacier_id) == 5 and is_number(glacier_id):
            pass
        else:
            print('Validation Error: The unique ID should be 5 digits.')
            error_count += 1

        if -90 <= lat <= 90:
            pass 
        else:
            print('Validation Error: The latitute should be between -90 and 90.')
            error_count += 1

        if -180 <= lon <= 180:
            pass
        else:
            print('Validation Error: The lontitute should be between -180 and 180.')
            error_count += 1

        if len(unit) == 2 and (unit.isupper() or unit == '99'):
            pass
        else:
            print('Validation Error: Thee political unit should be 2 capital letters or "99".')
            error_count += 1

    else:
        print('Validation Error:  The identifier, name and political unit should be passed as strings, and the latitude and longitude as numerical values. The 3-digit code should be passed as an integer.')
        error_count += 1

    return error_count



def validation_add_mass_balance_measurement(year, mass_balance, check_partial):

    crt_year = datetime.now().year
    error_count = 0

    if is_number(year) and year <= crt_year:
        pass
    else:
        print(f'Validation Error: The year should be an integer number which is less than or equal to the current year {crt_year}.')
        error_count += 1
    
    if is_number(mass_balance):
        pass
    else:
        print('Validation Error: The mass_balance should be a digit.')
        error_count += 1

    if type(check_partial) == bool:
        pass
    else:
        print('Validation Error: The check_partial should be a bool value.')
    
    return error_count



def validation_collect(row_index, id, unit, lat, lon):

    error_count = 0

    if len(id) == 5 and is_number(id):
        pass
    else:
        print(f'Validation Error in row{row_index}: The unique ID should be 5 digits.')
        error_count += 1

    if -90.0 <= lat <= 90.0:
        pass 
    else:
        print(f'Validation Error in row{row_index}: The latitute should be between -90 and 90.')
        error_count += 1

    if -180 <= lon <= 180:
        pass
    else:
        print(f'Validation Error in row{row_index}: The lontitute should be between -180 and 180.')
        error_count += 1

    if len(unit) == 2 and (unit.isupper() or unit == '99'):
        pass
    else:
        print(f'Validation Error in row{row_index}: Thee political unit should be 2 capital letters or "99".')
        error_count += 1

    return error_count


def validation_read_mass_balance(row_index, id, year, annual_balance):

    error_count = 0
    crt_year = datetime.now().year

    if len(id) == 5 and is_number(id):
        pass
    else:
        print(f'Validation Error in row{row_index}: The unique ID should be 5 digits.')
        error_count += 1

    if int(year) <= crt_year:
        pass
    else:
        print(f'Validation Error in row{row_index}: The year should be an integer number which is less than or equal to the current year {crt_year}.')
        error_count += 1

    if is_number(annual_balance):
        pass
    else:
        print(f'Validation Error in row{row_index}: The annual balance should be a digit.')
        error_count += 1

    return error_count


def validation_find_nearest(lat, lon):

    error_count = 0

    if is_number(lat):

        if -90 <= lat <= 90:
            pass 
        else:
            print('Validation Error: The latitute should be between -90 and 90.')
            error_count += 1
    else:
        print('Validation Error: The latitute should be a digit between -90 and 90.')
        error_count += 1


    if  is_number(lon):

        if -180 <= lon <= 180:
            pass
        else:
            print('Validation Error: The lontitute should be between -180 and 180.')
            error_count += 1
    else:
        print('Validation Error: The lontitute should be a digit between -180 and 180.')
        error_count += 1
        

    return error_count


def validation_filter_by_code(code_pattern):

    error_count = 0

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
            print('Validation Error: Every element of the code pattern should be a digit or a "?".')
            error_count += 1

    else:
        print('Validation Error: The code pattern should be an integer or string with a length of 3. Every element of the code pattern should be a digit or a "?".')
        error_count += 1

    return error_count

