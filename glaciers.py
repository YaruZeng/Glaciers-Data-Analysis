from pathlib import Path
import csv
import utils
import matplotlib.pyplot as plt


class Glacier:

    def __init__(self, glacier_id, name, unit, lat, lon, code):

        # check validation
        utils.validation_glacier(glacier_id, name, unit, lat, lon, code)

        self.id = glacier_id
        self.lat = lat
        self.lon = lon
        self.unit = unit
        self.name = name
        self.code = code

        self.mass_balance = {}


    def add_mass_balance_measurement(self, year, mass_balance, check_partial):

        # check validation
        utils.validation_add_mass_balance_measurement(year, mass_balance, check_partial)
            
        if year in self.mass_balance.keys(): 

            if check_partial == True:
                self.mass_balance[year]['mass_balance'] += mass_balance         
            if check_partial == False:
                pass
        else:
            self.mass_balance[year] = {'mass_balance' : mass_balance, 'check_partial' : check_partial}


    def plot_mass_balance(self, output_path):
        
        x = sorted(self.mass_balance.keys())
        
        y = []

        for i in range(len(x)):
            temp = self.mass_balance[x[i]]['mass_balance']
            y.append(temp)

        plt.figure(figsize=(10,5))
        plt.title(f'{self.id} {self.name}: Mass balance changes by years')
        plt.xlabel('year')
        plt.ylabel('mass balance in mm.w.e')
        plt.plot(x,y)
        plt.savefig(output_path, format='png')
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
                utils.validation_collect(row_index, id, unit, lat, lon)
                
                self.collection_object[id] = Glacier(id, name, unit, lat, lon, code)


    def read_mass_balance_data(self, file_path):
        
        with open(file_path, 'r') as f:
            balance_data = csv.DictReader(f)

            row_index = 0

            for row in balance_data:

                row_index += 1

                crt_id = row['WGMS_ID']
                year = row['YEAR']
                annual_balance = row['ANNUAL_BALANCE']

                if row['LOWER_BOUND'] == '9999' and row['UPPER_BOUND'] == '9999':
                    check_partial = False
                else:
                    check_partial = True
                    
                # check validation
                utils.validation_read_mass_balance(row_index, crt_id, year, annual_balance)
                    
                
                if annual_balance != '': # leave the row with a none annual balance
                    if crt_id in self.collection_object.keys():
                        # check glacier id is defined when creating the collection
                        year = int(row['YEAR']) 
                        annual_balance = float(row['ANNUAL_BALANCE'])
                        self.collection_object[crt_id].add_mass_balance_measurement(year,annual_balance,check_partial)
                    else:
                        raise ValueError(f'Row {row_index}: Failed to read mass balance data. {crt_id} is not defined when creating the collection.')


    def find_nearest(self, lat, lon, n=5):
        """Get the n glaciers closest to the given coordinates."""

        # check validation
        utils.validation_find_nearest(lat, lon, n)

        lat1 = lat
        lon1 = lon
        distance = {}
        self.nearest_names = []

        for k in self.collection_object:
            # compute the distance

            lat2 = self.collection_object[k].lat
            lon2 = self.collection_object[k].lon
            d = utils.haversine_distance(lat1, lon1, lat2, lon2)
            distance[self.collection_object[k].id] = d

        distance_ordered = dict(sorted(distance.items(), key=lambda e: e[1]))

        cnt = 0 
        for key in distance_ordered:
            cnt += 1
            if cnt > n:
                break
            self.nearest_names.append(self.collection_object[key].name)

        return self.nearest_names
    

    def filter_by_code(self, code_pattern):
        """Return the names of glaciers whose codes match the given pattern."""

        utils.validation_filter_by_code(code_pattern)

        self.names_same_pattern = []

        # check every possible code pattern and get corresponding names with the code pattern

        if type(code_pattern) == int:
            for k in self.collection_object:
                if code_pattern == self.collection_object[k].code:
                    self.names_same_pattern.append(self.collection_object[k].name)
        else:
            for k in self.collection_object:    
                if code_pattern[:1] == '?':
                    if code_pattern[1:2] == str(self.collection_object[k].code)[1:2] and code_pattern[2:3] == str(self.collection_object[k].code)[2:3]:
                        self.names_same_pattern.append(self.collection_object[k].name)
                    elif code_pattern[1:2] == str(self.collection_object[k].code)[1:2] and code_pattern[2:3] == '?':
                        self.names_same_pattern.append(self.collection_object[k].name)
                    elif code_pattern[1:2] == '?' and code_pattern[2:3] == str(self.collection_object[k].code)[2:3]:
                        self.names_same_pattern.append(self.collection_object[k].name)
                    elif code_pattern[1:2] == '?' and code_pattern[2:3] == '?':
                        self.names_same_pattern.append(self.collection_object[k].name)

                elif code_pattern[:1] != '?' and code_pattern[1:2] == '?':
                    if code_pattern[:1] == str(self.collection_object[k].code)[:1] and code_pattern[2:3] == str(self.collection_object[k].code)[2:3]:
                        self.names_same_pattern.append(self.collection_object[k].name)
                    elif code_pattern[:1] == str(self.collection_object[k].code)[:1] and code_pattern[2:3] == '?':
                        self.names_same_pattern.append(self.collection_object[k].name)

                elif code_pattern[:1] != '?' and code_pattern[1:2] != '?' and code_pattern[2:3] == '?':
                    if code_pattern[:1] == str(self.collection_object[k].code)[:1] and code_pattern[1:2] == str(self.collection_object[k].code)[1:2]:
                        self.names_same_pattern.append(self.collection_object[k].name)
                else:
                    if code_pattern == str(self.collection_object[k].code):
                        self.names_same_pattern.append(self.collection_object[k].name)

        return self.names_same_pattern


    def sort_by_latest_mass_balance(self, n=5, reverse=False):
        """Return the N glaciers with the highest area accumulated in the last measurement."""
        
        # check validation
        utils.validation_sort_by_latest_mass_balance(n, reverse)

        self.mass_balance_latest = {}
        output = []

        for k in self.collection_object:

            year_list = sorted(self.collection_object[k].mass_balance.keys(), reverse = True)

            if len(year_list) != 0:
                year_latest = year_list[0]
                self.mass_balance_latest[self.collection_object[k].id] = self.collection_object[k].mass_balance[year_latest]['mass_balance']

        if reverse:
            mass_balance_latest_ordered = dict(sorted(self.mass_balance_latest.items(), key=lambda e: e[1]))
        else:
            mass_balance_latest_ordered = dict(sorted(self.mass_balance_latest.items(), key=lambda e: e[1], reverse=True))

        cnt = 0 
        for key, value in mass_balance_latest_ordered.items():
            cnt += 1
            if cnt > n:
                break
            output.append(self.collection_object[key])

        return output

    
    def summary(self):

        self.mass_balance_latest = {}

        for k in self.collection_object:

            year_list = sorted(self.collection_object[k].mass_balance.keys(), reverse = True)

            if len(year_list) != 0:
                year_latest = year_list[0]
                self.mass_balance_latest[self.collection_object[k].id] = self.collection_object[k].mass_balance[year_latest]['mass_balance']


        num_glacier = len(self.mass_balance_latest)

        glacier_earliest = {}

        for k in self.collection_object:

            year_list = sorted(self.collection_object[k].mass_balance.keys())

            if len(year_list) != 0:
                year_earliest = year_list[0]
                glacier_earliest[self.collection_object[k].id] = year_earliest

        earliest_year = sorted(glacier_earliest.values())[0]

        shrunk_count = 0
        for k in self.mass_balance_latest:
            if self.mass_balance_latest[k] < 0:
                shrunk_count += 1
        
        shrunk_pcg = int(round((shrunk_count/num_glacier), 2) * 100)

        print(f'The collection has {num_glacier} glaciers.')
        print(f'The earliest measurement was in {earliest_year}.')
        print(f'{shrunk_pcg}% of glaciers shrunk in their last measurement.')


    def plot_extremes(self, output_path):

        mass_balance_latest_ordered = dict(sorted(self.mass_balance_latest.items(), key=lambda e: e[1]))
        
        id_shrunk_most = list(mass_balance_latest_ordered.keys())[0]
        id_grew_most = list(mass_balance_latest_ordered.keys())[-1]

        self.collection_object[id_shrunk_most].plot_mass_balance(output_path)
        self.collection_object[id_grew_most].plot_mass_balance(output_path)

