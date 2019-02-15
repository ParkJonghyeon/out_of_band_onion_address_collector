from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from time import strftime, localtime, time, sleep
#from pyvirtualdisplay import Display
import random

collect_date = strftime('%y%m%d', localtime(time()))

search_keyword = [
    # tor2web proxy TLD
    '.onion.city', '.onion.to', '.onion.cab', '.onion.link', '.onion.lu', '.onion.rip',
    '.onion.nu', '.onion.lt', '.onion.direct', '.tor2web.org', '.tor2web.fi', '.torstorm.org',
    '.onion.gq', '.onion.sh',
    # Keyword
    'Tor .onion',
    'Hidden Service .onion',
    'Tor hidden service'
]

# Facebook account
ID = '01099127538'
PASSWORD = 'lark0321!@#'


def facebook_login(id,pw):
    id_input = driver.find_element_by_id("email")
    id_input.send_keys(id)
    pw_input = driver.find_element_by_id("pass")
    pw_input.send_keys(pw)
    pw_input.send_keys(Keys.RETURN)


def check_exists_by_css(driver, css):
    try:
        driver.find_element_by_css_selector(css)
    except NoSuchElementException:
        return False
    return True


def scroll_to_end_page(driver):
    exist_more_page = True
    page_count = 0
    while exist_more_page == True and page_count < 30:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        page_count += 1
        exist_more_page = not check_exists_by_css(driver,'#browse_end_of_results_footer')
        sleep(random.randrange(5, 8))
    driver.execute_script("window.scrollTo(0, 0);")


def crawl_onion_address(driver, keyword, link_list_file):
    sleep(3)
    search = driver.find_element_by_css_selector("input._1frb")
    search.clear()
    search.send_keys("\"" + keyword + "\"")
    search.send_keys(Keys.RETURN)

    sleep(5)

    public_post=driver.find_element_by_css_selector("div._4-u3._5dwa._33gp span._5dw8 a")
    public_post.click()


    if check_exists_by_css(driver,"#browse_end_of_results_footer") is not True:
        scroll_to_end_page(driver)
    for more_links in driver.find_elements_by_css_selector("a._3084 div._3087"):
        if more_links.text == "See more":
            more_links.click()
    all_text = driver.find_element_by_id("pagelet_loader_initial_browse_result").text
    print(all_text)


if __name__ == "__main__":
    #virtual_display = Display(visible=0, size=(1024, 960))
    #virtual_display.start()

    driver = webdriver.Firefox()
    driver.get('https://www.facebook.com')
    sleep(2)
    facebook_login(ID, PASSWORD)

    #link_list_file = open('new_linkset/' + collect_date + 'facebook_link_list.tsv', 'a', encoding='utf-8')
    link_list_file = open(collect_date + 'facebook_link_list.tsv', 'a', encoding='utf-8')
    link_list_file.write('Title\tLink\tDate\n')
    for keyword in search_keyword:
        crawl_onion_address(driver, keyword, link_list_file)

    driver.quit()
    link_list_file.close()
    #virtual_display.stop()

