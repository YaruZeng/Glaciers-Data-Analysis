from pathlib import Path
import csv
import utils
import matplotlib.pyplot as plt
import os


class Glacier:
    def __init__(self, glacier_id, name, unit, lat, lon, code):

        # check validation
        self.error_count = utils.validation_glacier(glacier_id, name, unit, lat, lon, code)

        if self.error_count == 0:
            self.id = glacier_id
            self.lat = lat
            self.lon = lon
            self.unit = unit
            self.name = name
            self.code = code
            self.mass_balance = {}
        

    def add_mass_balance_measurement(self, year, mass_balance, check_partial):

        # check validation
        error_count = utils.validation_add_mass_balance_measurement(year, mass_balance, check_partial)

        if self.error_count == 0 and error_count == 0:
            
            if year in self.mass_balance.keys(): 

                if check_partial == True and self.mass_balance[year]['check_partial'] == True:
                    self.mass_balance[year]['mass_balance'] += mass_balance         
                if check_partial == False and self.mass_balance[year]['check_partial'] == True:
                    pass
            else:
                self.mass_balance[year] = {'mass_balance' : mass_balance, 'check_partial' : check_partial}


    def plot_mass_balance(self, output_path):
        
        #print(self.mass_balance)
        x = sorted(self.mass_balance.keys())
        #print(x)
        y = []

        for i in range(len(x)):
            temp = self.mass_balance[x[i]]['mass_balance']
            y.append(temp)
        #print(y)

        plt.figure(figsize=(10,5))
        plt.title(f'{self.id} {self.name}: Mass balance changes by years')
        plt.xlabel('year')
        plt.ylabel('mass balance in mm.w.e')
        plt.plot(x,y)
        path = os.path.join(output_path, f'{self.id}.png')
        plt.savefig(path, format='png')
        plt.show()

        
class GlacierCollection:

    def __init__(self, file_path):

        self.path = Path(file_path)
        
        self.collection_object = {}
        
        with open(self.path, newline = '') as f:
            collection_info = csv.DictReader(f)

            row_index = 0

            for row in collection_info:

                row_index += 1

                id = row['WGMS_ID']
                name = row['NAME']
                unit = row['POLITICAL_UNIT']
                lat = float(row['LATITUDE'])
                lon = float(row['LONGITUDE'])
                code = int(row['PRIM_CLASSIFIC'] + row['FORM'] + row['FRONTAL_CHARS'])

                # check validation
                error_count = utils.validation_collect(row_index, id, unit, lat, lon)
                
                if error_count == 0:
                    self.collection_object[id] = Glacier(id, name, unit, lat, lon, code)


    def read_mass_balance_data(self, file_path):

        self.collection_mass_balance = {}
        
        with open(file_path, 'r') as f:
            balance_data = csv.DictReader(f)

            row_index = 0

            for row in balance_data:

                row_index += 1

                crt_id = row['WGMS_ID']   
                year = row['YEAR']
                annual_balance = row['ANNUAL_BALANCE']
                #print(annual_balance, type(annual_balance))
                    
                if row['LOWER_BOUND'] != '9999' and row['UPPER_BOUND'] != '9999':
                    check_partial = True
                else:
                    check_partial = False
                
                # check validation
                error_count = utils.validation_read_mass_balance(row_index, crt_id, year, annual_balance)

                if error_count == 0:
                    year = int(row['YEAR']) 
                    annual_balance = float(row['ANNUAL_BALANCE'])
                    self.collection_object[crt_id].add_mass_balance_measurement(year,annual_balance,check_partial)


    def find_nearest(self, lat, lon, n=5):
        """Get the n glaciers closest to the given coordinates."""
        # check validation
        error_count = utils.validation_find_nearest(lat, lon)

        if error_count == 0:

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
        # check validation
        error_count = utils.validation_filter_by_code(code_pattern)

        if error_count == 0:
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

            print(names_same_code, len(names_same_code)) 


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

        mass_balance_latest_ordered = dict(sorted(self.mass_balance_latest.items(), key=lambda e: e[1]))
        #print(mass_balance_latest_ordered)
        
        id_shrunk_most = list(mass_balance_latest_ordered.keys())[0]
        id_grew_most = list(mass_balance_latest_ordered.keys())[-1]

        #print(id_shrunk_most)
        #print(id_grew_most)

        self.collection_object[id_shrunk_most].plot_mass_balance(output_path)
        self.collection_object[id_grew_most].plot_mass_balance(output_path)



file_path_basic = Path('sheet-A.csv')
a = GlacierCollection(file_path_basic)

a.read_mass_balance_data('sheet-EE.csv')

a.filter_by_code(424)
#a.find_nearest(444, 444, 2)
#a.sort_by_latest_mass_balance()
#a.summary()

#output_path = Path('../')
#a.collection_object['01047'].plot_mass_balance(output_path)
#a.plot_extremes(output_path)

#b = Glacier('1234', 'boogie', 'FF', 33.3, 44.5, 999)
#b.add_mass_balance_measurement(2027, 444, 1)

"""
for k in a.collection_object:
    
    print('mass balance of id '+k+' is')
    print(a.collection_object[k].mass_balance)
"""

