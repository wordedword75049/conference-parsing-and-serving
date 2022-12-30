import csv
import re

import requests
import json
import os
import tqdm

try:
    from BeautifulSoup import BeautifulSoup, Tag
except ImportError:
    from bs4 import BeautifulSoup, Tag

if not os.path.exists(r'./all_data/esmo/2021/'):
    os.makedirs(r'./all_data/esmo/2021/')

folder_name = './all_data/esmo_2021/data'
file_list = os.listdir(folder_name)

with open("./all_data/esmo_2021/links.json") as jsonFile:
    links_arr = json.load(jsonFile)
    jsonFile.close()


def detablify(text):
    if 'table>' in text:
        list_res = text.split('table>')
        return list_res[0][:-14] + list_res[2]
    return text


def parse_html(file_name):
    has_text = 1
    conference = "ESMO"
    year = "2021"
    journal = "ESMO2021"
    abst_number = file_name.split('.')[0][8:]
    html = folder_name + '/' + file_name

    with open(html, 'r', encoding="UTF-8") as html_report_part1:
        nct_number = re.findall(r'NCT\d{6,}', str(html_report_part1))
        parsed_html = BeautifulSoup(html_report_part1, "html.parser")
        nct_number = list(set(re.findall(r'NCT\d{6,}', str(parsed_html))))
        temp_str = ''
        for each in nct_number:
            if temp_str:
                temp_str += ', '
            temp_str += each
        nct_number = temp_str
        session_name = parsed_html.body.find('h2', attrs={"class": "full-page-title full-page-title-small"}).find('span',
                                                                                                                  attrs={
                                                                                                                      "class": "ezstring-field"}).next
        art_title = parsed_html.body.find('h1', attrs={"class": "full-page-title full-page-title-small"}).find('span',
                                                                                                               attrs={
                                                                                                                   "class": "ezstring-field"}).next
        # print(str(file_name))
        # print(title)
        content = parsed_html.body.find('div', attrs={"class": "full-article-content"})
        number = content.find('h4', attrs={"class": "title"}).next.split(' ')[-1]
        if number == "Abstract":
            number = "-"
        # print(number)

        dirty_text = detablify(
            str(content.find('div', attrs={"class": "expand-content"})).split('<div class="expand-spacer">')[0].split(
                '<div class="expand-content">')[-1])

    soup = BeautifulSoup(features="html.parser")
    html = Tag(soup, name="html")
    meta = Tag(soup, name="meta", attrs={"charset": "UTF-8"})
    head = Tag(soup, name="head")
    title = Tag(soup, name="title")
    body = Tag(soup, name="body")
    h4 = Tag(soup, name="h4")
    h1 = Tag(soup, name="h1")
    soup.append(html)
    html.append(head)
    head.append(meta)
    head.append(title)
    title.append(art_title)
    html.append(body)
    body.append(h1)
    h1.append(art_title)
    body.append(h4)
    h4.append(content.find('h4', attrs={"class": "title"}).next)
    body.append(content.find('div', attrs={"class": "expand-content"}))
    # with open('./all_data/esmo/2021/' + file_name, 'w', encoding="UTF-8") as output_file:
    #     output_file.write(soup.prettify())

    result_dict = {'local_path': '/esmo/2021/' + file_name,
                   'link': links_arr[int(file_name.split('.')[0].split('abstract')[-1])],
                   'has_text': has_text,
                   'conference': conference,
                   'year': year,
                   'abstract_id': abst_number,
                   'paper_id': number,
                   'journal': journal,
                   'nct_id': nct_number,
                   'abstract_name': art_title,
                   'session_name': session_name,
                   'abstract_tag_text': dirty_text}

    return result_dict


def write_info_to_file(data_list):
    file_path = './registry-table.csv'
    with open(file_path, 'w') as target_file:
        writer = csv.writer(target_file)
        writer.writerow(list(data_list[0].keys()))
        for each_row in data_list:
            writer.writerow(each_row.values())


f_list = os.listdir(folder_name)
parsings = []
for each_file in tqdm.tqdm(f_list):
    parsings.append(parse_html(each_file))

write_info_to_file(parsings)
