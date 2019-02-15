from googleapiclient.discovery import build
from time import strftime, localtime, time
import sys

collect_date = strftime('%y%m%d', localtime(time()))

search_keyword = [
    'onion.city',
    'onion.to',
    'onion.cab',
    'onion.link',
    'onion.lu',
    'onion.rip',
    'onion.nu'
]


APIKeys = [ "Google search API key" ]

search_engine_ID = 'Google search engine AIP key'


def get_search_result(service, keyword):
    res = service.cse().list(
        q='site:'+keyword,
        cx=search_engine_ID,
        dateRestrict='y[1]',
        googlehost='google.com',
        siteSearch=keyword,
        siteSearchFilter='i',).execute()
    return res


def next_page_exist(service, currentpage, keyword):
    if currentpage['queries'].__contains__('nextPage') is True:
        start_index = currentpage['queries']['nextPage'][0]['startIndex']

        if start_index < 100:
            next_res = service.cse().list(
                q='site:' + keyword,
                cx=search_engine_ID,
                dateRestrict='y[1]',
                googlehost='google.com',
                siteSearch=keyword,
                siteSearchFilter='i',
                start=start_index
            ).execute()
            return next_res
        else:
            return None
    else:
        return None


def get_onion_address(service, currentpage, keyword, result_file):

    search_result_num = int(currentpage['searchInformation']['totalResults'])

    while currentpage != None and search_result_num > 0:
        for item in currentpage['items']:
            page_title = item['htmlTitle']
            page_title = page_title.replace("\"", " ")
            page_link = item['link']
            result_file.write(page_title + '\t' + page_link + '\t' + collect_date + '\n')
            #print(item_title+"\t"+item_link)
        currentpage = next_page_exist(service, currentpage, keyword)
        if currentpage != None:
            search_result_num = int(currentpage['searchInformation']['totalResults'])


def main(API_num):
    service = build("customsearch", "v1", developerKey=APIKeys[API_num])

    link_list_file = open('new_linkset/' + collect_date + 'google_customS_link_list_A.tsv', 'a', encoding='utf-8')
    link_list_file.write('Title\tLink\tDate\n')

    for keyword in search_keyword:
        search_result_resorce = get_search_result(service,keyword)
        get_onion_address(service, search_result_resorce, keyword, link_list_file)

    link_list_file.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Require API num value(0-3)')
    else:
        main(int(sys.argv[1]))
