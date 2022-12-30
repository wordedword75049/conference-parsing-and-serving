from dataclasses import dataclass
import os
import tqdm

from contextlib import contextmanager

@contextmanager
def disable_ssl_warnings():
    import warnings
    import urllib3

    with warnings.catch_warnings():
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        yield None


import requests
from simple_parsing import ArgumentParser, field


@dataclass
class Options:
    input: str  # Path to input file
    url: str  # URL to Gateway API
    conf: str  # Conference to which files belong to
    year: str  # Year in which conference was held


def send_from_path(path, gateway_url, conference, year):
    if os.path.isfile(path):
        _, extension = os.path.splitext(path)
        print('sending ' + path + ' with extension ' + extension)
        if extension == '.csv':
            filetype = 'registry'
        elif extension == '.html':
            filetype = 'abstract'
        else:
            filetype = 'image'

        sent = False
        while not sent:
            # try:
            full_link = gateway_url + '/upload?type=' + filetype + '&conference=' + conference + '&year=' + year
            with disable_ssl_warnings():
                insert = requests.post(full_link, files={'file': open(path, 'rb')}, verify=False)
                insert.raise_for_status()
            sent = True
            print('succesfully sent')
            # except Exception:
            #     print('not sent')


    elif os.path.isdir(path):
        print('found dir ' + path)
        files_in_dir = os.listdir(path)
        for each_path in tqdm.tqdm(files_in_dir):
            new_path = path+'/'+each_path if path[-1] != '/' else path+each_path
            send_from_path(new_path, gateway_url, conference, year)
    else:
        print('something unusual like that ' + path)




if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_arguments(Options, dest="options")
    args = parser.parse_args()
    send_from_path(args.options.input, args.options.url, args.options.conf, args.options.year)


