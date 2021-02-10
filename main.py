from concurrent.futures.thread import ThreadPoolExecutor

import requests
from bs4 import BeautifulSoup
import pandas_read_xml as pdx
import pandas as pd
BASE_URL = 'https://www.cnbc.com/sitemapAll.xml'

def fetch_cnbc_urls():
    """Fetch cnbc urls that contains tesla and persist"""
    tesla_urls = []
    response = requests.get(BASE_URL)
    with open('cnbcBaseUrl.xml', 'wb') as file_handler:
        file_handler.write(response.content)
    df = pdx.read_xml("cnbcBaseUrl.xml", ['sitemapindex'])
    xml_url_list = [x['loc'] for x in df.sitemap]
    print(xml_url_list)

    for url in xml_url_list:
        if url.find('CNBCsitemapAll10.xml') != -1:
            resp = requests.get(url)
            file_name = url.split('/')[3]
            with open(file_name, 'wb') as file_handler:
                file_handler.write(resp.content)
            df = pdx.read_xml(file_name, ['urlset'])
            page_url_list = [x['loc'] for x in df.url if str(x['loc']).find('tesla') != -1]
            print(page_url_list)

            tesla_urls.extend(page_url_list)

    tesla_urls_df = pd.DataFrame(columns=['tesla_url'], data=tesla_urls)
    tesla_urls_df.to_csv('tesla_urls_All10.csv', index=False)
    print('total urls for All10: ', len(tesla_urls))

def fetch_and_save_tesla_content():
    """Fetch content from individual tesla urls from cnbc website and persist."""
    tesla_content = []
    tesla_urls_df = pd.read_csv('tesla_urls_All10.csv')
    future_list = []
    try:
        with ThreadPoolExecutor(max_workers=5) as executor:
            for i, url in enumerate(tesla_urls_df.tesla_url):
                future = executor.submit(make_http_call_to_cnbc_for_data_to_analyze, url)
                future_list.append(future)
                print(i, url)

        for data in future_list:
            tesla_content.extend(data.result())
    except Exception as exception:
        print(exception)

    tesla_content_df = pd.DataFrame(columns=['tesla_content'], data=tesla_content)
    tesla_content_df.to_csv('tesla_content.csv', index=False)

def make_http_call_to_cnbc_for_data_to_analyze(url):
    """extract title and description from cnbc tesla urls"""
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    print('content read: ', url)
    content1 = ''
    content2 = ''
    for title in soup.findAll('meta', attrs={'name': 'twitter:title'}):
        title_attrs = title.attrs
        if title_attrs is not None and 'content' in title_attrs:
            content1 = title_attrs['content']
            print('actual title content: ', content1)
    for description in soup.findAll('meta', attrs={'name': 'twitter:description'}):
        description_attrs = description.attrs
        if description_attrs is not None and 'content' in description_attrs:
            content2 = description_attrs['content']
            print('actual description content: ', content2)
    return content1, content2

if __name__ == '__main__':
    print('---Fetch And Save CNBC Tesla Data---')
    fetch_cnbc_urls()
    fetch_and_save_tesla_content()
