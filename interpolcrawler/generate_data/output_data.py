import argparse
import json
import os
import sqlite3
import xml.etree.cElementTree as ET


def generate_data(format=None, outputfile=None, sex=None, yob=None, name=None):
    # file_extension is not json and format is json raise error
    # if file_extension is not xml and format is xml raise error
    conn = sqlite3.connect("interpoldata.db")
    curr = conn.cursor()
    execution_string = get_execution_string(name, sex, yob)
    data = curr.execute(execution_string)

    try:
        if not outputfile:
            # print data to stdout
            for row in data.fetchall():
                row = get_db_row_as_dict(row)
                print('name={first_name} birth_place={birth_place} date_of_birth={date_of_birth}'
                      ' nationality={nationality} height={height} weight={weight} '
                      'eye_color={eye_color} hair_color={hair_color} sex={sex}'
                      ' image_url={image_url} link={link}'.format(**row))

        else:
            split_file_name = outputfile.split('.')

            if (len(split_file_name) > 1 and split_file_name[-1] == 'json') or len(split_file_name) == 1:
                create_json_file(split_file_name, data)
            elif format == 'xml' or len(split_file_name) > 1 and split_file_name[-1] == 'xml':
                create_xml_file(split_file_name, data)
            else:
                raise Exception("Wrong file extension or format")
    except Exception() as e:
        print(e)
    finally:
        conn.close()


def get_execution_string(name, sex, yob):
    execute_string = "SELECT * FROM person_data_tb"
    if name:
        execute_string = execute_string + " WHERE first_name='{}'".format(name)

        if sex:
            sex = "M" if sex == "male" else "F"
            execute_string = execute_string + " AND sex='{}'".format(sex)

            if yob:
                execute_string = execute_string + " AND date_of_birth LIKE '{}%'".format(yob)
        elif yob:
            execute_string = execute_string + " AND date_of_birth LIKE '{}%'".format(yob)

    elif sex:
        sex = "M" if sex == "male" else "F"
        execute_string = execute_string + " WHERE sex='{}'".format(sex)

        if yob:
            execute_string = execute_string + " AND date_of_birth LIKE '{}%'".format(yob)

    elif yob:
        execute_string = execute_string + " WHERE date_of_birth LIKE '{}%'".format(yob)

    return execute_string


def get_db_row_as_dict(row):
    return {'first_name': row[1], 'birth_place': row[3], 'date_of_birth': row[4], 'nationality': row[5],
            'height': row[9], 'weight': row[10], 'eye_color': row[6], 'hair_color': row[7], 'sex': row[8],
            'image_url': row[11], 'link': row[12]}


def add_db_row_to_xml(row, parent):
    el = ET.SubElement(parent, 'first_name')
    el.text = row[1]

    el = ET.SubElement(parent, 'birth_place')
    if row[3]:
        el.text = row[3]

    el = ET.SubElement(parent, 'date_of_birth')
    el.text = row[4]

    el = ET.SubElement(parent, 'nationality')
    el.text = row[5]

    el = ET.SubElement(parent, 'height')
    el.text = str(row[9])

    el = ET.SubElement(parent, 'weight')
    el.text = str(row[10])

    el = ET.SubElement(parent, 'eye_color')
    if row[6]:
        el.text = row[6]

    el = ET.SubElement(parent, 'hair_color')
    if row[7]:
        el.text = row[7]

    el = ET.SubElement(parent, 'sex')
    el.text = row[8]

    el = ET.SubElement(parent, 'image_url')
    el.text = row[11]

    el = ET.SubElement(parent, 'link')
    el.text = row[12]


def create_json_file(file_name_list, data_db_obj):
    file_name = None
    if len(file_name_list) > 1:
        file_name = '.'.join(file_name_list)
    else:
        file_name = file_name_list[0] + '.json'

    new_file_path = os.path.join(os.getcwd(), file_name)
    new_file = open(new_file_path, 'w')

    json_list = []
    # get person data
    for row in data_db_obj.fetchall():
        row = get_db_row_as_dict(row)
        json_list.append(row)
        # write to file

    new_file.write(json.dumps({"records": [record for record in json_list]}))
    new_file.close()


def create_xml_file(file_name_list, data_db_obj):
    file_name = None
    if len(file_name_list) > 1:
        file_name = '.'.join(file_name_list)
    else:
        file_name = file_name_list[0] + '.xml'

    new_file_path = os.path.join(os.getcwd(), file_name)

    records = ET.Element('records')
    et = ET.ElementTree(records)

    for row in data_db_obj.fetchall():
        person = ET.SubElement(records, 'person')
        add_db_row_to_xml(row, person)

    # write to file
    et.write(open(new_file_path, 'w'), xml_declaration=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--format')
    parser.add_argument('--outputfile')
    parser.add_argument('--sex')
    parser.add_argument('--yob')
    parser.add_argument('--name')
    args = parser.parse_args()

    generate_data(args.format, args.outputfile, args.sex, args.yob, args.name)
