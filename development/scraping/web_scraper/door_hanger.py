#!/home/apptrinity19/development/scraping/web_scraper/env/bin/python

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import time
from datetime import date
import csv
import itertools


start_time = time.time()
product_id = 12
rows = []
rows.append([
        'Product ID', 
        'Economy Price', 
        'Economy Sale Price', 
        'Economy No Of Days', 
        'Fast Price', 
        'Fast Sale Price', 
        'Fast No Of Days', 
        'Faster Price', 
        'Faster Sale Price', 
        'Faster No Of Days', 
        'Crazy Fast Price', 
        'Crazy fast sale price', 
        'Crazy fast No Of Days', 
        'Labels', 
        'Quantity'
    ])


def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")
    options.add_argument('--headless')
    driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver", options=options)
    driver.set_window_size(1920, 1080)
    return driver


def lookup(driver):
    driver.get('https://www.m13.com/product/door-hanger-printing')

    selectQuantity = Select(driver.find_element_by_id("QuantitySelected"))
    # selectQuantity.select_by_value(quantity)
    # time.sleep(1)
    selectPrintSize = Select(driver.find_element_by_id("Order_ProductSizeId"))
    # selectPrintSize.select_by_value(printSize)
    # time.sleep(1)
    selectSides = Select(driver.find_element_by_id("Order_SidesId"))
    # selectSides.select_by_value(sides)
    # time.sleep((1))
    selectPaperStock = Select(driver.find_element_by_id("Order_PaperStockId"))
    # selectPaperStock.select_by_value(paperStock)
    # time.sleep(1)
    selectCoating = Select(driver.find_element_by_id("Order_CoatingId"))
    # selectCoating.select_by_value(coating)
    # time.sleep(1)
    selectSlit = Select(driver.find_element_by_id("SelectedOrderOptions_10__Value"))
    # selectSlit.select_by_value(slit)
    # time.sleep(1)

    selectQuantityValues = []
    for option in selectQuantity.options:
        selectQuantityValue = option.get_attribute("value")
        # print(option.get_attribute("value"))
        # selectQuantity.select_by_value(selectQuantityValue)
        if selectQuantityValue != '' and  selectQuantityValue != '-1':
            selectQuantityValues.append(selectQuantityValue)
    # print(selectQuantityValues)
    # time.sleep(1)       

    selectPrintSizeValues = []
    for option in selectPrintSize.options:
        selectPrintSizeValue = option.get_attribute("value")
        if selectPrintSizeValue != '':
            selectPrintSizeValues.append(selectPrintSizeValue)
    # print(selectPrintSizeValues)
    # time.sleep(1)

    selectSidesValues = []
    for option in selectSides.options:
        selectSidesValue = option.get_attribute("value")
        if selectSidesValue != '':
            selectSidesValues.append(selectSidesValue)
    # print(selectSidesValues)
    # time.sleep(1)

    selectPaperStockValues = []
    for option in selectPaperStock.options:
        selectPaperStockValue = option.get_attribute("value")
        if selectPaperStockValue != '':
            selectPaperStockValues.append(selectPaperStockValue)
    # print(selectPaperStockValues)
    # time.sleep(1)

    selectCoatingValues = []
    for option in selectCoating.options:
        selectCoatingValue = option.get_attribute("value")
        if selectCoatingValue != '':
            selectCoatingValues.append(selectCoatingValue)
    # print(selectCoatingValues)
    # time.sleep(1)

    selectSlitValues = []
    for option in selectSlit.options:
        selectSlitValue = option.get_attribute("value")
        if selectSlitValue != '':
            selectSlitValues.append(selectSlitValue)
    # print(selectSlitValues)
    # time.sleep(1)

    optionValuesList = [selectQuantityValues, selectPrintSizeValues, selectSidesValues, selectPaperStockValues, selectCoatingValues, selectSlitValues]
    time.sleep(0.05)
    optionValuesCombination = list(itertools.product(*optionValuesList))
    print(len(optionValuesCombination))
    # print(optionValuesCombination[0:50])

    # time.sleep(5)
    for x in range(len(optionValuesCombination)):
        selectQuantity.select_by_value(str(optionValuesCombination[x][0]))
        if str(optionValuesCombination[x][1]) != '628':
            selectPrintSize.select_by_value(str(optionValuesCombination[x][1]))
        selectSides.select_by_value(str(optionValuesCombination[x][2]))
        selectPaperStock.select_by_value(str(optionValuesCombination[x][3]))
        # selectCoating.select_by_value(str(optionValuesCombination[x][4]))
        if str(optionValuesCombination[x][3]) == '2' and str(optionValuesCombination[x][4]) == '8':
            selectCoating.select_by_value("1")
        else:
            selectCoating.select_by_value(str(optionValuesCombination[x][4]))
        selectSlit.select_by_value(str(optionValuesCombination[x][5]))
        # print(x)

        if optionValuesCombination[x][1] in selectPrintSizeValues:
            selectPrintSizeText = selectPrintSize.first_selected_option.text

        if optionValuesCombination[x][2] in selectSidesValues:
            selectSidesText = selectSides.first_selected_option.text

        if optionValuesCombination[x][3] in selectPaperStockValues:
            selectPaperStockText = selectPaperStock.first_selected_option.text

        if optionValuesCombination[x][4] in selectCoatingValues:
            selectCoatingText = selectCoating.first_selected_option.text

        if optionValuesCombination[x][5] in selectSlitValues:
            selectSlitText = selectSlit.first_selected_option.text
            # print(selectSlitText)
        time.sleep(0.9)
        page_source = driver.page_source
        # print(page_source)

        soup = BeautifulSoup(page_source, 'lxml')
        # print(soup.prettify())
        # time.sleep(5)
        service_types = []
        service_days = []
        service_prices = []
        turnaroundrow_data = soup.find_all('tr', class_='turnaroundrow')
        for turnaroundrow_dt in turnaroundrow_data:
            service_type = turnaroundrow_dt.find('span').get_text()
            service_type = service_type.strip()
            service_types.append(service_type)

            service_day = turnaroundrow_dt.find('span', class_='turnarounddescription').get_text()
            service_day = service_day.strip()
            service_days.append(service_day)

            service_price = turnaroundrow_dt.find('td', class_='turnaroundprice').get_text()
            service_price = service_price.strip().split("\n")
            # print(service_price)
            if service_price == ['Please Call']:
                service_price = ['Please Call', 'Please Call']
            service_prices.append(service_price)

        # rows.append([product_id, service_prices[0], '', service_days[0], service_prices[1], '', service_days[1], service_prices[2], '', service_days[2], service_prices[3], '', service_days[3], 
        #         'PRINT SIZE={};, SIDES={};, PAPER OR STOCK={};, COATING={};Variable Data=0; Door Hanger Die Cut=0; Slit Position={}'.format(optionValuesCombination[x][1], optionValuesCombination[x][2], optionValuesCombination[x][3], optionValuesCombination[x][4], selectSlitText), optionValuesCombination[x][0]
        #     ])
        
        try:
            # print(service_prices)
            rows.append([
                product_id, 
                service_prices[0][0], 
                service_prices[0][1], 
                service_days[0], 
                service_prices[1][0], 
                service_prices[1][1], 
                service_days[1], 
                service_prices[2][0], 
                service_prices[2][1], 
                service_days[2], 
                service_prices[3][0], 
                service_prices[3][1], 
                service_days[3], 
                    'PRINT SIZE={}, SIDES={}, PAPER OR STOCK={}, COATING={}, Variable Data=0, Door Hanger Die Cut=0, Slit Position={}'.format(selectPrintSizeText, selectSidesText, selectPaperStockText, selectCoatingText, selectSlitText), 
                    optionValuesCombination[x][0]
                ])
        except Exception as e:
            print(e)
            rows.append([product_id, '', '', '', '', '', '', '', '', '', '', '', '', 
                    'PRINT SIZE={}, SIDES={}, PAPER OR STOCK={}, COATING={}, Variable Data=0, Door Hanger Die Cut=0, Slit Position={}'.format(selectPrintSizeText, selectSidesText, selectPaperStockText, selectCoatingText, selectSlitText), 
                    optionValuesCombination[x][0]
                ])
    return rows


def excel_file(rows):
    # Create csv and write rows to output file
    with open('/home/apptrinity19/development/scraping/web_scraper/files/door-hanger_' + str(date.today()) +  '.csv', 'w', newline='') as f_output:
        csv_output = csv.writer(f_output)
        csv_output.writerows(rows)
    print("End--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    driver = init_driver()
    lookup(driver)
    excel_file(rows)
    time.sleep(2)
    driver.quit()
