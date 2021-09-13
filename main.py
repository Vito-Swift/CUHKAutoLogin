from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import requests
import time

# the url used for check internet connectivity
beacon_url = "https://www.github.com"
# timeout of accessing internet
beacon_timeout = 5
# set the interval between two probes (default to be 60 seconds)
check_interval = 60

# TODO: please fill-in your credential HERE
username = "YOUR_CUHK_EMAIL"
passwd = "YOUR_CUHK_ONEPASS"

# Use this url to login secure wlan
login_url = "https://securelogin.wlan.cuhk.edu.hk/"


def login_secure_wlan():
    browser = webdriver.Firefox(executable_path="/home/vitowu/CLionProjects/pythonProject/geckodriver")
    browser.get(login_url)
    delay = 10

    # Get into welcome.html page
    try:
        WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'login')))
        WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'checkbox')))
        print("got into the welcome.html page")
    except TimeoutException:
        print("take too much time getting into the welcome page")
        yield
    browser.find_element_by_class_name('checkbox').click()
    browser.find_element_by_id('login').click()

    # Get into login.html page
    try:
        WebDriverWait(browser, delay).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/form/input[1]')))
        WebDriverWait(browser, delay).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/form/input[2]')))
        WebDriverWait(browser, delay).until(
            EC.presence_of_element_located((By.ID, 'login')))
        print("got into the login.html page")
    except TimeoutException:
        print("take too much time getting into the login page")
        exit(0)
    browser.find_element_by_xpath('/html/body/div[1]/div/form/input[1]').send_keys(username)
    browser.find_element_by_xpath('/html/body/div[1]/div/form/input[2]').send_keys(passwd)
    browser.find_element_by_id('login').click()


def main():
    while True:
        try:
            print("Start probe internet connection")
            internet_connected = True
            try:
                request = requests.get(beacon_url, timeout=beacon_timeout)
                print("Probe result: connected to Internet")
            except (requests.ConnectionError, requests.Timeout) as exception:
                print("Probe result: no Internet connection")
                internet_connected = False

            if not internet_connected:
                print("Try login secure wlan...")
                login_secure_wlan()
                time.sleep(1)
                continue

            print("Transit to inactivate mode, next probe is scheduled in {} seconds...".format(check_interval))
            time.sleep(check_interval)
        except KeyboardInterrupt:
            print("Catch Ctrl+C, exit")
            exit(0)


if __name__ == '__main__':
    main()
