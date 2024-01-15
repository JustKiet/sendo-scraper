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
from selenium.webdriver.common.action_chains import ActionChains

def scrape_sendo():
    options = Options()
    options.headless = False  
    driver = webdriver.Edge(options=options)
    try:
        # Truy cập vào trang web
        driver.get("https://www.sendo.vn/")
        time.sleep(5)
        search_element = driver.find_element(By.XPATH, "//input[@class='d7ed-T0Aa7w d7ed-vjfwh6']")
        search_element.send_keys("smartphone") 
        search_button = driver.find_element(By.XPATH, "//button[@class='d7ed-s0YDb1 d7ed-jQXTxb d7ed-AREzVq d7ed-YaJkXL d7ed-joBgy5 d7ed-DbNJxd']")
        search_button.click()
        time.sleep(10)
        current_page_url = driver.current_url  # Lưu trữ URL trang hiện tại
        products_wrapper = driver.find_element(By.XPATH, "//div[@class='d7ed-fdSIZS d7ed-OoK3wU d7ed-mPGbtR']")
        products_elements = products_wrapper.find_elements(By.CSS_SELECTOR, "div[class='d7ed-d4keTB d7ed-OoK3wU']")
        data=[]
        comment_content = ""
        star_score = []
        d_name_spans = ""
        for i in range(min(len(products_elements),6)):
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
            title = "null"
            score = "0"
            rating_count = "0"
            numbs = "null"
            try:
                summary_element = driver.find_element(By.XPATH, "//div[@class='_39ab-k3Gyep']")
                rating_score_average = summary_element.find_element(By.XPATH, "//span[@class='d7ed-ChCxUf d7ed-AHa8cD d7ed-mzOLVa']")
                rating_count = summary_element.find_element(By.XPATH, "//span[@class='_3141-BtwciV d7ed-KXpuoS d7ed-bjQW4F d7ed-ekib8m']")
                comments = driver.find_elements(By.XPATH, "//*[@id='id-danh-gia']/div/div[3]/div")
                comment_contents = []  # List to store comment_content for all items
                for comment in comments:
                    #star_container = comment.find_element(By.CSS_SELECTOR, "div[class='d7ed-P_QiIC d7ed-GE9WCQ']")
                    #star_rating = star_container.find_element(By.CSS_SELECTOR, "div.d7ed-ppmM09')]")
                    #if star_rating.find_element(By.XPATH, "//div[contains(@class, 'd7ed-AYt6AP')]"):
                    #    star_score.append('5')
                    #elif star_rating.find_element(By.XPATH, "//div[contains(@class, 'd7ed-vdoKHm')]"):
                    #    star_score.append('4')
                    #elif star_rating.find_element(By.XPATH, "//div[contains(@class, 'd7ed-LrYHhb')]"):
                    #    star_score.append('3')
                    #elif star_rating.find_element(By.XPATH, "//div[contains(@class, 'd7ed-tWkzSc')]"):
                    #    star_score.append('2')
                    #elif star_rating.find_element(By.XPATH, "//div[contains(@class, 'd7ed-ygMGdU')]"):
                    #    star_score.append('1')
                    comment_wrapper = comment.find_element(By.CSS_SELECTOR, "div[class='_39ab-_2vzod']")
                    comment_content = comment_wrapper.find_element(By.TAG_NAME, "p")
                    comment_text = comment_content.text
                    comment_contents.append(comment_text)  # Append comment_text to the list
                score = rating_score_average.text
                numbs = rating_count.text 
                title = title_element.text
                row_data= {
                    "TenSP":title,
                    "DG":score,
                    "SoDG":numbs,
                    # "TenHienthi":username,
                    # "verify":verify,
                    #"comment_DG":star_score,
                    "comment":comment_contents
                }

                data.append(row_data)
                
                driver.back()
                time.sleep(3)
                products_elements = driver.find_elements(By.CSS_SELECTOR, "div[class='d7ed-d4keTB d7ed-OoK3wU']")
            except NoSuchElementException:
                driver.back()
                time.sleep(3)
                products_elements = driver.find_elements(By.CSS_SELECTOR, "div[class='d7ed-d4keTB d7ed-OoK3wU']")

        # Kiểm tra xem tập tin đã tồn tại chưa để xác định việc ghi headers hay không
        write_headers = not os.path.exists("sendo.csv")

        # Ghi dữ liệu vào file CSV
        with open("sendo.csv", "a", newline="", encoding="utf-8") as csv_file:
            fieldnames = [
                    "TenSP", "DG", "DG_average_image", "SoDG","comment_DG","comment"
                ]
            writer = DictWriter(csv_file, fieldnames=fieldnames)
            write_headers = True

            if write_headers:
                writer.writeheader()  # Ghi headers chỉ khi tập tin mới

            writer.writerows(data)

    finally:
        # Đóng trình duyệt
        driver.quit()

# Call the function
scrape_sendo()