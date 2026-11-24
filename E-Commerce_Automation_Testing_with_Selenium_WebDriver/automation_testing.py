import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

# block common ad websites
driver.execute_cdp_cmd("Network.enable", {})
driver.execute_cdp_cmd("Network.setBlockedURLs", {
    "urls": [
        "*doubleclick.net/*",
        "*googlesyndication.com/*",
        "*googleadservices.com/*",
        "*adservice.google.com/*",
        "*googleads.g.doubleclick.net/*"
    ]
})

# Navigate to the website
driver.get("https://www.demoblaze.com/")

wait = WebDriverWait(driver, 10)

# Wait until Products link appears on the page
wait.until(
    EC.element_to_be_clickable((By.LINK_TEXT, "Sign up"))
)
print("Home page loaded successfully")

#Postive test case 1: Sign up with valid credentials
driver.find_element(By.LINK_TEXT, "Sign up").click()
wait.until(
    EC.visibility_of_element_located((By.ID, "sign-username"))
)
driver.find_element(By.ID, "sign-username").send_keys("testuser12345678@88888996657")
driver.find_element(By.ID, "sign-password").send_keys("Test@1234")
driver.find_element(By.XPATH, "//button[text()='Sign up']").click()
wait.until(EC.alert_is_present())
alert = driver.switch_to.alert
print("Alert message:", alert.text)
alert.accept()
wait.until(
    EC.invisibility_of_element_located((By.ID, "signInModal"))
)

# Positive test case 2: Log in with valid credentials
login_link = wait.until(
    EC.element_to_be_clickable((By.LINK_TEXT, "Log in"))
)
login_link.click()
wait.until(
    EC.visibility_of_element_located((By.ID, "loginusername"))
)
driver.find_element(By.ID, "loginusername").send_keys("testuser12345678@888889966")
driver.find_element(By.ID, "loginpassword").send_keys("Test@1234")
driver.find_element(By.XPATH, "//button[text()='Log in']").click()
wait.until(
    EC.visibility_of_element_located((By.ID, "nameofuser"))
)
print("Login successful, user:", driver.find_element(By.ID, "nameofuser").text) 

# Postive test case 3: Add product to cart
product_link = wait.until(
    EC.element_to_be_clickable((By.LINK_TEXT, "Laptops"))
)
product_link.click()
wait.until(
    EC.element_to_be_clickable((By.LINK_TEXT, "Sony vaio i5"))
)
driver.find_element(By.LINK_TEXT, "Sony vaio i5").click()
wait.until(
    EC.element_to_be_clickable((By.XPATH, "//a[text()='Add to cart']"))
)
driver.find_element(By.XPATH, "//a[text()='Add to cart']").click()
wait.until(EC.alert_is_present())
alert = driver.switch_to.alert
print("Alert message:", alert.text)
alert.accept() 

#positive test case 4: view cart and place order
cart_link = wait.until(
    EC.element_to_be_clickable((By.ID, "cartur"))
)
cart_link.click()
wait.until(
    EC.visibility_of_element_located((By.XPATH, "//td[text()='Sony vaio i5']"))
)
print("Product added to cart successfully")
driver.find_element(By.XPATH, "//button[text()='Place Order']").click()
wait.until(
    EC.visibility_of_element_located((By.ID, "name"))
)
driver.find_element(By.ID, "name").send_keys("Test User")
driver.find_element(By.ID, "country").send_keys("Test Country")
driver.find_element(By.ID, "city").send_keys("Test City")
driver.find_element(By.ID, "card").send_keys("1234 5678 9012 3456")
driver.find_element(By.ID, "month").send_keys("12")
driver.find_element(By.ID, "year").send_keys("2025")
driver.find_element(By.XPATH, "//button[text()='Purchase']").click()
wait.until(
    EC.visibility_of_element_located((By.XPATH, "//h2[text()='Thank you for your purchase!']"))
)
time.sleep(2) 
 # Wait for the confirmation dialog to appear
confirm_btn = wait.until(
    EC.element_to_be_clickable((By.CLASS_NAME, "confirm"))
)
confirm_btn.click()
print("Order placed successfully")

# validate test case 1: Go to cart again without adding any product and try to place order
cart_link = wait.until(
    EC.element_to_be_clickable((By.ID, "cartur"))
)
cart_link.click()
place_order_btn = wait.until(
    EC.visibility_of_element_located((By.XPATH, "//button[text()='Place Order']"))
)
place_order_btn.click()
wait.until(
    EC.visibility_of_element_located((By.ID, "name"))
)
driver.find_element(By.ID, "name").send_keys("Test User")
driver.find_element(By.ID, "country").send_keys("Test Country")
driver.find_element(By.ID, "city").send_keys("Test City")
driver.find_element(By.ID, "card").send_keys("1234 5678 9012 3456")
driver.find_element(By.ID, "month").send_keys("12")
driver.find_element(By.ID, "year").send_keys("2025")
driver.find_element(By.XPATH, "//button[text()='Purchase']").click()
wait.until(
    EC.visibility_of_element_located((By.XPATH, "//h2[text()='Thank you for your purchase!']"))
)
time.sleep(2) 
confirm_btn = wait.until(
    EC.element_to_be_clickable((By.CLASS_NAME, "confirm"))
)
confirm_btn.click()
print("Order placed successfully without adding product to cart, which is a bug")

# Navigate test case 1: Log out
logout_link = wait.until(
    EC.element_to_be_clickable((By.ID, "logout2"))
)
logout_link.click()
wait.until(
    EC.element_to_be_clickable((By.LINK_TEXT, "Log in"))
)

# Negative test case 1 : Log in with invaild username
login_link = wait.until(
    EC.element_to_be_clickable((By.LINK_TEXT, "Log in"))
)
login_link.click()

wait.until(
    EC.visibility_of_element_located((By.ID, "loginusername"))
)
driver.find_element(By.ID, "loginusername").send_keys("invailduser33432545545545454545")
driver.find_element(By.ID, "loginpassword").send_keys("Test@1234")
driver.find_element(By.XPATH, "//button[text()='Log in']").click()
wait.until(EC.alert_is_present())
alert = driver.switch_to.alert
print("Alert message:", alert.text)
alert.accept()
close_btn = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "//div[@id='logInModal']//button[normalize-space()='Close']")
    )
)
close_btn.click()
print("Login Failed") 

# Negative test case 2 : Sign up with already exit user
driver.find_element(By.LINK_TEXT, "Sign up").click()
wait.until(
    EC.visibility_of_element_located((By.ID, "sign-username"))
)
driver.find_element(By.ID, "sign-username").send_keys("testuser12345678@888889966")
driver.find_element(By.ID, "sign-password").send_keys("Test@1234")
driver.find_element(By.XPATH, "//button[text()='Sign up']").click()
wait.until(EC.alert_is_present())
alert = driver.switch_to.alert
print("Alert message:", alert.text)
alert.accept()
close_btn = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "//div[@id='signInModal']//button[normalize-space()='Close']")
    )
)
close_btn.click()
print("Sign up Failed") 

input("Press Enter to close the browser...")
driver.quit()