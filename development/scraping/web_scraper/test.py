from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import time
import csv
import itertools
import sys

import asyncio

start_time = time.time()
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")
options.add_argument('--headless')
driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver", options=options)
driver.set_window_size(1920, 1080)
driver.get('https://www.m13.com/product/drink-coaster-printing')


product_id = 7
rows = []
rows.append(['Product ID', 'Economy Price', 'Economy Sale Price', 'Economy No Of Days', 'Fast Price', 'Fast Sale Price', 'Fast No Of Days', 'Faster Price', 'Faster Sale Price', 'Faster No Of Days', 'Crazy Fast Price', 'Crazy fast sale price', 'Crazy fast No Of Days', 'Labels', 'Quantity'])

# time.sleep(2)

selectQuantity = Select(driver.find_element_by_id("QuantitySelected"))
selectPrintSize = Select(driver.find_element_by_id("Order_ProductSizeId"))
selectSides = Select(driver.find_element_by_id("Order_SidesId"))
selectPaperStock = Select(driver.find_element_by_id("Order_PaperStockId"))

selectQuantityValues = []
for option in selectQuantity.options:
    selectQuantityValue = option.get_attribute("value")
    if selectQuantityValue != '' and selectQuantityValue != '-1':
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

optionValuesList = [selectQuantityValues, selectPrintSizeValues, selectSidesValues, selectPaperStockValues]
optionValuesCombination = tuple(itertools.product(*optionValuesList))
print(len(optionValuesCombination))
print(optionValuesCombination[0:40])
# print(sys.getsizeof(optionValuesCombination)

# time.sleep(5)


async def mycoro(start, end):
    for x in range(start, end):
        # await asyncio.sleep(1)
        selectQuantity.select_by_value(str(optionValuesCombination[x][0]))
        selectPrintSize.select_by_value(str(optionValuesCombination[x][1]))
        selectSides.select_by_value(str(optionValuesCombination[x][2]))
        selectPaperStock.select_by_value(str(optionValuesCombination[x][3]))
        await asyncio.sleep(2)
        print(x)
        print([optionValuesCombination[x][0], optionValuesCombination[x][1], optionValuesCombination[x][2], optionValuesCombination[x][3]])

        if optionValuesCombination[x][0] in selectQuantityValues:
            selectQuantityText = selectQuantity.first_selected_option.text

        if optionValuesCombination[x][1] in selectPrintSizeValues:
            selectPrintSizeText = selectPrintSize.first_selected_option.text

        if optionValuesCombination[x][2] in selectSidesValues:
            selectSideText = selectSides.first_selected_option.text

        if optionValuesCombination[x][3] in selectPaperStockValues:
            selectPaperStockText = selectPaperStock.first_selected_option.text

        # time.sleep(0.9)
        
        page_source = driver.page_source
        # print(page_source)

        soup = BeautifulSoup(page_source, 'lxml')
        # print(soup.prettify())
        # time.sleep(5)
        
        await asyncio.sleep(1)
        # service_types = []
        # service_days = []
        # service_prices = []

        turnaroundrow_data = soup.find('tr', class_='turnaroundrow')
        # for turnaroundrow_dt in turnaroundrow_data:
        service_type = turnaroundrow_data.find('span').get_text()
        service_type = service_type.strip()
        # service_types.append(service_type)

        service_day = turnaroundrow_data.find('span', class_='turnarounddescription').get_text()
        service_day = service_day.strip()
        # service_days.append(service_day)

        service_price = turnaroundrow_data.find('td', class_='turnaroundprice').get_text()
        service_price = service_price.strip().split("\n")
        if service_price == ['Please Call']:
            service_price = ['Please Call', 'Please Call']
        # service_prices.append(service_price)
        
            
        print(service_price)
        # try:
        # 	rows.append([product_id, service_prices[0][0], service_prices[0][1], service_days[0], service_prices[1][0], service_prices[1][1], service_days[1], service_prices[2][0], service_prices[2][1], service_days[2], service_prices[3][0], service_prices[3][1], service_days[3], 
        #         'PRINT SIZE={}, SIDES={}, PAPER OR STOCK={}'.format(selectPrintSizeText, selectSideText, selectPaperStockText), selectQuantityText
        #     ])
        # except Exception as e:
        # 	print(e)

    # driver.save_screenshot('WebsiteScreenShot.png')
    # print(service_types)
    # print(service_days)
    # print(service_prices)

    # Create csv and write rows to output file
    with open('files/drink-coaster_1.csv', 'w', newline='') as f_output:
        csv_output = csv.writer(f_output)
        csv_output.writerows(rows)


async def doit():
    return await asyncio.gather(mycoro(0,10), mycoro(10, 20), mycoro(20,30), mycoro(30,40))

many = doit()
asyncio.run(many)
print("End--- %s seconds ---" % (time.time() - start_time))



# from aiohttp import ClientSession
# import asyncio
# from itertools import islice
# import sys

# def limited_as_completed(coros, limit):
#     futures = [
#         asyncio.ensure_future(c)
#         for c in islice(coros, 0, limit)
#     ]
#     async def first_to_finish():
#         while True:
#             await asyncio.sleep(0)
#             for f in futures:
#                 if f.done():
#                     futures.remove(f)
#                     try:
#                         newf = next(coros)
#                         futures.append(
#                             asyncio.ensure_future(newf))
#                     except StopIteration as e:
#                         pass
#                     return f.result()
#     while len(futures) > 0:
#         yield first_to_finish()

# async def fetch(url, session):
#     async with session.get(url) as response:
#         return await response.read()

# limit = 1000

# async def print_when_done(tasks):
#     for res in limited_as_completed(tasks, limit):
#         await res

# r = int(sys.argv[1])
# url = "https://google.com/{}"
# loop = asyncio.get_event_loop()
# with ClientSession() as session:
#     coros = (fetch(url.format(i), session) for i in range(r))
#     loop.run_until_complete(print_when_done(coros))
# loop.close()