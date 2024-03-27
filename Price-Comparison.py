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


def get_walmart_prices(product_name):
    try:
        driver.get('https://www.walmart.ca/en')
        print('Opened the Walmart page.')

        search_box = driver.find_element(By.NAME, 'q')
        search_box.send_keys(product_name)
        print(f'Entered "{product_name}" into the search box.')

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


def get_superstore_prices(product_name):
    try:
        driver.get('https://www.realcanadiansuperstore.ca/')
        print('Opened the Superstore page.')

        search_box = driver.find_element(By.ID, 'search')
        search_box.send_keys(product_name)
        print(f'Entered "{product_name}" into the search box.')

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
        print(f"Error in get_superstore_prices: {e}")
        return []


def get_saveonfood_prices(product_name):
    try:
        driver.get('https://www.saveonfoods.com/sm/pickup/rsid/1982/')
        print('Opened the Save On Food page.')

        search_box = driver.find_element(By.ID, 'header-search-input')
        search_box.send_keys(product_name)
        print(f'Entered "{product_name}" into the search box.')

        search_button = driver.find_element(By.XPATH, '//button[@class="header-search-submit"]')
        search_button.click()
        print('Clicked the search button.')

        wait = WebDriverWait(driver, 10)
        # Wait for the search to load dynamically
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'product')))
        print('Waited for search results to load dynamically.')

        products = driver.find_elements(By.CLASS_NAME, 'product')
        product_prices = []

        for product in products:
            product_name = product.find_element(By.CLASS_NAME, 'product__name').text
            product_price = product.find_element(By.CLASS_NAME, 'price').text
            product_prices.append({'product': product_name, 'price': product_price})

        return product_prices
    except Exception as e:
        print(f"Error in get_saveonfood_prices: {e}")
        return []


# tried to use input stores, but it's harder so leave it now.
# def search_product_in_store(store_url, product_name):
#     try:
#         # Initialize WebDriver
#         driver = webdriver.Chrome()  # You can change this to whatever browser you prefer
#         driver.get(store_url)
#         print(f'Opened the {store_url} page.')

#         search_box = driver.find_element(By.NAME, 'q')  # Adjust this according to the store's search box name or locator
#         search_box.send_keys(product_name)
#         print(f'Entered "{product_name}" into the search box.')

#         search_box.submit()
#         print('Submitted the search query.')

#         wait = WebDriverWait(driver, 10)
#         # Wait for the search to load dynamically
#         wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.product-price > span.visuallyhidden')))
#         print('Waited for search results to load dynamically.')

#         products = driver.find_elements(By.CSS_SELECTOR, 'div.product-title-link a')
#         prices = driver.find_elements(By.CSS_SELECTOR, 'div.product-price > span.visuallyhidden')

#         product_prices = []
#         for product, price in zip(products, prices):
#             product_prices.append({'product': product.text, 'price': price.text})

#         return product_prices
#     except Exception as e:
#         print(f"Error in search_product_in_store: {e}")
#         return []

product_input = input("Enter the product that you want to compare the price: ")
walmart_prices = get_walmart_prices(product_input)
superstore_prices = get_superstore_prices(product_input)
saveonfood_prices = get_saveonfood_prices(product_input)


def save_to_csv(products_prices, product_name):
    try:
        timestamp = time.strftime('%Y%m%d%H%M%S')
        filename = f'{product_name}_prices_{timestamp}.csv'
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Product', 'Price'])
            for item in products_prices:
                writer.writerow([item['product'], item['price']])
        print(f'Saved data to CSV file: {filename}')
    except Exception as e:
        print(f"Error in save_to_csv: {e}")


class TestProductScraper(unittest.TestCase):
    def test_get_walmart_prices(self):
        product_name = "test product"
        product_prices = get_walmart_prices(product_name)
        self.assertIsInstance(product_prices, list)
        self.assertTrue(
            all(isinstance(item, dict) and 'product' in item and 'price' in item for item in product_prices))
        print('Test for get_walmart_prices passed.')

    def test_get_superstore_prices(self):
        product_name = "test product"
        product_prices = get_superstore_prices(product_name)
        self.assertIsInstance(product_prices, list)
        self.assertTrue(
            all(isinstance(item, dict) and 'product' in item and 'price' in item for item in product_prices))
        print('Test for get_superstore_prices passed.')

    def test_get_saveonfood_prices(self):
        product_name = "test product"
        product_prices = get_saveonfood_prices(product_name)
        self.assertIsInstance(product_prices, list)
        self.assertTrue(
            all(isinstance(item, dict) and 'product' in item and 'price' in item for item in product_prices))
        print('Test for get_saveonfood_prices passed.')

    def test_save_to_csv(self):
        test_product = "test product"
        test_data = [{'product': f'{test_product} 1', 'price': '$2.99'},
                     {'product': f'{test_product} 2', 'price': '$3.49'}]
        save_to_csv(test_data, test_product)
    

    import os
    self.assertTrue(os.path.isfile(f'{test_product}_prices.csv'))
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
