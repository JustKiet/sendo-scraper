from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from csv import DictWriter
import time
import os
import sqlite3
from selenium.webdriver.common.action_chains import ActionChains

def scrape_sendo():
    site = 'sendo'
    options = Options()
    options.headless = False  
    driver = webdriver.Edge(options=options)
    try:
        driver.get("https://www.sendo.vn/")
        time.sleep(5)
        search_element = driver.find_element(By.XPATH, "//input[@class='d7ed-T0Aa7w d7ed-vjfwh6']")
        search_element.send_keys("giầy nam") 
        search_button = driver.find_element(By.XPATH, "//button[@class='d7ed-s0YDb1 d7ed-jQXTxb d7ed-AREzVq d7ed-YaJkXL d7ed-joBgy5 d7ed-DbNJxd']")
        search_button.click()
        time.sleep(10)
        body = driver.find_element(By.TAG_NAME,'body')
        body.send_keys(Keys.PAGE_DOWN)
        body.send_keys(Keys.PAGE_DOWN)
        body.send_keys(Keys.PAGE_DOWN)
        products_wrapper = driver.find_element(By.XPATH, "//div[@class='d7ed-fdSIZS d7ed-OoK3wU d7ed-mPGbtR']")
        products_elements = products_wrapper.find_elements(By.CSS_SELECTOR, "div[class='d7ed-d4keTB d7ed-OoK3wU']")
        data=[]
        comment_content = ""
        star_score = ""
        d_name_spans = ""
        for i in range(min(len(products_elements),1)):
            try:
                products_element = products_elements[i]
                title_link_element = products_element.find_element(By.TAG_NAME, 'a')
                link = title_link_element.get_attribute('href')
                driver.get(link)
                time.sleep(2)
                body = driver.find_element(By.TAG_NAME,'body')
                body.send_keys(Keys.PAGE_DOWN)
                body.send_keys(Keys.PAGE_DOWN)
                body.send_keys(Keys.PAGE_DOWN)
                body.send_keys(Keys.PAGE_DOWN)
                time.sleep(2)
                body.send_keys(Keys.PAGE_DOWN)
                body.send_keys(Keys.PAGE_DOWN)
                title_element= driver.find_element(By.XPATH, "//h1[@class='d7ed-ytwGPk d7ed-zrT4k2 d7ed-kUYEit d7ed-AHa8cD d7ed-mzOLVa']")
                price_element = driver.find_element(By.XPATH, "//span[@class='d7ed-ij7pjf d7ed-AHa8cD d7ed-giDKVr']")
                price = price_element.text
                title = "null"
                score = "0"
                rating_count = "0"
                numbs = "null"
                try:
                    summary_element = driver.find_element(By.XPATH, "//div[@class='_39ab-k3Gyep']")
                    rating_score_average = summary_element.find_element(By.XPATH, "//span[@class='d7ed-ChCxUf d7ed-AHa8cD d7ed-mzOLVa']")
                    rating_count = summary_element.find_element(By.XPATH, "//span[@class='_3141-BtwciV d7ed-KXpuoS d7ed-bjQW4F d7ed-ekib8m']")
                    comments = driver.find_elements(By.XPATH, "//*[@id='id-danh-gia']/div/div[3]/div")
                    comment_contents = ""
                    for comment in comments:
                        star_container = comment.find_element(By.CSS_SELECTOR, "div[class='d7ed-P_QiIC d7ed-GE9WCQ']")
                        star_review = star_container.find_element(By.CSS_SELECTOR, "div.d7ed-ppmM09")
                        get_class_attr = star_review.get_attribute('class')
                        get_star_class = get_class_attr.split(' ')
                        five_star = 'd7ed-AYt6AP'
                        four_star = 'd7ed-vdoKHm'
                        three_star = 'd7ed-LrYHhb'
                        two_star = 'd7ed-tWkzSc'
                        one_star = 'd7ed-ygMGdU'
                        if five_star in get_star_class:
                            star_score = '5 sao'
                        elif four_star in get_star_class:
                            star_score = '4 sao'
                        elif three_star in get_star_class:
                            star_score = '3 sao'
                        elif two_star in get_star_class:
                            star_score = '2 sao'
                        elif one_star in get_star_class:
                            star_score = '1 sao'
                        comment_author = comment.find_element(By.CSS_SELECTOR, "strong[class='_39ab-RycCgu']")
                        author = comment_author.text
                        comment_wrapper = comment.find_element(By.CSS_SELECTOR, "div[class='_39ab-_2vzod']")
                        comment_content = comment_wrapper.find_element(By.TAG_NAME, "p")
                        comment_text = comment_content.text
                        comment_contents = comment_text
                        score = rating_score_average.text
                        numbs = rating_count.text 
                        title = title_element.text
                        row_data = {
                            "product_title":title,
                            "price": price,
                            "rating":score,
                            "total_reviews":numbs,
                            "author": author,
                            "comment_rating":star_score,
                            "comment": comment_contents
                        }
                        
                        data.append(row_data)
                        
                    driver.back()
                    time.sleep(10)
                    products_elements = driver.find_elements(By.CSS_SELECTOR, "div[class='d7ed-d4keTB d7ed-OoK3wU']")
                except NoSuchElementException:
                    driver.back()
                    time.sleep(10)
                    products_elements = driver.find_elements(By.CSS_SELECTOR, "div[class='d7ed-d4keTB d7ed-OoK3wU']")

            except NoSuchElementException:
                continue

        write_headers = not os.path.exists("sendo.csv")
        with open("sendo.csv", "a", newline="", encoding="utf-8") as csv_file:
            fieldnames = [
                  "product_title", "price", "rating", "DG_average_image", "total_reviews", "author", "comment_rating", "comment", 
            ]
            writer = DictWriter(csv_file, fieldnames=fieldnames)
            write_headers = True
            if write_headers:
                writer.writeheader() 
                writer.writerows(data)


    finally:
        conn.close()
        driver.quit()

scrape_sendo() 