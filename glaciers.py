from pathlib import Path
import csv
import utils

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


    def find_nearest(self, lat, lon, n=5):
        """Get the n glaciers closest to the given coordinates."""
        lat1 = lat
        lon1 = lon
        distance = {}
        nearest_names = []

        for k in self.collection_object:
            lat2 = self.collection_object[k].lat
            lon2 = self.collection_object[k].lon
            d = utils.haversine_distance(lat1, lon1, lat2, lon2)
            distance[self.collection_object[k].id] = d

        #print('distance_ordered is', distance, len(distance))

        distance_ordered = dict(sorted(distance.items(), key=lambda e: e[1], reverse=True))
        #print('distance_ordered is', distance_ordered, len(distance_ordered))

        cnt = 0 
        for key, value in distance_ordered.items():
            cnt += 1
            if cnt > n:
                break
            nearest_names.append(self.collection_object[key].name)

        print(nearest_names)
    

    def filter_by_code(self, code_pattern):
        """Return the names of glaciers whose codes match the given pattern."""
        names_same_code = []
        if type(code_pattern) == int:
            for k in self.collection_object:
                if code_pattern == self.collection_object[k].code:
                    names_same_code.append(self.collection_object[k].name)
        else:
            for k in self.collection_object:    
                if code_pattern[:1] == '?':
                    if code_pattern[1:2] == str(self.collection_object[k].code)[1:2] and code_pattern[2:3] == str(self.collection_object[k].code)[2:3]:
                        names_same_code.append(self.collection_object[k].name)
                    elif code_pattern[1:2] == str(self.collection_object[k].code)[1:2] and code_pattern[2:3] == '?':
                        names_same_code.append(self.collection_object[k].name)
                    elif code_pattern[1:2] == '?' and code_pattern[2:3] == str(self.collection_object[k].code)[2:3]:
                        names_same_code.append(self.collection_object[k].name)
                    elif code_pattern[1:2] == '?' and code_pattern[2:3] == '?':
                        names_same_code.append(self.collection_object[k].name)

                elif code_pattern[:1] != '?' and code_pattern[1:2] == '?':
                    if code_pattern[:1] == str(self.collection_object[k].code)[:1] and code_pattern[2:3] == str(self.collection_object[k].code)[2:3]:
                        names_same_code.append(self.collection_object[k].name)
                    elif code_pattern[:1] == str(self.collection_object[k].code)[:1] and code_pattern[2:3] == '?':
                        names_same_code.append(self.collection_object[k].name)

                elif code_pattern[:1] != '?' and code_pattern[1:2] != '?' and code_pattern[2:3] == '?':
                    if code_pattern[:1] == str(self.collection_object[k].code)[:1] and code_pattern[1:2] == str(self.collection_object[k].code)[1:2]:
                        names_same_code.append(self.collection_object[k].name)
                else:
                    if code_pattern == str(self.collection_object[k].code):
                        names_same_code.append(self.collection_object[k].name)

        print(names_same_code)    

    def sort_by_latest_mass_balance(self, n=5, reverse=False):
        """Return the N glaciers with the highest area accumulated in the last measurement."""
        
        self.mass_balance_latest = {}
        output_names = []

        for k in self.collection_object:

            year_list = sorted(self.collection_object[k].mass_balance.keys(), reverse = True)

            if len(year_list) != 0:
                year_latest = year_list[0]
                self.mass_balance_latest[self.collection_object[k].id] = self.collection_object[k].mass_balance[year_latest]['mass_balance']

        #print(mass_balance_latest, len(mass_balance_latest))

        if reverse:
            mass_balance_latest_ordered = dict(sorted(self.mass_balance_latest.items(), key=lambda e: e[1]))
        else:
            mass_balance_latest_ordered = dict(sorted(self.mass_balance_latest.items(), key=lambda e: e[1], reverse=True))

        #print(mass_balance_latest_ordered, len(mass_balance_latest_ordered))

        cnt = 0 
        for key, value in mass_balance_latest_ordered.items():
            cnt += 1
            if cnt > n:
                break
            output_names.append(self.collection_object[key].name)

        print(output_names)

    
    def summary(self):
        num_glacier = len(self.mass_balance_latest)
        #print(num_glacier)

        glacier_earliest = {}

        #print(self.mass_balance_latest)

        for k in self.collection_object:

            year_list = sorted(self.collection_object[k].mass_balance.keys())

            if len(year_list) != 0:
                year_earliest = year_list[0]
                glacier_earliest[self.collection_object[k].id] = year_earliest
        #print(glacier_earliest)

        earliest_year = sorted(glacier_earliest.values())[0]

        shrunk_count = 0
        for k in self.mass_balance_latest:
            if self.mass_balance_latest[k] < 0:
                shrunk_count += 1
        
        #print(shrunk_count)
        
        shrunk_pcg = int(round((shrunk_count/num_glacier), 2) * 100)

        #print(shrunk_pcg)

        print(f'The collection has {num_glacier} glaciers.')
        print(f'The earliest measurement was in {earliest_year}.')
        print(f'{shrunk_pcg}% of glaciers shrunk in their last measurement.')

    def plot_extremes(self, output_path):
        raise NotImplementedError


file_path_basic = Path('sheet-A.csv')
a = GlacierCollection(file_path_basic)

a.read_mass_balance_data('sheet-EE.csv')

#a.filter_by_code(424)
#a.find_nearest(2, 3, 2)
#a.sort_by_latest_mass_balance()
#a.summary()

