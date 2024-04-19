import json

f1 = open("Cleansed_CommutingModes.csv", "r")
lines = f1.readlines()

dictionary ={}
column_names = lines[0].split(",")
column_names[-1] = column_names[-1][:-1]
print(column_names)

for data_entry in lines: 
    if data_entry == lines[0]:
        continue 
    # split each line into elements of a list
    else:
        temp_list = data_entry.split(",")
        temp_list[-1] = temp_list[-1][:-1]
        year_range = temp_list[0]
        data_type = temp_list[1]
        location = temp_list[2]

        for i, data in enumerate(temp_list):
            if year_range not in dictionary:
                dictionary[year_range] = {}
            elif data_type not in dictionary[year_range]:
                dictionary[year_range][data_type] = {}
            elif location not in dictionary[year_range][data_type]:
                dictionary[year_range][data_type][location] = {}
            elif i > 2:
                dictionary[year_range][data_type][location][column_names[i]] = data 



# Create the dictionary here
f1.close()

#Save the json object to a file
f2 = open("CommutingModes.json", "w")
json.dump(dictionary, f2, indent = 4)

f2.close()
