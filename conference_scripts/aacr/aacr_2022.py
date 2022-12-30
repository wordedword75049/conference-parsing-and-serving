import csv

import requests
import json
import os
import tqdm

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup




def fill_dict(keys, values):
    dictionary = {}
    for key, value in zip(keys, values):
        dictionary.update({key: value})
    return dictionary


def remove_front_space(line):
    if line != '':
        while line[0] == ' ':
            line = line[1:]
    return line

def remove_all_spaces_and_tabs(line):
    if line != '':
        while (line[0] == ' ') or (line[0] == '\t'):
            line = line[1:]
        while (line[-1] == ' ') or (line[-1] == '\t'):
            line = line[:-1]
    return line


def clean_tags_from_text(text):
    index = len(text) - 1
    tag_flag = False
    end_index = -1
    while index >= 0:
        if (text[index] == '>') and (text[index - 1] != ' '):
            end_index = index
            tag_flag = True
        if (text[index] == 'p') and (text[index + 1] == '>'):
            text = text[:index + 2] + '\n' + text[index + 2:]
        if (text[index] == '<') and (tag_flag == True):
            #print('erasing ' + text[index:end_index + 1])
            text = text[:index] + text[end_index + 1:]
            tag_flag = False
        index = index - 1
    return text


def parse_json(main_data):
    links = list(main_data.keys())
    html_constructing_data = []
    registry_data = []
    for each_link in tqdm.tqdm(links):
        abstract = main_data[each_link]
        dict_keys = ['local_path', 'link', 'conference', 'year', 'abstract_id',
                     'abstract_name', 'abstract_tag_text', 'additional_content']

        ins_conference = 'AACR'
        ins_year = '2022'
        ins_abstract_id = abstract['Id']
        ins_abstract_link = each_link
        ins_local_path = '/aacr/2022/' + ins_abstract_id + '.html'
        ins_abstract_name = abstract['Title']
        ins_abstract_text = abstract['Abstract']
        html_constructing_data.append([ins_abstract_id, ins_abstract_name, ins_abstract_text, ins_local_path])
        registry_data.append(fill_dict(dict_keys, [ins_local_path, ins_abstract_link, ins_conference, ins_year, ins_abstract_id,
                                                   remove_all_spaces_and_tabs(ins_abstract_name),
                                                   remove_all_spaces_and_tabs(ins_abstract_text), ['No images']]))
    return registry_data, html_constructing_data


def html_the_data(data_to_html):
    for each in tqdm.tqdm(data_to_html):
        file_text = f"""<html>
                        <head>
                        <meta charset="UTF-8">
                        <title>AACR2022 - {each[0]}.</title>
                        </head>
                        <h1>{each[0]}. {each[1]}</h1>
                        <body>{each[2]}</body>
                        </html>"""
        if not os.path.exists(r'./all_data' + '/'.join(each[3].split('/')[:-1])):
            os.makedirs(r'./all_data' + '/'.join(each[3].split('/')[:-1]))
        f = open('./all_data' + each[3], 'w')
        f.write(file_text)
        f.close()


def write_info_to_file(data_list):
    file_path = './all_data/aacr/2022/registry_table.csv'
    with open(file_path, 'w') as target_file:
        writer = csv.writer(target_file)
        writer.writerow(list(data_list[0].keys()))
        for each_row in data_list:
            writer.writerow(each_row.values())



with open('server/temp/presentations.json') as f:
    data = json.load(f)

reg, htmlt = parse_json(data)

html_the_data(htmlt)
write_info_to_file(reg)
