from pathlib import Path
import csv

class Glacier:
    def __init__(self, glacier_id, name, unit, lat, lon, code):
        self.id = glacier_id
        self.name = name
        self.unit = unit 
        self.lat = lat 
        self.lon = lon 
        self.code = code
        
        self.mass_balance = {}
    def add_mass_balance_measurement(self, year, mass_balance, check_partial):
        
        if year in self.mass_balance.keys():
            
            if check_partial == 1 and self.mass_balance[year]['check_partial'] == 1:
                self.mass_balance[year]['mass_balance'] += mass_balance
                      
            if check_partial == 0 and self.mass_balance[year]['check_partial'] == 1:
                pass
        
        else:
            self.mass_balance[year] = {'mass_balance' : mass_balance, 'check_partial' : check_partial}
        

    def plot_mass_balance(self, output_path):
        raise NotImplementedError

        
class GlacierCollection:

    def __init__(self, file_path):

        self.path = Path(file_path)
        
        self.collection_object = {}
        
        with open(self.path, newline = '') as f:
            file = csv.DictReader(f)
            
            for row in file:
                glacier_id = row['WGMS_ID']
                name = row['NAME']
                unit = row['POLITICAL_UNIT']
                lat = float(row['LATITUDE'])
                lon = float(row['LONGITUDE'])
                code = int(row['PRIM_CLASSIFIC'] + row['FORM'] + row['FRONTAL_CHARS'])
                
                self.collection_object[glacier_id] = Glacier(glacier_id, name, unit, lat, lon, code)


    def read_mass_balance_data(self, file_path):

        self.collection_mass_balance = {}
        
        with open(file_path, 'r', encoding='utf-8') as f:
            file = csv.reader(f)
            balance_data = list(file)
            row_index_del = []

            #print(len(balance_data))

            for row_index in range(len(balance_data)):
                if balance_data[row_index][11] == '':
                    row_index_del.append(row_index)
                    #print(row_index, balance_data[row_index])

            #print(row_index_del)
            cnt_del = 0
            for i in range(len(row_index_del)):
                del balance_data[row_index_del[i]]
                if i < len(row_index_del) - 1:
                    cnt_del += 1
                    row_index_del[i+1] -= cnt_del
                    #print(row_index_del)


            #print(len(balance_data))

            for row_index in range(len(balance_data)):
                
                if row_index != 0:
                    current_id = balance_data[row_index][2]
                    year = balance_data[row_index][3]
                    
                    mass_balance = float(balance_data[row_index][11])
                    
                    if balance_data[row_index][4] != '9999' and balance_data[row_index][5] != '9999':
                        check_partial = 1
                    else:
                        check_partial = 0

                    self.collection_object[current_id].add_mass_balance_measurement(year,mass_balance,check_partial)


    def find_nearest(self, lat, lon, n):
        """Get the n glaciers closest to the given coordinates."""
        raise NotImplementedError
    
    def filter_by_code(self, code_pattern):
        """Return the names of glaciers whose codes match the given pattern."""
        raise NotImplementedError

    def sort_by_latest_mass_balance(self, n, reverse):
        """Return the N glaciers with the highest area accumulated in the last measurement."""
        raise NotImplementedError

    def summary(self):
        raise NotImplementedError

    def plot_extremes(self, output_path):
        raise NotImplementedError


file_path_basic = Path('sheet-A.csv')
a = GlacierCollection(file_path_basic)

a.read_mass_balance_data('sheet-EE.csv')

'''for k in a.collection_object:
    
    print('mass balance of id '+k+' is')
    print(a.collection_object[k].mass_balance)'''

