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

def get_walmart_prices():
    try:
        driver.get('https://www.walmart.ca/en')
        print('Opened the Walmart page.')

        search_box = driver.find_element(By.NAME, 'q')
        search_box.send_keys('fairlife milk')
        print('Entered "fairlife milk" into the search box.')

        search_button = driver.find_element(By.XPATH, '//button[@data-automation-id="search-submit-btn"]')
        search_button.click()
        print('Clicked the search button.')

        wait = WebDriverWait(driver, 10)
        # Wait for the search to load dynamically
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.product-price > span.visuallyhidden')))
        print('Waited for search results to load dynamically.')

        products = driver.find_elements(By.CSS_SELECTOR, 'div.product-title-link a')
        prices = driver.find_elements(By.CSS_SELECTOR, 'div.product-price > span.visuallyhidden')

        product_prices = []
        for product, price in zip(products, prices):
            product_prices.append({'product': product.text, 'price': price.text})

        return product_prices
    except Exception as e:
        print(f"Error in get_walmart_prices: {e}")
        return []

def get_superstore_prices():
    try:
        driver.get('https://www.realcanadiansuperstore.ca/')
        print('Opened the Superstore page.')

        search_box = driver.find_element(By.ID, 'search')
        search_box.send_keys('fairlife milk')
        print('Entered "fairlife milk" into the search box.')

        search_button = driver.find_element(By.XPATH, '//button[@class="btn btn-search"]')
        search_button.click()
        print('Clicked the search button.')

        wait = WebDriverWait(driver, 10)
        # Wait for the search to load dynamically
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.product-details')))
        print('Waited for search results to load dynamically.')

        products = driver.find_elements(By.CSS_SELECTOR, 'div.product-details h3 a')
        prices = driver.find_elements(By.CSS_SELECTOR, 'div.price')

        product_prices = []
        for product, price in zip(products, prices):
            product_prices.append({'product': product.text, 'price': price.text})

        return product_prices
    except Exception as e:
        print(f"Error in get_walmart_prices: {e}")
        return []

def get_saveonfood_prices():
    try:
        driver.get('https://www.saveonfoods.com/sm/pickup/rsid/1982/')
        print('Opened the Save On Food page.')

        search_box = driver.find_element(By.NAME, 'q')
        search_box.send_keys('fairlife milk')
        print('Entered "fairlife milk" into the search box.')

        search_button = driver.find_element(By.XPATH, '//button[@data-automation-id="search-submit-btn"]')
        search_button.click()
        print('Clicked the search button.')

        wait = WebDriverWait(driver, 10)
        # Wait for the search to load dynamically
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.product-price > span.visuallyhidden')))
        print('Waited for search results to load dynamically.')

        products = driver.find_elements(By.CSS_SELECTOR, 'div.product-title-link a')
        prices = driver.find_elements(By.CSS_SELECTOR, 'div.product-price > span.visuallyhidden')

        product_prices = []
        for product, price in zip(products, prices):
            product_prices.append({'product': product.text, 'price': price.text})

        return product_prices
    except Exception as e:
        print(f"Error in get_walmart_prices: {e}")
        return []


def save_to_csv(products_prices):
    try:
        timestamp = time.strftime('%Y%m%d%H%M%S')
        filename = f'fairlife_milk_prices_{timestamp}.csv'
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
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

    def test_save_to_csv(self):
        test_data = [{'product': 'Fairlife Milk 1', 'price': '$2.99'},
                     {'product': 'Fairlife Milk 2', 'price': '$3.49'}]

        save_to_csv(test_data)

        import os
        self.assertTrue(os.path.isfile('fairlife_milk_prices.csv'))
        print('Test for save_to_csv passed.')

        with open('fairlife_milk_prices.csv', mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)
            self.assertEqual(header, ['Product', 'Price'])

            row1 = next(reader)
            self.assertEqual(row1, ['Fairlife Milk 1', '$2.99'])

            row2 = next(reader)
            self.assertEqual(row2, ['Fairlife Milk 2', '$3.49'])

if __name__ == '__main__':
    try:
        unittest.main()
        print('All tests passed successfully.')
    except Exception as e:
        print(f"Error in running tests: {e}")
    finally:
        driver.quit()
        print('Chrome driver quit.')
