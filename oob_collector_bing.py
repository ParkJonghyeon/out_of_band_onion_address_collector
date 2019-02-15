from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from time import strftime, localtime, time, sleep
import random
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

def refresh_if_error_page(driver):
    trial_count = 3
    while check_exists_by_css(driver, 'a#errorCode') == True:
        try:
            driver.refresh()
            sleep(5)
            trial_count -= 1
            print("error page. count = "+str(trial_count))
            if trial_count < 1:
                break
        except WebDriverException:
            continue


def next_page_exist_check(driver):
    if check_exists_by_css(driver, "a.sb_pagN"):
        try:
            current_page_num = int(driver.find_element_by_css_selector('a.sb_pagS').text)
            if current_page_num > 15 and current_page_num % (random.randrange(6, 8)) == 0:
                try:
                    driver.refresh()
                except WebDriverException:
                    refresh_if_error_page(driver)
                sleep(7)

            driver.find_element_by_link_text(str(current_page_num + 1)).click()
            refresh_if_error_page(driver)
            sleep(random.randrange(7, 15))

            new_page_num = int(driver.find_element_by_css_selector('a.sb_pagS').text)
            if current_page_num >= new_page_num:
                return False
            return True

        except NoSuchElementException:
            return False
    else:
        return False


def check_exists_by_css(driver, css):
    try:
        driver.find_element_by_css_selector(css)
    except NoSuchElementException:
        return False
    return True


def crawl_onion_address(driver, keyword, result_file):
    refresh_if_error_page(driver)
    sleep(7)
    driver.find_element_by_id("sb_form_q").clear()
    driver.find_element_by_id("sb_form_q").send_keys("site:"+keyword)
    driver.find_element_by_id("sb_form_q").send_keys(Keys.RETURN)
    sleep(7)
    refresh_if_error_page(driver)

    page_remain = True
    while page_remain == True:
        if check_exists_by_css(driver, 'li.b_algo') == True:
            link_list = driver.find_elements_by_css_selector('li.b_algo')
            for link in link_list:
                search_item = link.find_element_by_css_selector('h2 a')
                page_title = search_item.text
                page_title = page_title.replace("\"", " ")
                page_link = search_item.get_attribute('href')
                result_file.write(page_title + '\t' + page_link + '\t' + collect_date + '\n')
                #print(page_title+'\t'+page_link)
            page_remain = next_page_exist_check(driver)

            # sleep(random.randrange(30, 60))
        else:
            page_remain = False


if __name__ == "__main__":
    virtual_display = Display(visible=0, size=(1024, 960))
    virtual_display.start()

    driver = webdriver.Firefox()
    driver.get('https://www.bing.com')
    refresh_if_error_page(driver)

    sleep(1)

    link_list_file = open('new_linkset/' + collect_date + 'bing_link_list.tsv', 'a', encoding='utf-8')
    link_list_file.write('Title\tLink\tDate\n')
    for keyword in search_keyword:
        crawl_onion_address(driver, keyword, link_list_file)

    driver.quit()
    link_list_file.close()
    virtual_display.stop()
