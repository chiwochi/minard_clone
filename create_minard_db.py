import pandas as pd
import sqlite3

class CreateMinardDB:
    def __init__(self):
        # 一條一條讀取txt的資料
        with open("data/minard.txt") as f:
            lines = f.readlines()
        # 將標題存入 column_names   
        column_names = lines[2].split()
        # print(column_names)

        # 因為標題有多餘符號，所以進行取代，讓資料更清晰
        patterns_to_be_replaced = {"(", ")", "$", ","}
        adjusted_column_names = []
        for column_name in column_names:
            for pattern in patterns_to_be_replaced:
                if pattern in column_name:
                    column_name = column_name.replace(pattern, "")
            adjusted_column_names.append(column_name)
        # print(adjusted_column_names)
        self.lines = lines
        # 將標題分割成 city temperature troop
        self.column_names_city = adjusted_column_names[:3]
        self.column_names_temperature = adjusted_column_names[3:7]
        self.column_names_troop = adjusted_column_names[7:]
        # print(column_names_city)
        # print(column_names_temperature)
        # print(column_names_troop)
        
    def create_city_dataframe(self):
        i = 6
        longitudes, latitudes, cities = [], [], []
        while i <= 25:
            long, lat, city = self.lines[i].split()[:3]
            longitudes.append(float(long))
            latitudes.append(float(lat))
            cities.append(city)
            i+=1
        # print(longitudes)
        # print(latitudes)
        # print(cities)
        city_data = (longitudes, latitudes, cities)
        # for data in city_data:
        #     print(data)
            
        city_df = pd.DataFrame()
        for column_name, data in zip(self.column_names_city, city_data):
            city_df[column_name] = data
        # print(city_df)
        return city_df
    
    def create_temperature_dataframe(self):
        i = 6
        longitudes, temperatures, days, dates = [], [], [], []
        while i <=14:
            lines_split = self.lines[i].split()
            longitudes.append(float(lines_split[3]))
            temperatures.append(int(lines_split[4]))
            days.append(int(lines_split[5]))
            if i == 10:
                dates.append("Nov 24")
            else:
                date_str = lines_split[6] + " " + lines_split[7]
                dates.append(date_str)
            i += 1
        temperatures_data = (longitudes, temperatures, days, dates)
        # for data in temperatures_data:
        #     print(data)
        temperatures_df = pd.DataFrame()
        for column_name, data in zip(self.column_names_temperature, temperatures_data):
            temperatures_df[column_name] = data
        # print(temperatures_df)
        return temperatures_df
    
    def create_troop_dataframe(self):
        i = 6
        longitudes, latitudes, survivals, directions, divisions = [], [], [], [], []
        while i <= 53:
            lines_split = self.lines[i].split()
            divisions.append(int(lines_split[-1]))
            directions.append(lines_split[-2])
            survivals.append(int(lines_split[-3]))
            latitudes.append(float(lines_split[-4]))
            longitudes.append(float(lines_split[-5]))
            i+=1
            
        # print(divisions)
        # print(directions)
        # print(survivals)
        # print(latitudes)
        # print(longitudes)
        troop_data = (longitudes,latitudes, survivals, directions, divisions)
        # for data in troop_data:
            # print(data)
        troop_df = pd.DataFrame()
        for column_name, data in zip(self.column_names_troop, troop_data):
            troop_df[column_name] = data
        # print(troop_df)
        return troop_df
    
    def create_database(self):
        connection = sqlite3.connect("data/minard.db")
        city_df = self.create_city_dataframe()
        temperatures_df = self.create_temperature_dataframe()
        troop_df = self.create_troop_dataframe()
        df_dict = {
            "cities": city_df,
            "temperatures": temperatures_df,
            "troops": troop_df
        }
        for k, v in df_dict.items():
            v.to_sql(name=k, con = connection, index = False, if_exists="replace")
        connection.close()
        
create_minard_db = CreateMinardDB()
create_minard_db.create_database()

