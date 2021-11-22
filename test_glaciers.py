import pytest
from pathlib import Path
import glaciers


@pytest.fixture()
def define_collection():
    file_path = Path('sheet-A.csv')
    collection = glaciers.GlacierCollection(file_path)
    
    return collection


@pytest.mark.parametrize('err, glacier_id, name, unit, lat, lon, code',
    [
        (TypeError,2345,'glacier0','99',56,-89,333),
        (TypeError,'12345','glacier1','99',56,[1,2],333),
        (TypeError,'12345','glacier2','99',56,88,'333'),
        (ValueError,'2345','glacier3','SS',56,-89,333),
        (ValueError,'12345','glacier4','ns',56,-89,333),
        (ValueError,'12345','glacier5','99',-888,-89,333),
        (ValueError,'12345','glacier6','99',56,999,333)
    ]
)
def test_glacier_creating_error(err, glacier_id, name, unit, lat, lon, code):
    with pytest.raises(err):
        glaciers.Glacier(glacier_id, name, unit, lat, lon, code)
    assert True


@pytest.mark.parametrize('err, year, mass_balance, check_partial',
    [
        (ValueError,'2033','333',True),
        (ValueError,'glac',345,True),
        (ValueError,'2021','eee',False),
        (TypeError,'2021',111,'glacier')
    ]
)
def test_glacier_add_mass_error(err, year, mass_balance, check_partial):
    with pytest.raises(err):
        glaciers.Glacier('12345','glacier0','99',56,-89,333).add_mass_balance_measurement(year, mass_balance, check_partial)
    assert True


def test_collection_mass_balance_error(define_collection):
    collection = define_collection
    with pytest.raises(ValueError):
        collection.read_mass_balance_data('sheet-EE_test_mass_balance_error.csv')
    assert True


@pytest.mark.parametrize('err, lat, lon, n',
    [
        (ValueError,'ee','33',2),
        (ValueError,66,345,3),
        (ValueError,'43','-66',6.9)
    ]
)
def test_find_nearest_error(define_collection, err, lat, lon, n):
    collection = define_collection
    with pytest.raises(err):
        collection.find_nearest(lat, lon, n)
    assert True


@pytest.mark.parametrize('id, year,expected',
    [
        ('04532', 2015, -793.0), # data for the partial measurement
        ('04532', 2020, -13331.0), # data for the whole measurement
        ('01048', 1982, -300.0),# data for the whole measurement
        ('01316', 1966, -25510.0),# data for the partial measurement
        ('10407', 2014, -720.0),# data for the whole measurement
        ('03903', 2015, -18969.0)# data for the whole measurement
    ]
)
def test_mass_balance_success(define_collection, id, year, expected):
   collection = define_collection
   collection.read_mass_balance_data('sheet-EE_valid.csv')
   actual = collection.collection_object[id].mass_balance[year]['mass_balance']
   assert actual == expected
   

@pytest.mark.parametrize('code_pattern, expected',
    [
        (238,['CAINHAVARRE']),
        ('?46',['BONETE S', 'MARTIAL ESTE', 'MUZTAG ATA (GLACIER NO. 15)']),
        ('6?3',['ECHAURREN NORTE', 'SNAEFELL']),
        ('54?',['DE LOS TRES', 'GLJUFURARJOKULL']),
        ('??5',['PENON', 'CIPRESES', 'FLATISVATNET', 'MEMORGEBREEN', 'NORDFJORDBREEN', 'NORTHERN PART']),
        ('?5?',['BIRCH', 'BODMER', 'SCALETTA']),
        ('1??',['TORRE'])
    ]
)
def test_filter_by_code(define_collection,code_pattern,expected):
    collection = define_collection
    actual = collection.filter_by_code(code_pattern)
    assert actual == expected


@pytest.mark.parametrize('n, reverse, expected',
    [
        (5, True, ['ARTESONRAJU', 'TUNSBERGDALSBREEN', 'PARLUNG NO. 94', 'GRAAFJELLSBREA', 'AGUA NEGRA']),
        (5, False, ['STORSTEINSFJELLBREEN', 'CAINHAVARRE', 'BLAAISEN', 'REMBESDALSKAAKA', 'CHHOTA SHIGRI']),
        (2, True, ['ARTESONRAJU', 'TUNSBERGDALSBREEN']),
        (3, False, ['STORSTEINSFJELLBREEN', 'CAINHAVARRE', 'BLAAISEN'])
    ]
)
def test_sort_by_latest_mass_balance(define_collection,n,reverse,expected):
    collection = define_collection
    file_path = Path('sheet-EE_valid.csv')
    collection.read_mass_balance_data(file_path)
    actual = collection.sort_by_latest_mass_balance(n,reverse)
    assert actual == expected



