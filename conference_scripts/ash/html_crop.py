import csv

import requests
import json
import os
import tqdm
import re

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup


def html_the_data(path, body, number, name):
    file_text = f"""<html>
                    <head>
                    <meta charset="UTF-8">
                    <title>ASH2022-{number}</title>
                    </head>
                    <h1>{number}. {name}</h1>
                    <body>{body}</body>
                    </html>"""
    f = open(path, 'w')

    f.write(file_text)
    f.close()


folder_name = r'./parsed/ash/2022'
file_list = os.listdir(folder_name)


def remove_front_space(line):
    print(line)
    if line != '':
        while line[0] == ' ' or line[0] == '\t':
            print('found space or tab')
            line = line[1:]
            print('cutted it out')
    print(line)
    return line


def parse_html(file_name):
    html = folder_name + '/' + file_name
    html_report_part1 = open(html, 'r').read()
    parsed_html = BeautifulSoup(html_report_part1, "html.parser")
    year = "2022"
    conference = "ASH"
    abstract_id = str(file_name.split('.')[0][5:])
    title = parsed_html.head.find('title').text
    try:
        sub_index= title.index(':')
    except ValueError:
        print(abstract_id)
        print(title)
        return {}
    abs_name = title[title.index(':')+2:]
    if not parsed_html.body:
        print('no body in')
        print(abstract_id)
        return {}

    author_names = parsed_html.body.find('p', attrs={"class": "name"})
    author_names = str(author_names)

    author_names = re.sub('<sup>.{0,15}<\/sup>', '|', author_names)
    author_names = author_names.replace('||', '|')
    author_names = author_names.replace(' and', ',')
    author_names = author_names.replace('|,', '|')
    author_names = re.sub('<.{0,1}b>', '', author_names)
    author_names = author_names.replace('<p class="name">', '')
    author_names = author_names.replace('</p>', '')

    names_list = [author.strip() for author in author_names.split('|') if author]

    if parsed_html.body.find('div', attrs={"class": "abstract"}) is not None:
        text_abstract_dirty = parsed_html.body.find('div', attrs={"class": "abstract"}).next
    else:
        text_abstract_dirty = None
    if text_abstract_dirty is not None:
        add_content = text_abstract_dirty.find_all('img')
        content_list = []
        if len(add_content) > 0:
            for each_img in add_content:
                only_str = str(each_img['src'])
                each_img['src'] = "images/" + only_str.split('/')[-1]
                response = requests.get("https://ash.confex.com" + only_str)
                if not os.path.exists(folder_name + '/images/'):
                    os.makedirs(folder_name + '/images/')
                with open(folder_name + '/images/' + only_str.split('/')[-1], 'wb') as f:
                    f.write(response.content)
                content_list.append("images/" + only_str.split('/')[-1])
        else:
            content_list = ['No images']
        for div in text_abstract_dirty.find_all("div", {'class': 'parents'}):
            div.decompose()
        for div in text_abstract_dirty.find_all("div", {'class': 'siblings'}):
            div.decompose()
    else:
        content_list = ['No images']
    # s = text_abstract_dirty.find_all('img')[0]['src']
    # print('/'.join(s.split('/')[:-1]))

    result_dict = {'local_path': '/ash/2022/' + file_name,
                   'link': 'https://ash.confex.com/ash/2022/webprogram/' + file_name,
                   'conference': conference,
                   'year': year,
                   'abstract_id': abstract_id,
                   'abstract_name': abs_name,
                   'abstract_tag_text': str(text_abstract_dirty)[5:-6],
                   'additional_content': content_list,
                   'authors': names_list,
                   'doi': 'https://doi.org/10.1182/blood-' + year + '-' + abstract_id}
    html_the_data(html, result_dict['abstract_tag_text'], result_dict['abstract_id'], result_dict['abstract_name'])
    return result_dict


def write_info_to_file(data_list):
    file_path = './parsed/ash/2022/registry_table.csv'
    with open(file_path, 'w') as target_file:
        writer = csv.writer(target_file)
        writer.writerow(list(data_list[0].keys()))
        for each_row in data_list:
            writer.writerow(each_row.values())


f_list = os.listdir(folder_name)
if not os.path.exists(r'./parsed/ash/2022/images/'):
    os.makedirs(folder_name + '/images/')

parsings = []
for each_file in tqdm.tqdm(f_list):
    result = parse_html(each_file)
    if result:
        parsings.append(result)

write_info_to_file(parsings)

