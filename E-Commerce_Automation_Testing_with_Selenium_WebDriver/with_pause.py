import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
time.sleep(1)

# block common ad websites
driver.execute_cdp_cmd("Network.enable", {})
time.sleep(1)

driver.execute_cdp_cmd("Network.setBlockedURLs", {
    "urls": [
        "*doubleclick.net/*",
        "*googlesyndication.com/*",
        "*googleadservices.com/*",
        "*adservice.google.com/*",
        "*googleads.g.doubleclick.net/*"
    ]
})
time.sleep(1)

# Navigate to the website
driver.get("https://www.demoblaze.com/")
time.sleep(1)

wait = WebDriverWait(driver, 10)
time.sleep(1)

# Wait until Products link appears on the page
wait.until(
    EC.element_to_be_clickable((By.LINK_TEXT, "Sign up"))
)
time.sleep(1)

print("Home page loaded successfully")
time.sleep(1)

#Postive test case 1: Sign up with valid credentials
driver.find_element(By.LINK_TEXT, "Sign up").click()
time.sleep(1)

wait.until(
    EC.visibility_of_element_located((By.ID, "sign-username"))
)
time.sleep(1)

driver.find_element(By.ID, "sign-username").send_keys("testuser12345678@8888899665547")
time.sleep(1)

driver.find_element(By.ID, "sign-password").send_keys("Test@1234")
time.sleep(1)

driver.find_element(By.XPATH, "//button[text()='Sign up']").click()
time.sleep(1)

wait.until(EC.alert_is_present())
time.sleep(1)

alert = driver.switch_to.alert
time.sleep(1)

print("Alert message:", alert.text)
time.sleep(1)

alert.accept()
time.sleep(1)

wait.until(
    EC.invisibility_of_element_located((By.ID, "signInModal"))
)
time.sleep(1)

# Positive test case 2: Log in with valid credentials
login_link = wait.until(
    EC.element_to_be_clickable((By.LINK_TEXT, "Log in"))
)
time.sleep(1)

login_link.click()
time.sleep(1)

wait.until(
    EC.visibility_of_element_located((By.ID, "loginusername"))
)
time.sleep(1)

driver.find_element(By.ID, "loginusername").send_keys("testuser12345678@888889966")
time.sleep(1)

driver.find_element(By.ID, "loginpassword").send_keys("Test@1234")
time.sleep(1)

driver.find_element(By.XPATH, "//button[text()='Log in']").click()
time.sleep(1)

wait.until(
    EC.visibility_of_element_located((By.ID, "nameofuser"))
)
time.sleep(1)

print("Login successful, user:", driver.find_element(By.ID, "nameofuser").text)
time.sleep(1)

# Postive test case 3: Add product to cart
product_link = wait.until(
    EC.element_to_be_clickable((By.LINK_TEXT, "Laptops"))
)
time.sleep(1)

product_link.click()
time.sleep(1)

wait.until(
    EC.element_to_be_clickable((By.LINK_TEXT, "Sony vaio i5"))
)
time.sleep(1)

driver.find_element(By.LINK_TEXT, "Sony vaio i5").click()
time.sleep(1)

wait.until(
    EC.element_to_be_clickable((By.XPATH, "//a[text()='Add to cart']"))
)
time.sleep(1)

driver.find_element(By.XPATH, "//a[text()='Add to cart']").click()
time.sleep(1)

wait.until(EC.alert_is_present())
time.sleep(1)

alert = driver.switch_to.alert
time.sleep(1)

print("Alert message:", alert.text)
time.sleep(1)

alert.accept()
time.sleep(1)

#positive test case 4: view cart and place order
cart_link = wait.until(
    EC.element_to_be_clickable((By.ID, "cartur"))
)
time.sleep(1)

cart_link.click()
time.sleep(1)

wait.until(
    EC.visibility_of_element_located((By.XPATH, "//td[text()='Sony vaio i5']"))
)
time.sleep(1)

print("Product added to cart successfully")
time.sleep(1)

driver.find_element(By.XPATH, "//button[text()='Place Order']").click()
time.sleep(1)

wait.until(
    EC.visibility_of_element_located((By.ID, "name"))
)
time.sleep(1)

driver.find_element(By.ID, "name").send_keys("Test User")
time.sleep(1)

driver.find_element(By.ID, "country").send_keys("Test Country")
time.sleep(1)

driver.find_element(By.ID, "city").send_keys("Test City")
time.sleep(1)

driver.find_element(By.ID, "card").send_keys("1234 5678 9012 3456")
time.sleep(1)

driver.find_element(By.ID, "month").send_keys("12")
time.sleep(1)

driver.find_element(By.ID, "year").send_keys("2025")
time.sleep(1)

driver.find_element(By.XPATH, "//button[text()='Purchase']").click()
time.sleep(1)

wait.until(
    EC.visibility_of_element_located((By.XPATH, "//h2[text()='Thank you for your purchase!']"))
)
time.sleep(1)

time.sleep(2)
time.sleep(1)

 # Wait for the confirmation dialog to appear
confirm_btn = wait.until(
    EC.element_to_be_clickable((By.CLASS_NAME, "confirm"))
)
time.sleep(1)

confirm_btn.click()
time.sleep(1)

print("Order placed successfully")
time.sleep(1)

# validate test case 1: Go to cart again without adding any product and try to place order
cart_link = wait.until(
    EC.element_to_be_clickable((By.ID, "cartur"))
)
time.sleep(1)

cart_link.click()
time.sleep(1)

place_order_btn = wait.until(
    EC.visibility_of_element_located((By.XPATH, "//button[text()='Place Order']"))
)
time.sleep(1)

place_order_btn.click()
time.sleep(1)

wait.until(
    EC.visibility_of_element_located((By.ID, "name"))
)
time.sleep(1)

driver.find_element(By.ID, "name").send_keys("Test User")
time.sleep(1)

driver.find_element(By.ID, "country").send_keys("Test Country")
time.sleep(1)

driver.find_element(By.ID, "city").send_keys("Test City")
time.sleep(1)

driver.find_element(By.ID, "card").send_keys("1234 5678 9012 3456")
time.sleep(1)

driver.find_element(By.ID, "month").send_keys("12")
time.sleep(1)

driver.find_element(By.ID, "year").send_keys("2025")
time.sleep(1)

driver.find_element(By.XPATH, "//button[text()='Purchase']").click()
time.sleep(1)

wait.until(
    EC.visibility_of_element_located((By.XPATH, "//h2[text()='Thank you for your purchase!']"))
)
time.sleep(1)

time.sleep(2)
time.sleep(1)

confirm_btn = wait.until(
    EC.element_to_be_clickable((By.CLASS_NAME, "confirm"))
)
time.sleep(1)

confirm_btn.click()
time.sleep(1)

print("Order placed successfully without adding product to cart, which is a bug")
time.sleep(1)

# Navigate test case 1: Log out
logout_link = wait.until(
    EC.element_to_be_clickable((By.ID, "logout2"))
)
time.sleep(1)

logout_link.click()
time.sleep(1)

wait.until(
    EC.element_to_be_clickable((By.LINK_TEXT, "Log in"))
)
time.sleep(1)

# Negative test case 1 : Log in with invaild username
login_link = wait.until(
    EC.element_to_be_clickable((By.LINK_TEXT, "Log in"))
)
time.sleep(1)

login_link.click()
time.sleep(1)

wait.until(
    EC.visibility_of_element_located((By.ID, "loginusername"))
)
time.sleep(1)

driver.find_element(By.ID, "loginusername").send_keys("invailduser33432545545545454545")
time.sleep(1)

driver.find_element(By.ID, "loginpassword").send_keys("Test@1234")
time.sleep(1)

driver.find_element(By.XPATH, "//button[text()='Log in']").click()
time.sleep(1)

wait.until(EC.alert_is_present())
time.sleep(1)

alert = driver.switch_to.alert
time.sleep(1)

print("Alert message:", alert.text)
time.sleep(1)

alert.accept()
time.sleep(1)

close_btn = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "//div[@id='logInModal']//button[normalize-space()='Close']")
    )
)
time.sleep(1)

close_btn.click()
time.sleep(1)

print("Login Failed")
time.sleep(1)

# Negative test case 2 : Sign up with already exit user
driver.find_element(By.LINK_TEXT, "Sign up").click()
time.sleep(1)

wait.until(
    EC.visibility_of_element_located((By.ID, "sign-username"))
)
time.sleep(1)

driver.find_element(By.ID, "sign-username").send_keys("testuser12345678@888889966")
time.sleep(1)

driver.find_element(By.ID, "sign-password").send_keys("Test@1234")
time.sleep(1)

driver.find_element(By.XPATH, "//button[text()='Sign up']").click()
time.sleep(1)

wait.until(EC.alert_is_present())
time.sleep(1)

alert = driver.switch_to.alert
time.sleep(1)

print("Alert message:", alert.text)
time.sleep(1)

alert.accept()
time.sleep(1)

close_btn = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "//div[@id='signInModal']//button[normalize-space()='Close']")
    )
)
time.sleep(1)

close_btn.click()
time.sleep(1)

print("Sign up Failed")
time.sleep(1)

input("Press Enter to close the browser...")
driver.quit()