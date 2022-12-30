from dataclasses import dataclass
import os

from contextlib import contextmanager
import tqdm
@contextmanager
def disable_ssl_warnings():
    import warnings
    import urllib3

    with warnings.catch_warnings():
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        yield None


import requests
from simple_parsing import ArgumentParser, field
try:
    from BeautifulSoup4 import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup



@dataclass
class Options:
    input: str  # Path to input file


def html_the_data(path, body, number, name):
    file_text = f"""<html>
                    <head>
                    <meta charset="UTF-8">
                    <title>ASH2020-{number}.</title>
                    </head>
                    <h1>{number}. {name}</h1>
                    <body>{body}</body>
                    </html>"""
    f = open(path, 'w')

    f.write(file_text)
    f.close()


def reparse_from_path(path):
    if os.path.isfile(path):
        _, extension = os.path.splitext(path)
        if extension == '.html':
            html_file = open(path, 'r').read()
            parsed_html = BeautifulSoup(html_file, "html.parser")
            new_html = BeautifulSoup()
            main_body = parsed_html.find('div', attrs={"class": "rightAside"})
            title = main_body.find('h2', attrs={"class": "subtitle"})
            content = main_body.find('div', attrs={"class": "content"})
            if title.find('span', attrs={"class": "number"}) is not None:
                abs_number = str(parsed_html.body.find('span', attrs={"class": "number"}).text)
            else:
                abs_number = 'U/N'
            abs_name = title.text[7:]
            for img in content.find_all('img'):
                img_url = img['src']
                img['src'] = "images/" + img_url.split('/')[-1]
            for div in content.find_all("div", {'class': 'parents'}):
                div.decompose()
            for div in content.find_all("div", {'class': 'siblings'}):
                div.decompose()
            html_the_data(path, content, abs_number, abs_name)



    elif os.path.isdir(path):
        print('found dir ' + path)
        files_in_dir = os.listdir(path)
        for each_path in files_in_dir:
            new_path = path+'/'+each_path if path[-1] != '/' else path+each_path
            reparse_from_path(new_path)
    else:
        print('something unusual like that ' + path)




if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_arguments(Options, dest="options")
    args = parser.parse_args()
    reparse_from_path(args.options.input)


