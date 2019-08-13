import os


def generate_data(format=None, outputfile=None, sex=None, yob=None, name=None):
    # file_extension is not json and format is json raise error
    # if file_extension is not xml and format is xml raise error
    split_file_name = outputfile.split('.')

    if not outputfile:
        # get data from db
        # print data to stdout
        if format != 'xml':
            # print json
        else:
            #print xml

    elif (len(split_file_name) > 1 and split_file_name[-1] == 'json') or len(split_file_name) == 1:
        create_json_file(split_file_name, sex, yob, name)
    elif format == 'xml' or len(split_file_name) > 1 and split_file_name[-1] == 'xml':
        create_xml_file(split_file_name, sex, yob, name)
    else:
        raise Exception("Wrong file extension or format")


def create_json_file(file_name_list=None, sex=None, yob=None, name=None):
    file_name = None
    if len(file_name_list) > 1:
        file_name = '.'.join(file_name_list)
    else:
        file_name = file_name_list[0] + '.json'

    new_file_path = os.path.join(os.getcwd(), '..', '..', file_name)
    new_file = open(new_file_path, 'w')

    # get person data

    # write to file
    new_file.write()


def create_xml_file(file_name_list=None, sex=None, yob=None, name=None):
    file_name = None
    if len(file_name_list) > 1:
        file_name = '.'.join(file_name_list)
    else:
        file_name = file_name_list[0] + '.xml'

    new_file_path = os.path.join(os.getcwd(), '..', '..', file_name)
    new_file = open(new_file_path, 'w')

    # get person data

    # write to file
    new_file.write()


