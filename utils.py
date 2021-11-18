import math

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

        if len(glacier_id) == 5:
            pass
        else:
            print('Validation Error: The unique ID should be 5 digits.')
            error_count += 1

        if -90.0 <= lat <= 90.0:
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
