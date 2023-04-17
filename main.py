from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from time import sleep


zip_code = input("Please enter zip code you would like to search for: ")

options = webdriver.ChromeOptions()
# options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

driver.get("https://www.bmwusa.com/inventory/zip")

# EDGE CASE: if there is only one dealership, then it will not ask you to select one
zip_input = driver.find_element(By.ID, "zipentry-input")
zip_input.clear()
zip_input.send_keys(zip_code)
zip_input.send_keys(Keys.ENTER)
driver.implicitly_wait(2)
# Try/except handles edge case where if there is only one dealer in a zipcode
# then they are automatically selected
try:
    select_dealer_btn = driver.find_element(By.CLASS_NAME, "dealerlist-dealerselectbutton")
    if select_dealer_btn is not None:
        select_dealer_btn.click()
except NoSuchElementException as err:
    print(f"NoSuchElementException: {err}")
    pass
driver.implicitly_wait(3)
set_range_dropdown = driver.find_element(By.CLASS_NAME, "nav-results-page_label_3G3MB")
set_range_dropdown.click()
select_range_options = driver.find_elements(By.CLASS_NAME, "location-select_rangebutton_2c4VW")
hundred_mile_range_option = select_range_options[3]
hundred_mile_range_option.click()
select_update_range_btn = driver.find_element(By.CLASS_NAME, "location-select_button_39oXs")
select_update_range_btn.click()
driver.implicitly_wait(3)
# https://www.bmwusa.com/inventory/results?Series=3&InteriorColor=Black&Option=S07M9&ExteriorColor=Black&FuelType=X
# This finds a black 330e with the shadowline package
driver.get("https://www.bmwusa.com/inventory/results?Series=3&Option=S07M9&ExteriorColor=Black&FuelType=X")
# Let's grab all the hrefs that have the form /inventory/#/detail/VIN_NUMBER_HERE
car_anchors = driver.find_elements(By.CLASS_NAME, "new-vehicle-card_detailbutton_wYsVN")
car_hrefs = []
for anchor in car_anchors:
    href = anchor.get_attribute("href")
    car_hrefs.append(href)
if len(car_hrefs) < 1:
    print(f"Unfortunately, no cars found within 100 miles of {zip_code}")
    exit()
print(f"Printing car links:\n {car_hrefs}")
sleep(3)
# This just opens up the tabs to demo
# for href in car_hrefs:
#     driver.switch_to.new_window('tab')
#     driver.get(href)
#     sleep(6)
sleep(10)
driver.quit()
