import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import unittest

chrome_driver_path = 'C:\\Users\\Yao\\.cache\\selenium\\chromedriver\\win64\\117.0.5938.62'

try:
    driver = webdriver.Chrome(chrome_driver_path)
    print('Chrome driver initialized successfully.')
except Exception as e:
    print(f"Error initializing Chrome driver: {e}")
    exit()

def get_walmart_price():
    try:
        driver.get('https://www.walmart.ca/en')
        print('Opened the Walmart page.')

        search_box = driver.find_element(By.NAME, 'q')
        search_box.send_keys('fairlife milk')
        print('Entered "fairlife milk" into the search box.')

        search_button = driver.find_element(By.NAME, 'Search icon')
        search_button.click()
        print('Clicked the search button.')

        wait = WebDriverWait(driver, 10)
        # Wait for the search to load dynamically
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.product-price > span.visuallyhidden')))
        print('Waited for search links to load dynamically.')

        products = driver.find_elements(By.CSS_SELECTOR, 'div.product-title-link a')
        prices = driver.find_elements(By.CSS_SELECTOR, 'div.product-price > span.visuallyhidden')

        product_prices = []
        for product, price in zip(products, prices):
            product_prices.append({'product': product.text, 'price': price.text})

        return product_prices
    except Exception as e:
        print(f"Error in get_walmart_price: {e}")
        return []

def save_to_csv(products_prices):
    try:
         timestamp = time.strftime('%Y%m%d%H%M%S')
        filename = f'fairlife_milk_prices_{timestamp}.csv'
        ith open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Product', 'Price'])
            for item in products_prices:
                writer.writerow([item['product'], item['price']])
        print(f'Saved data to CSV file: {filename}')
    except Exception as e:
        print(f"Error in save_to_csv: {e}")

class TestFairlifeMilkScraper(unittest.TestCase):
    def test_get_walmart_prices(self):
        product_prices = get_walmart_prices()
        self.assertIsInstance(product_prices, list)
        self.assertTrue(all(isinstance(item, dict) and 'product' in item and 'price' in item for item in product_prices))
        print('Test for get_walmart_prices passed.')

    def test_parse_news_article(self):
        url = 'https://example.com/news_article'
        news_data = parse_news_article(url)
        self.assertIsInstance(news_data, dict)
        self.assertIn('title', news_data)
        self.assertIn('content', news_data)
        self.assertIsInstance(news_data['title'], str)
        self.assertIsInstance(news_data['content'], str)
        print('Test for parse_news_article passed.')

    def test_save_to_csv(self):
        test_data = [{'title': 'Test Title 1', 'content': 'Test Content 1'},
                     {'title': 'Test Title 2', 'content': 'Test Content 2'}]

        save_to_csv(test_data)

        import os
        self.assertTrue(os.path.isfile('tesla_news.csv'))
        print('Test for save_to_csv passed.')

        with open('tesla_news.csv', mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)
            self.assertEqual(header, ['Title', 'Content'])

            row1 = next(reader)
            self.assertEqual(row1, ['Test Title 1', 'Test Content 1'])

            row2 = next(reader)
            self.assertEqual(row2, ['Test Title 2', 'Test Content 2'])

if __name__ == '__main__':
    try:
        unittest.main()
        print('All tests passed successfully.')
    except Exception as e:
        print(f"Error in running tests: {e}")
    finally:
        driver.quit()
        print('Chrome driver quit.')
