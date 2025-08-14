import os
import csv
import json

def csv_read(filepath, delimiter='\\'):
    rows = []
    with open(filepath, newline='') as f:
        reader = csv.reader(f, delimiter=delimiter)
        for row in reader:
            if row != []:
                rows.append(row)
    return rows

def csv_to_dict(filepath, delimiter='\\'):
    rows = csv_read(filepath, delimiter=delimiter)
    row_header = rows[0]
    rows_body = rows[1:]
    obj_list = []
    for row in rows_body:
        obj = {}
        for element_i, e in enumerate(row):
            obj[row_header[element_i]] = e.strip()
        obj_list.append(obj)
    return obj_list

def json_create(filepath):
    if not os.path.exists(filepath):
        json_write(filepath, {})

def json_read(filepath, create=False):
    if create == True: json_create(filepath)
    with open(filepath) as f:
        data = json.load(f)
    return data

def json_write(filepath, data):
    j = json.dumps(data, indent=4)
    with open(filepath, 'w') as f:
        print(j, file=f)

