import pytest
import glaciers
from pathlib import Path


@pytest.fixture()
def define_instance():
    file_path = Path('sheet-A.csv')
    collection = glaciers.GlacierCollection(file_path)
    
    return collection

# test validation

def test_mass_balance_error(define_instance):
    collection = define_instance
    with pytest.raises(ValueError):
        collection.read_mass_balance_data('sheet-EE_test_mass_balance_error.csv')
    assert True


def test_mass_balance_success(define_instance):
   collection = define_instance
   collection.read_mass_balance_data('sheet-EE_valid.csv')
   whole = collection.collection_object['04532'].mass_balance[2015]['mass_balance']
   partial = collection.collection_object['04532'].mass_balance[2020]['mass_balance']
   
   assert whole == -793.0 and partial == -13331.0
   

#@pytest.mark.parametrize('test_input, excepted',[(collection.filter_by_code(),[]),(,)])
#def test_filter_by_code(define_instance):
#    collection = define_instance

#def test_sort_by_latest_mass_balance()


    











#a.filter_by_code(424)
#a.find_nearest(444, 444, 2)
#a.sort_by_latest_mass_balance(8,True)
#a.summary()

#output_path = Path('../')
#a.collection_object['01047'].plot_mass_balance(output_path)
#a.plot_extremes(output_path)

#b = Glacier('1234', 'boogie', 'FF', 33.3, 44.5, 999)
#b.add_mass_balance_measurement(2021, 444, 1)
#print(b.mass_balance)

