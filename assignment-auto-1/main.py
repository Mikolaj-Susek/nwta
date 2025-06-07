from selenium.webdriver.common.by import By
import time
from decimal import Decimal, ROUND_HALF_UP
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager


def js_style_round(x, places=2):
    return float(Decimal(str(x)).quantize(Decimal('1.' + '0' * places), rounding=ROUND_HALF_UP))

driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))

driver.get("http://localhost:8080/")

# Wait for the page to load
time.sleep(1)

# List of operations and their corresponding button IDs
operations = {
    '+': 'add',
    '-': 'subtract',
    '*': 'multiply',
    '/': 'divide'
}

# Store incorrect results
found_exceptions = []

# Test all combinations from 0 to 9 with each operation
for a in range(10):
    for b in range(10):
        for symbol, button_id in operations.items():
            # Click the clear button (first button on the page)
            driver.find_element(By.TAG_NAME, "button").click()

            # Fill in the input fields
            input1 = driver.find_element(By.ID, "num1")
            input2 = driver.find_element(By.ID, "num2")
            input1.send_keys(str(a))
            time.sleep(0.1)
            input2.send_keys(str(b))
            time.sleep(0.1)

            # Click the operation button
            driver.find_element(By.ID, button_id).click()
            time.sleep(0.1)

            # Get the result text
            result = driver.find_element(By.ID, "result").text
            time.sleep(0.1)

            erase = driver.find_element(By.XPATH, "//button[text()='Erase']")
            erase.click()

            # Calculate the expected result
            try:
                if a < 0 or a > 9 or b < 0 or b > 9:
                    expected = "out of range"
                elif symbol == '/' and b == 0:
                    expected = "Error!"
                elif symbol == '/':
                    expected = f"{js_style_round(a / b):.2f}"
                elif symbol == '+':
                    expected = str(a + b)
                elif symbol == '-':
                    expected = str(a - b)
                elif symbol == '*':
                    expected = str(a * b)
            except:
                expected = "EXCEPTION"

            # Compare the result
            if result != expected:
                print(f"Mismatch: {a} {symbol} {b} = {result}, expected: {expected}")
                found_exceptions.append((a, symbol, b, result, expected))

            if len(found_exceptions) == 10:
                break
        if len(found_exceptions) == 10:
            break
    if len(found_exceptions) == 10:
        break

print("\nFound exceptions:")
for ex in found_exceptions:
    print(f"{ex[0]} {ex[1]} {ex[2]} = {ex[3]} (expected: {ex[4]})")

driver.quit()


