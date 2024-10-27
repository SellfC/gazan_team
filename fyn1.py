# func.py
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def page_down(driver, timeout=10): # Added timeout parameter
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(50, document.body.scrollHeight);")

        try: # Wait for new elements to load after scrolling
            WebDriverWait(driver, timeout).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'tile-hover-target'))  # Or another suitable selector
            )
            # Or wait for the page height to change:
            # WebDriverWait(driver, timeout).until(lambda driver: driver.execute_script("return document.body.scrollHeight;") > last_height)

        except Exception as e: # Timeout or other exception
            print(f"Error waiting for elements after scroll: {e}")
            break # Stop scrolling if elements don't load

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height




        