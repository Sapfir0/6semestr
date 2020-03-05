import re
import os

def get_input_names():
    os.chdir('input')
    input_list = list(filter(lambda x: re.match('.*.xml', x), os.listdir()))
    os.chdir('..')
    return input_list

def get_patents(path: str):
    input_file = open(path, 'r')
    input_string = input_file.read()
    input_file.close()
    return input_string

def parse(text: str):
    splitter = '<?xml version="1.0" encoding="UTF-8"?>'
    splitted = text.split(splitter)
    splitted = list(filter(lambda x: x != '', splitted))
    return splitted

def save_parsed(list_parsed: list, path_save_to: str):
    for i in range(len(list_parsed)):
        output_file = open(path_save_to + str(i) + '.xml', 'w')
        output_file.write(list_parsed[i])
        output_file.close()

names = get_input_names()
for filename in names:
    input_path = 'input/' + filename
    patents = get_patents(input_path)
    parsed = parse(patents)
    save_parsed(parsed, 'output/' + filename)