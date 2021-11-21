import pytest
from pathlib import Path
import glaciers


year_mass_balance = [
    {
        'year':2015,
        'value':-793.0
    },
    {
        'year':2020,
        'value':-13331.0
    }
]

data_code_name = [
    {'code':323,
    'name':['EIRIKSJOKULL', 'HOFSJOKUL_EYSTRI', 'HRUTFELL', 'ORAEFAJOKULL', 'SNAEFELLSJOKULL', 'THRANDARJOKULL', 'TINDFJALLAJOKULL', 'TORFAJOKULL', 'TUNGNAFELLSJOKULL']},
    {'code':'5?4',
    'name': ['ALERCE', 'DE LOS TRES', 'NARVAEZ GRANDE', 'PIEDRAS BLANCAS', 'SAN LORENZO SUR', 'ARTESONRAJU', 'SHALLAP']}
]


@pytest.fixture()
def define_collection():
    file_path = Path('sheet-A.csv')
    collection = glaciers.GlacierCollection(file_path)
    
    return collection


@pytest.fixture(params = year_mass_balance)
def year_mass_balance(request):
    return request.param
# test validation


@pytest.fixture(params = data_code_name)
def data_code_names(request):
    return request.param


def test_mass_balance_error(define_collection):
    collection = define_collection
    with pytest.raises(ValueError):
        collection.read_mass_balance_data('sheet-EE_test_mass_balance_error.csv')
    assert True


def test_mass_balance_success(define_collection, year_mass_balance):
   collection = define_collection
   collection.read_mass_balance_data('sheet-EE_valid.csv')
   year = year_mass_balance['year']
   expected = year_mass_balance['value']
   actual = collection.collection_object['04532'].mass_balance[year]['mass_balance']
   #partial = collection.collection_object['04532'].mass_balance[2020]['mass_balance']
   
   assert actual == expected
   

def test_sort_by_latest_mass_balance(define_collection):
    collection = define_collection
    names_latest = collection.sort_by_latest_mass_balance(5,True)
    print(names_latest)

    assert names_latest == ['ARTESONRAJU', 'TUNSBERGDALSBREEN', 'PARLUNG NO. 94', 'GRAAFJELLSBREA', 'AGUA NEGRA']


    


