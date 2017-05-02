import time
import moment
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def print_cekis():
    cekisElem = driver.find_element_by_class_name("cekis")

    flight1flightNumber = cekisElem.find_element_by_xpath('.//div[1]/div[1]/div[1]/div[2]')
    flight1departureTime = cekisElem.find_element_by_xpath('.//div[1]/div[1]/div[2]/div[2]')
    flight1arrivalTime = cekisElem.find_element_by_xpath('.//div[1]/div[1]/div[3]/div[2]')

    flight2flightNumber = cekisElem.find_element_by_xpath('.//div[1]/div[2]/div[1]/div[2]')
    flight2departureTime = cekisElem.find_element_by_xpath('.//div[1]/div[2]/div[2]/div[2]')
    flight2arrivalTime = cekisElem.find_element_by_xpath('.//div[1]/div[2]/div[3]/div[2]')

    # print "Flight 1 number: " + flight1flightNumber.text
    # print "Flight 1 departure time: " + flight1departureTime.text
    # print "Flight 1 arrival time: " + flight1arrivalTime.text

    # print "--------------"
    #
    # print "Flight 2 number: " + flight2flightNumber.text
    # print "Flight 2 departure time: " + flight2departureTime.text
    # print "Flight 2 arrival time: " + flight2arrivalTime.text
    # print "Total price: " + cekisElem.find_element_by_class_name("cr").text

    print "VNO -> FNC " + cekisElem.find_element_by_class_name(
        "cr").text + " " + flight1departureTime.text + " --> " + flight2departureTime.text

    print "--------------"


driver = webdriver.Chrome()

try:
    driver.maximize_window()
    driver.get("http://flights.novatours.eu/")
    print driver.find_element_by_name("departure").get_attribute("value")

    driver.find_element_by_id("arrival_input").click()
    WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.ID, "FNC"))
    )
    driver.find_element_by_id("FNC").click()

    driver.find_element_by_id("departure_date_shadow").click()

    WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".departure-calendar .calendar"))
    )

    searchedDepartureDates = []

    yellowDate = driver.find_element_by_class_name("departure-calendar").find_element_by_css_selector(".fl.days.yellow")

    yellowDate.click()
    departureDate = moment.date(yellowDate.find_element_by_tag_name('a').get_attribute('href')[28:], "YYYY-MM-DD")
    searchedDepartureDates.append(yellowDate.find_element_by_tag_name('a').get_attribute('href')[28:])

    driver.find_element_by_id("arrival_date_shadow").click()

    WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".arrival-calendar .calendar"))
    )

    arrivalYellowDates = driver.find_element_by_class_name("arrival-calendar").find_elements_by_css_selector(
        ".fl.days.yellow")
    for dateElem in arrivalYellowDates:
        arrivalDate = moment.date(dateElem.find_element_by_tag_name('a').get_attribute('href')[28:], "YYYY-MM-DD")
        if arrivalDate.diff(departureDate, 'days').days == 7:
            dateElem.click()
            break

    print driver.find_element_by_name("arrival").get_attribute("value")
    print driver.find_element_by_name("departure_date").get_attribute("value")
    print driver.find_element_by_name("arrival_date").get_attribute("value")

    driver.find_element_by_id("skrydziai-submit").click()

    WebDriverWait(driver, 100).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".cekis"))
    )

    print_cekis()

    for _ in range(0, 40):
        driver.find_element_by_class_name("update-search").find_element_by_tag_name("a").click()

        driver.find_element_by_id("departure_date").click()

        WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".departure-calendar .calendar"))
        )

        yellowDate = None

        for date in driver.find_element_by_class_name("departure-calendar").find_elements_by_css_selector(
                ".fl.days.yellow"):
            dateString = date.find_element_by_tag_name('a').get_attribute('href')[28:]
            if dateString in searchedDepartureDates:
                continue

            yellowDate = date
            break

        if yellowDate is None:
            break

        yellowDate.click()
        departureDate = moment.date(yellowDate.find_element_by_tag_name('a').get_attribute('href')[28:], "YYYY-MM-DD")

        searchedDepartureDates.append(yellowDate.find_element_by_tag_name('a').get_attribute('href')[28:])

        driver.find_element_by_id("arrival_date").click()

        WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".arrival-calendar .calendar"))
        )
        time.sleep(1)

        # O gal skrydis po 8 dienu
        driver.find_element_by_class_name("arrival-calendar").find_element_by_xpath(
            './/a[@href="' + departureDate.add(days=7).format("YYYY-MM-DD") + '"]').click()

        if driver.find_element_by_class_name("arrival-calendar").is_displayed():
            print "Calendar still displayed"
            driver.find_element_by_class_name("arrival-calendar").find_element_by_xpath(
                './/a[@href="' + departureDate.add(days=1).format("YYYY-MM-DD") + '"]').click()

        # Jeigu kalendorius visvien rodomas, reiskias turim idomia situacija
        if driver.find_element_by_class_name("arrival-calendar").is_displayed():
            break

        driver.find_element_by_id("skrydziai-submit-search").click()

        WebDriverWait(driver, 100).until(
            EC.invisibility_of_element_located((By.ID, "skrydziai-submit-search"))
        )

        WebDriverWait(driver, 100).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".cekis"))
        )

        print_cekis()

    assert "No results found." not in driver.page_source
finally:
    driver.close()
