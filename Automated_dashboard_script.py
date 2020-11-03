# import packages
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import shutil
import glob
import os
from unicodedata import *
import time
# open a chrome browser using selenium
driver = webdriver.Chrome(ChromeDriverManager().install())
# got to web page where excel file links are located
driver.get("https://www.dshs.texas.gov/coronavirus/additionaldata/")
# these options allow selenium to download files
options = Options()
options.add_experimental_option("browser.download.folderList",2)
options.add_experimental_option("browser.download.manager.showWhenStarting", False)
options.add_experimental_option("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream,application/vnd.ms-excel")


# initialize an object to the location on the web page and click on it to download
link = driver.find_element_by_xpath('/html/body/form/div[4]/div/div[3]/div[2]/div/div/ul[1]/li[1]/a')
link.click()
# Wait for 15 seconds to allow chrome to download file
time.sleep(15)

# locating most recent .xlsx downloaded file
list_of_files = glob.glob('/Users/Sully/Downloads/*.xlsx')
latest_file = max(list_of_files, key=os.path.getmtime)
# replace "\" with "/" so file path can be located by python
latest_file = latest_file.replace("\\", "/")
latest_file
# we need to locate the old .xlsx file(s) in the dir we want to store the new xlsx file in
list_of_files = glob.glob('/Users/Sully/Desktop/NewGit/Automated_interactive_dashboard/*.xlsx')
# need to delete old xlsx file(s) so if we download new xlsx file with same name we do not get an error while moving it
for file in list_of_files:
    print("deleting old xlsx file:", file)
    os.remove(file)
# Move the new file from the download dir to the github dir
shutil.move(latest_file,'/Users/Sully/Desktop/NewGit/Automated_interactive_dashboard/')
