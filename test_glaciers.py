import pytest
from pathlib import Path
import glaciers



@pytest.fixture()
def define_collection():
    file_path = Path('sheet-A.csv')
    collection = glaciers.GlacierCollection(file_path)
    
    return collection


def test_mass_balance_error(define_collection):
    collection = define_collection
    with pytest.raises(ValueError):
        collection.read_mass_balance_data('sheet-EE_test_mass_balance_error.csv')
    assert True


@pytest.mark.parametrize('year,expected',
    [
        (2015, -793.0), # data for the partial measurement
        (2020, -13331.0) # data for the whole measurement
    ]
)
def test_mass_balance_success(define_collection, year, expected):
   collection = define_collection
   collection.read_mass_balance_data('sheet-EE_valid.csv')
   actual = collection.collection_object['04532'].mass_balance[year]['mass_balance']
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
    #collection.read_mass_balance_data('sheet-EE_valid.csv')
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



