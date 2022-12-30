import requests
import json
import os
import tqdm
import re

HEADERS = {
    'Host': 'www.abstractsonline.com',
    'Connection': 'keep-alive',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': ' '.join((
        'Mozilla/5.0 (X11; Linux x86_64)',
        'AppleWebKit/537.36 (KHTML, like Gecko)',
        'Chrome/99.0.4844.84',
        'Safari/537.36'
    )),
    'Backpack': '7d61a318-fbed-4554-ad01-2c59ecc11be5',
    'sec-ch-ua-platform': '"Linux"',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://www.abstractsonline.com/pp8/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8',
    'Cookie': '; '.join((
        '_ga=GA1.2.277052467.1648460515',
        '_gid=GA1.2.513389964.1648460515',
        'backpack=7d61a318-fbed-4554-ad01-2c59ecc11be5',
        'backpackExpiration=Tue%2C%2029%20Mar%202022%2000%3A42%3A01',
        'AWSALB=CO3PI1QDdox/mghx/3PAa+9vS14Xav8to1MMejs1+jepjZpjMCnwZ1wyYz4rjzkEttSrdelGUbM5O7hGx2iwA4nYtTP4PQ5XDFI7uh9/QwsKGI3Mzt4kXrx4PRJl',
        'AWSALBCORS=CO3PI1QDdox/mghx/3PAa+9vS14Xav8to1MMejs1+jepjZpjMCnwZ1wyYz4rjzkEttSrdelGUbM5O7hGx2iwA4nYtTP4PQ5XDFI7uh9/QwsKGI3Mzt4kXrx4PRJl'
    ))
}

from bs4 import BeautifulSoup

url_start = 'https://ash.confex.com/ash/2022/webprogram/'
#os.mkdir('loaded_lymphoid_oral')

def repl(matchobj):
    print('WE ARE REPLACING')
    return f'<div class="abstract"><div><p>'

with open('./ash2022/Lymphoid_Malignancies_papers.json', 'r', encoding='utf-8') as f:
    text = json.load(f)
print(type(text))
for each_abstract in tqdm.tqdm(text):
    print(each_abstract)
    r = requests.get(each_abstract)
    if not os.path.exists(r'./all_data/ash/2022/'):
        os.makedirs(r'./all_data/ash/2022/')
    if not os.path.exists('./all_data/ash/2022/'+each_abstract.split('/')[-1].split('.')[0]+'.html'):
        with open('./all_data/ash/2022/'+each_abstract.split('/')[-1].split('.')[0]+'.html', 'w') as output_file:
            subbed_text = re.sub(r"(<div class=\"abstract\">(?:\n*|\t*|\s*)(?:\S{5}))", repl, r.text)
            htmled_text = BeautifulSoup(subbed_text, "html.parser")
            metatag = htmled_text.new_tag('meta')
            metatag.attrs['charset'] = 'UTF-8'
            htmled_text.head.append(metatag)
            output_file.write(str(htmled_text))