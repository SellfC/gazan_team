import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from fyn1 import page_down
from selenium.webdriver.chrome.options import Options
from openpyxl import Workbook
from selenium.common.exceptions import NoSuchElementException

# --- Speed Optimization: Headless Mode ---
options = Options()
options.binary_location = r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
# options.add_argument("headless")  # Uncomment for headless mode if needed


def get_products_links(driver, item_name='шуруповёрт'):
    products_urls = []
    page_num = 1
    while True:
        print(f"Scraping page {page_num}")
        driver.get(
            url=f'https://www.ozon.ru/category/instrumenty-dlya-remonta-i-stroitelstva-9856/?deny_category_prediction=true&from_global=true&opened=brand&page={page_num}&text={item_name}')
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'tile-hover-target'))
            )
        except Exception as e:
            print(f"Error waiting for tile-hover-target: {e}")
            break

        finde_links = driver.find_elements(By.CLASS_NAME, 'tile-hover-target')
        print(f"Found {len(finde_links)} links on page {page_num}")
        products_urls.extend([link.get_attribute("href") for link in finde_links])

        try:
            next_page_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Следующая')]")
            print("Clicking 'Next' button")
            next_page_button.click()
            WebDriverWait(driver, 10).until(EC.staleness_of(next_page_button))
            page_num += 1
        except NoSuchElementException:
            print("No 'Next' button found. Last page reached.")
            break

    print(f"Total links collected: {len(products_urls)}")
    return products_urls

def parse_product_data(driver, url):
    print(f"Parsing product page: {url}")
    driver.get(url)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h1.tm6_27.tsHeadline550Medium')))
    except Exception as e:
        print(f"Error waiting for product title: {e}")
        return {'name': "N/A", 'green_price': "N/A", 'price': "N/A", 'url': url}

    try:
        name = driver.find_element(By.CSS_SELECTOR, 'h1.tm6_27.tsHeadline550Medium').text
        print(f"Product name: {name}")

        try:
            green_price = driver.find_element(By.CLASS_NAME, 's5m_27.ms4_27').text.replace('₽', '')
            print(f"Green price: {green_price}")
        except NoSuchElementException:
            green_price = "N/A"

        try:
            price = driver.find_element(By.CLASS_NAME, 'mt0_27.m0t_27.mt4_27').text.replace('₽', '')
            print(f"Price: {price}")
        except NoSuchElementException:
            price = "N/A"

    except Exception as e:
        print(f"Error parsing product page: {e}")
        return {'name': "N/A", 'green_price': "N/A", 'price': "N/A", 'url': url}

    return {'name': name, 'green_price': green_price, 'price': price, 'url': url}



with uc.Chrome(options=options) as driver:
    links = get_products_links(driver, 'шуруповёрт')

    products_data = []
    processed_urls = set()
    for i, link in enumerate(links):
        if link not in processed_urls:
            print(f"Processing link {i+1} of {len(links)}: {link}") # More debugging
            product_data = parse_product_data(driver, link)
            products_data.append(product_data)
            processed_urls.add(link)

    wb = Workbook()
    ws = wb.active
    ws.append(['Name', 'Green Price', 'Price', 'URL'])

    for product in products_data:
        ws.append([product['name'], product['green_price'],
                  product['price'], product['url']])

    wb.save('products_data.xlsx')