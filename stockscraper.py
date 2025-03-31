from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Set up ChromeDriver path
chrome_driver_path = r"C:\Users\HP user\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

# Open stock screener page
url = "https://stockanalysis.com/stocks/screener/"
driver.get(url)

# Maximize the window for better interaction
driver.maximize_window()

# ✅ **Explicitly wait for elements**
wait = WebDriverWait(driver, 10)

# ✅ **Open the 'Indicators' dropdown**
indicators_dropdown = wait.until(
    EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[1]/div[2]/main/div[3]/div[1]/div/div[3]/button"))
)
indicators_dropdown.click()

# ✅ **Find and select all checkboxes**
time.sleep(1)
checkboxes_container = driver.find_element(By.XPATH, "/html/body/div/div[1]/div[2]/main/div[3]/div[1]/div/div[3]/div/div[2]")

checkboxes = checkboxes_container.find_elements(By.XPATH, ".//input[@type='checkbox']")

for checkbox in checkboxes:
    if not checkbox.is_selected():
        driver.execute_script("arguments[0].click();", checkbox)
        time.sleep(0.5)

print("✅ All checkboxes selected.")
time.sleep(2)

# ✅ **Scraping and pagination**
all_stocks = []
page_number = 1

while True:
    print(f"📄 Scraping page {page_number}...")  # Debug message
    
    try:
        # Find all stock rows
        stock_rows = driver.find_elements(By.XPATH, "//table/tbody/tr")

        for row in stock_rows:
            columns = row.find_elements(By.TAG_NAME, "td")
            if len(columns) > 1:  # Ensure row has data
                stock_data = [col.text for col in columns]
                all_stocks.append(stock_data)
        
        # Use JavaScript to scroll down the page to ensure all elements are visible
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for the page to scroll and load content

        # Wait for the "Next" button to be visible and clickable
        next_button = WebDriverWait(driver, 3 ).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[1]/div[2]/main/div[3]/nav[2]/button[2]"))
        )

        # Check if the "Next" button is disabled
        if "disabled" in next_button.get_attribute("class"):  # Check if it's disabled
            print(f"❌ Reached last page ({page_number}). Stopping.")
            break
        
        # Use JavaScript to click the "Next" button directly
        driver.execute_script("arguments[0].click();", next_button)

        page_number += 1
        time.sleep(2)  # Allow time for new page to load
        
    except Exception as e:
        print(f"❌ No 'Next' button found on page {page_number} or an error occurred: {e}. Stopping.")
        break

# Save to CSV
df = pd.DataFrame(all_stocks)
df.to_csv("stocks.csv", index=False, header=False)
print(f"✅ Data saved to stocks.csv. Scraped {page_number} pages.")

# ✅ **Close browser**
driver.quit()
