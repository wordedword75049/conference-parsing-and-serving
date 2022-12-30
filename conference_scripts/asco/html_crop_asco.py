import csv

import requests
import json
import os
import tqdm
from pyparsing import unicode

try:
    from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup
except ImportError:
    from bs4 import BeautifulSoup, BeautifulStoneSoup

import html




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
    while " <b>" in line:
        ind = line.index(" <b>")
        line = line[:ind] + " <br><b>" + line[ind + 4:]
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
    registry_data = []
    for abstract in tqdm.tqdm(main_data):
        dict_keys = ['local_path', 'link', 'conference', 'year', 'abstract_id', 'abstract_name',
                     'abstract_tag_text', 'additional_content']

        ins_conference = 'ASCO'
        ins_year = '2022'
        ins_link = 'https://meetings.asco.org/abstracts-presentations/'+abstract['id']
        ins_paper_id = abstract['id']
        ins_local_path = '/asco/2022/' + ins_paper_id + '.html'
        ins_abstract_name = html.unescape(abstract['title'])
        ins_abstract_text = html.unescape(remove_all_spaces_and_tabs(abstract['text']))
        registry_data.append(fill_dict(dict_keys, [ins_local_path, ins_link, ins_conference, ins_year, ins_paper_id, clean_tags_from_text(ins_abstract_name),
                                                   ins_abstract_text, ['No images']]))
        html_the_data([ins_paper_id, ins_abstract_name, ins_abstract_text, ins_local_path])
    return registry_data


def html_the_data(each):
    file_text = f"""<html>
                    <head>
                    <meta charset="UTF-8">
                    <title>ASCO2022 - {each[0]}.</title>
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
    file_path = './asco_2022.csv'
    with open(file_path, 'w') as target_file:
        writer = csv.writer(target_file)
        writer.writerow(list(data_list[0].keys()))
        for each_row in data_list:
            writer.writerow(each_row.values())

with open('./parsed_asco_texts.json') as f:
    data = json.load(f)

reg=parse_json(data)

write_info_to_file(reg)

