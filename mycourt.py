import chromedriver_autoinstaller
chromedriver_autoinstaller.install()

from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import date, timedelta, datetime
import pause
import time
import sys
from keys import email, password

web = webdriver.Chrome()

email = email
password = password
day_of_week = 5
booking_time = "16.00-17.00"
booking_offset_in_days = 30

def main():
    date_at_offset = (date.today()+timedelta(days=booking_offset_in_days))
    date_at_offset_str = date_at_offset.strftime("%d-%m-%Y")

    if date_at_offset.isoweekday() == day_of_week:
        login()

        pause_to = datetime.now().replace(hour=int(booking_time.split(".")[0]), minute=0, second=0, microsecond=0)
        print("Pausing until " + str(pause_to))
        pause.until(pause_to)
        
        print("it's booking time!")
        book(date_at_offset_str)
    else:
        print("It's not booking time. Incorrect weekday " + date_at_offset_str)
        sys.exit(0)

def login():
    web.get("https://www.mycourt.se/login_form.php")

    time.sleep(1)

    web.find_element(by=By.ID, value="email").send_keys(email)
    web.find_element(by=By.ID, value="password").send_keys(password)
    web.execute_script("arguments[0].click();", web.find_element(By.XPATH, value="//input[contains(@class,'form-control') and @name='agree_terms_conditions']"))
    loginButton = web.find_element(By.XPATH, value="//button[contains(text(),'Logga in')]")
    loginButton.click()

    time.sleep(2)

def book(date_at_offset):
    for _ in range(2):
        web.execute_script ("""
        let form = document.createElement("form");
        form.setAttribute("method", "post");
        form.setAttribute("action", "/table_cust.php?room_id=896393");
        
        let dateInput = document.createElement("input");
        dateInput.setAttribute("type", "text");
        dateInput.setAttribute("name", "today_cal");
        dateInput.setAttribute("value", "{date_at_offset}");
        form.appendChild(dateInput);

        let modeInput = document.createElement("input");
        modeInput.setAttribute("type", "text");
        modeInput.setAttribute("name", "mode");
        modeInput.setAttribute("value", "cal_clicked");
        form.appendChild(modeInput);

        document.body.appendChild(form);

        form.submit(); 
        """.format(date_at_offset=date_at_offset))
        time.sleep(2)

    tdElement = web.find_element(By.XPATH, value="//td[@court_time='{booking_time}']".format(booking_time=booking_time))
    tdElement.click()

    time.sleep(2)

    terms_and_conditions = web.find_element(by=By.XPATH, value="//input[@id='requre_terms_and_conditions']")

    if not terms_and_conditions.is_selected():
        web.execute_script("arguments[0].click();", terms_and_conditions)

    time.sleep(1)

    bookButton = web.find_element(By.XPATH, value="//input[@value='Boka och fortsätt']")
    bookButton.click()
    
if __name__ == "__main__":
    main()

    time.sleep(900)