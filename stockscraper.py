from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Chrome driver setup
chrome_driver_path = r"C:\Users\HP user\Downloads\chrome_Driver\chromedriver-win64\chromedriver.exe"
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

# Website open and set up for scraping
driver.get("https://stockanalysis.com/stocks/screener/")
driver.maximize_window() # maximize window for visibility
wait = WebDriverWait(driver, 3) # allow elements to load

# Open the dropdown stock indicators list
indicators_dropdown = wait.until(
    EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[1]/div[2]/main/div[3]/div[1]/div/div[3]/button"))
) # Use XPATH from element HTML
indicators_dropdown.click()

# Choose all stock indicators
time.sleep(1)
checkboxes_container = driver.find_element(By.XPATH, "/html/body/div/div[1]/div[2]/main/div[3]/div[1]/div/div[3]/div/div[2]")
checkboxes = checkboxes_container.find_elements(By.XPATH, ".//input[@type='checkbox']")

# Loop through and select every checkbox
for checkbox in checkboxes:
    if not checkbox.is_selected():
        driver.execute_script("arguments[0].click();", checkbox)
        time.sleep(0.5)

print("All indicators have been selected")
time.sleep(2)

# Scraping webpage data
all_stocks = []
page_number = 1

while True:
    print(f"Scraping page {page_number}")

    try:
        # Find all rows of stocks
        stock_rows = driver.find_elements(By.XPATH, "//table/tbody/tr")

        for row in stock_rows:
            columns = row.find_elements(By.TAG_NAME, "td")
            if len(columns) > 1:
                stock_data = [col.text for col in columns]
                all_stocks.append(stock_data)

        
        # Make sure that all elements are visible
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(2)

        # Click the Next button
        next_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[1]/div[2]/main/div[3]/nav[2]/button[2]"))
        )

        if "disabled" in next_button.get_attribute("class"):
            print(f"Reached the last page ({page_number}). Ending")
            break

        driver.execute_script("arguments[0].click();", next_button)

        page_number += 1
        time.sleep(2)


    except Exception as e:
        print(f"No next button was found, stopped at page {page_number} or error {e} occured")
        break

# Save everything to CSV file
df = pd.DataFrame(all_stocks)
df.to_csv("stocks.csv", index=False, header=False)
print(f"{page_number} pages scraped. Data saved to stocks.csv")

# Close browser
driver.quit()
