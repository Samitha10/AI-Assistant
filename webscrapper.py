import os
import csv
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import NoSuchElementException, TimeoutException
# selenium 
# webdriver-manager
def get_data(website: str):
    # Create a directory to save the images
    if not os.path.exists('product_images'):
        os.makedirs('product_images')

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Open the webpage
    url = website
    driver.get(url)

    # Extract product names and prices
    product_elements = driver.find_elements(By.CLASS_NAME, 'product')

    product_data = []

    for product in product_elements:
        name = product.find_element(By.CLASS_NAME, 'woocommerce-loop-product__title').text

        # Initialize price and handle exception if not found
        try:
            price = product.find_element(By.CLASS_NAME, 'price').text
        except NoSuchElementException:
            price = None

        category = product.find_element(By.CLASS_NAME, 'woocommerce-loop-product__category').text
        
        # Initialize image names
        img_primary_name = None
        img_secondary_name = None
        
        # Extract image URLs with exception handling
        try:
            img_primary_url = product.find_element(By.CLASS_NAME, 'img-primary').get_attribute('src')
            img_primary_name = f'{name}_primary.jpg'
            img_primary_path = os.path.join('product_images', img_primary_name)
            with open(img_primary_path, 'wb') as file:
                file.write(requests.get(img_primary_url).content)
        except NoSuchElementException:
            print(f"Primary image not found for product {name}")

        try:
            img_secondary_url = product.find_element(By.CLASS_NAME, 'img-secondary').get_attribute('src')
            img_secondary_name = f'{name}_secondary.jpg'
            img_secondary_path = os.path.join('product_images', img_secondary_name)
            with open(img_secondary_path, 'wb') as file:
                file.write(requests.get(img_secondary_url).content)
        except NoSuchElementException:
            print(f"Secondary image not found for product {name}")
        
        # Click the "Read more" button to go to the product description page
        read_more_button = product.find_element(By.TAG_NAME, 'a')
        read_more_button.send_keys(Keys.CONTROL + Keys.RETURN)  # Open in a new tab
        
        # Switch to the new tab
        driver.switch_to.window(driver.window_handles[1])
        
        # Get the current URL of the page
        current_url = driver.current_url

        # Initialize description and availability
        description = None
        availability = None
        
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'summary'))
            )
            description_element = driver.find_element(By.CLASS_NAME, 'woocommerce-product-details__short-description')
            description = description_element.text if description_element else "Description not available"
        except (NoSuchElementException, TimeoutException):
            print(f"Description not found or timed out for product {name}")
            description = "Description not available"
        
        # Extract availability information
        try:
            availability_element = driver.find_element(By.CSS_SELECTOR, 'p.stock.in-stock')
            availability = availability_element.text
        except NoSuchElementException:
            try:
                availability_element = driver.find_element(By.CSS_SELECTOR, 'p.stock.out-of-stock')
                availability = availability_element.text
            except NoSuchElementException:
                print(f"Availability information not found for product {name}")
                availability = "Availability not available"
        
        
        # Store the product data
        product_data.append({
            'name': name,
            'price': price,
            'category': category,
            'description': description,
            'availability': availability,
            'img_primary': img_primary_name,
            'img_secondary': img_secondary_name,
            'product_url': current_url
        })
        
        # Close the new tab and switch back to the main page
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        print(f"Product {name} saved.")
        
        # Wait a bit before moving on to the next product
        time.sleep(2)

    # Close the WebDriver
    driver.quit()

    # Define the CSV file name
    csv_file = 'product_details.csv'

    # Check if the CSV file already exists
    file_exists = os.path.isfile(csv_file)

    # Open the CSV file in append mode
    with open(csv_file, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write the header only if the file does not exist
        if not file_exists:
            writer.writerow(['name', 'price', 'category', 'description', 'availability', 'img_primary', 'img_secondary', 'product_url'])
        
        # Write the product data to the CSV file
        for product in product_data:
            writer.writerow([product['name'], product['price'], product['category'], product['description'], product['availability'], product['img_primary'], product['img_secondary'], product['product_url']])

# # Example usage
# get_data('https://store.spaceylon.com/product-category/baby-care/')

# get_data('https://store.spaceylon.com/product-category/skin-wellness/')
# get_data('https://store.spaceylon.com/product-category/skin-wellness/page/2/')
# get_data('https://store.spaceylon.com/product-category/skin-wellness/page/3/')
# get_data('https://store.spaceylon.com/product-category/skin-wellness/page/4/')
# get_data('https://store.spaceylon.com/product-category/skin-wellness/page/5/')
# get_data('https://store.spaceylon.com/product-category/skin-wellness/page/6/')

# get_data('https://store.spaceylon.com/product-category/mind-body/')
# get_data('https://store.spaceylon.com/product-category/mind-body/page/2/')
# get_data('https://store.spaceylon.com/product-category/mind-body/page/3/')
get_data('https://store.spaceylon.com/product-category/mind-body/page/4/')
get_data('https://store.spaceylon.com/product-category/mind-body/page/5/')
get_data('https://store.spaceylon.com/product-category/mind-body/page/6/')
get_data('https://store.spaceylon.com/product-category/mind-body/page/7/')
get_data('https://store.spaceylon.com/product-category/mind-body/page/8/')
get_data('https://store.spaceylon.com/product-category/mind-body/page/9/')
get_data('https://store.spaceylon.com/product-category/mind-body/page/10/')
get_data('https://store.spaceylon.com/product-category/mind-body/page/11/')
get_data('https://store.spaceylon.com/product-category/mind-body/page/12/')
get_data('https://store.spaceylon.com/product-category/mind-body/page/13/')
get_data('https://store.spaceylon.com/product-category/mind-body/page/14/')
get_data('https://store.spaceylon.com/product-category/mind-body/page/15/')
get_data('https://store.spaceylon.com/product-category/mind-body/page/16/')


get_data('https://store.spaceylon.com/product-category/hair-wellness/')
get_data('https://store.spaceylon.com/product-category/hair-wellness/page/2/')
get_data('https://store.spaceylon.com/product-category/hair-wellness/page/3/')
get_data('https://store.spaceylon.com/product-category/hair-wellness/page/4/')
get_data('https://store.spaceylon.com/product-category/hair-wellness/page/5/')


get_data('https://store.spaceylon.com/product-category/home-wellness/')
get_data('https://store.spaceylon.com/product-category/home-wellness/page/2/')
get_data('https://store.spaceylon.com/product-category/home-wellness/page/3/')

get_data('https://store.spaceylon.com/product-category/fragrances/')
get_data('https://store.spaceylon.com/product-category/fragrances/page/2/')
get_data('https://store.spaceylon.com/product-category/fragrances/page/3/')
get_data('https://store.spaceylon.com/product-category/fragrances/page/4/')

get_data('https://store.spaceylon.com/product-category/more/')
get_data('https://store.spaceylon.com/product-category/more/page/2/')