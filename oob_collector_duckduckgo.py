from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from time import strftime, localtime, time, sleep
import random
from selenium.common.exceptions import WebDriverException as WE
from pyvirtualdisplay import Display

collect_date = strftime('%y%m%d', localtime(time()))

search_keyword = [
    'onion.city',
    'onion.to',
    'onion.cab',
    'onion.link',
    'onion.lu',
    'onion.rip',
    'onion.nu',
    'onion.lt',
    'onion.direct',
    'tor2web.org',
    'tor2web.fi',
    'torstorm.org',
    'onion.gq',
    'onion.sh'
]

def scroll_to_end_page(driver):
    exist_more_page = True
    page_count = 0

    while exist_more_page == True and page_count < 15:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        page_count += 1
        exist_more_page = not check_exists_by_css(driver,'div.no-results')
        # print(str(exist_more_page))
        sleep(random.randrange(5, 8))

    driver.execute_script("window.scrollTo(0, 0);")
    # print('total '+str(page_count)+'page')


def check_exists_by_css(driver, css):
    try:
        driver.find_element_by_css_selector(css)
    except NoSuchElementException:
        return False
    return True


def crawl_onion_address(driver, keyword, result_file):
    driver.find_element_by_css_selector("input.search__input--adv").clear()
    driver.find_element_by_css_selector("input.search__input--adv").send_keys("site:"+keyword)
    driver.find_element_by_css_selector("input.search__input--adv").send_keys(Keys.RETURN)

    sleep(5)

    if check_exists_by_css(driver, 'div.results_links_deep') == True:
        scroll_to_end_page(driver)

        link_list = driver.find_elements_by_css_selector('h2.result__title')
        for link in link_list:
            try:
                #search_item = link.find_element_by_css_selector('a.result__a')
                search_item = link.find_elements_by_css_selector('a')
                page_title = search_item[0].text
                page_title = page_title.replace("\"", " ")
                page_link = search_item[0].get_attribute('href')
                result_file.write(page_title + '\t' + page_link + '\t' + collect_date + '\n')
                # print(page_title+'\t'+page_link)'''
            except NoSuchElementException:
                result_file.write("Except Occur!!\t" + page_title + "\t" + keyword)
                # print("Except Occur!!")
                # print(page_title)
                # print(keyword)
                break


if __name__ == "__main__":
    virtual_display = Display(visible=0, size=(1024, 960))
    virtual_display.start()

    driver = webdriver.Firefox()
    driver.get('https://duckduckgo.com')

    sleep(1)

    driver.find_element_by_css_selector("input.search__input--adv").clear()
    driver.find_element_by_css_selector("input.search__input--adv").send_keys(random.randrange(0,255))
    driver.find_element_by_css_selector("input.search__input--adv").send_keys(Keys.RETURN)

    sleep(5)

    driver.find_element_by_css_selector("div.search-filters div.dropdown--safe-search").click()
    sleep(2)
    driver.find_elements_by_css_selector("div.modal__body ol.modal__list a")[2].click()
    sleep(5)

    link_list_file = open('new_linkset/' + collect_date + 'duckduckgo_link_list.tsv', 'a', encoding='utf-8')
    link_list_file.write('Title\tLink\tDate\n')

    for keyword in search_keyword:
        crawl_onion_address(driver, keyword, link_list_file)

    driver.quit()
    link_list_file.close()
    virtual_display.stop()
