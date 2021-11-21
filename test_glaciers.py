import pytest
import glaciers
from pathlib import Path


@pytest.fixture()
def define_instance():
    file_path = Path('sheet-A.csv')
    collection = glaciers.GlacierCollection(file_path)
    
    return collection

# test validation

def test_mass_balance_error():
    collection = define_instance
    with pytest.raises(ValueError):
        collection.read_mass_balance_data('sheet-EE_test_mass_balance_error.csv')
    assert True


def test_mass_balance_success():
   collection = define_instance
   collection.read_mass_balance_data('sheet-EE_valid.csv')
   whole = collection.collection_object['04532'].mass_balance[2015]['mass_balance']
   partial = collection.collection_object['04532'].mass_balance[2020]['mass_balance']
   
   assert whole == -793.0 and partial == -13331.0
   

#@pytest.mark.parametrize('test_input, excepted',[(collection.filter_by_code(),[]),(,)])
#def test_filter_by_code(define_instance):
#    collection = define_instance

@pytest.mark.parametrize('test_input, excepted',(define_instance.sort_by_latest_mass_balance(5, True),['ARTESONRAJU', 'TUNSBERGDALSBREEN', 'PARLUNG NO. 94', 'GRAAFJELLSBREA', 'AGUA NEGRA']))
def test_sort_by_latest_mass_balance(request):
    test_input = request.param['test_input']
    excepted = request.param['excepted']
    assert test_input == excepted





    


