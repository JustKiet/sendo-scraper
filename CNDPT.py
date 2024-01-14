from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from csv import DictWriter
import time
import os
from selenium.webdriver.common.action_chains import ActionChains

def dangkitinchi():
    options = Options()
    options.headless = False  
    driver = webdriver.Edge()
    try:
        # Truy cập vào trang web
        driver.get("https://www.sendo.vn/")
        search_element = driver.find_element(By.CSS_SELECTOR("input[@class='d7ed-T0Aa7w d7ed-vjfwh6']"))
        search_element.send_keys("smartphone") 
        search_button = driver.find_element(By.CSS_SELECTOR("button[@class='d7ed-s0YDb1 d7ed-jQXTxb d7ed-AREzVq d7ed-YaJkXL d7ed-joBgy5 d7ed-DbNJxd']"))
        search_button.click()
        current_page_url = driver.current_url  # Lưu trữ URL trang hiện tại
        products_elements = driver.find_elements(By.CSS_SELECTOR, ".d7ed-d4keTB .d7ed-OoK3wU")
        data=[]
        star_urls=[]
        star_urls_per = []
        comment_content =""
        d_name_spans=""
        for i in range(min(len(products_elements),6)):
            products_element = products_elements[i]
            title_link_element = products_element.find_element(By.TAG_NAME, "a")
            link = title_link_element.get_attribute("href")
            driver.get(link)
            time.sleep(2)
            body = driver.find_element(By.TAG_NAME,'body')
            body.send_keys(Keys.PAGE_DOWN)
            body.send_keys(Keys.PAGE_DOWN)
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(20)
            title_element= driver.find_element(By.CSS_SELECTOR("h1[@class='d7ed-ytwGPk d7ed-zrT4k2 d7ed-kUYEit d7ed-AHa8cD d7ed-mzOLVa']"))
            summary_element = driver.find_element(By.CLASS_NAME,"_39ab-k3Gyep")
            rating_score_average = summary_element.find_element(By.CSS_SELECTOR("span[@class='d7ed-ChCxUf d7ed-AHa8cD d7ed-mzOLVa']"))
            rating_count = summary_element.find_element(By.CSS_SELECTOR("span[@class='_3141-BtwciV d7ed-KXpuoS d7ed-bjQW4F d7ed-ekib8m']"))
            comments = driver.find_elements(By.CSS_SELECTOR("div[@class='_39ab-RXeRpQ']"))
            comment_contents = []  # List to store comment_content for all items
            for comment in comments:
                star_score_per = comment.find_element(By.CSS_SELECTOR, ".top .container-star")
                star_images_per = star_score_per.find_elements(By.TAG_NAME, "img")
                star_urls_per = []
                for star_image_per in star_images_per:
                    star_url_per = star_image_per.get_attribute("src")
                    star_urls_per.append(star_url_per)
                d_name_spans = comment.find_elements(By.CSS_SELECTOR, ".middle span")
                comment_content = comment.find_element(By.CSS_SELECTOR, ".item-content .content")
                comment_text = comment_content.text
                comment_contents.append(comment_text)  # Append comment_text to the list


            # Lấy nội dung của các phần tử khác
            title = title_element.text
            score = rating_score_average.text
            numbs = rating_count.text 
            # username = d_name_spans[0].text
            # verify = d_name_spans[2].text

            row_data={
                "TenSP":title,
                "DG":score,
                "DG_average_image":star_urls,
                "SoDG":numbs,
                # "TenHienthi":username,
                # "verify":verify,
                "comment_DG":star_urls_per,
                "comment":comment_contents

            }

            data.append(row_data)

            driver.back()
            products_elements = driver.find_elements(By.CSS_SELECTOR, ".Bm3ON")

        # Kiểm tra xem tập tin đã tồn tại chưa để xác định việc ghi headers hay không
        write_headers = not os.path.exists("lazada.csv")

        # Ghi dữ liệu vào file CSV
        with open("lazada.csv", "a", newline="", encoding="utf-8") as csv_file:
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
dangkitinchi()
