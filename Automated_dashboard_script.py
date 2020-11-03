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

#data analysis
import pandas as pd
import re

pd.set_option('display.max_rows', 500)
pd.options.display.max_colwidth = 150
# again we need to locate the .xlsx file
list_of_files = glob.glob('/Users/Sully/Desktop/NewGit/Automated_interactive_dashboard/*.xlsx')
latest_file = max(list_of_files, key=os.path.getctime)
#print(latest_file.split("\\")[-1])
df = pd.read_excel("{}".format(latest_file),header=None)
#print(df.head())


#dropping uneccessary data

# print out latest COVID data datetime and notes
date = re.findall("- [0-9]+/[0-9]+/[0-9]+ .+", df.iloc[0, 0])
#print("COVID cases latest update:", date[0][2:])
#print(df.iloc[1, 0])
#print(str(df.iloc[262:266, 0]).lstrip().rstrip())
#drop non-data rows
df2 = df.drop([0, 1, 258, 260, 261, 262, 263, 264, 265, 266, 267])



# clean column names
df2.iloc[0,:] = df2.iloc[0,:].apply(lambda x: x.replace("\r", ""))
df2.iloc[0,:] = df2.iloc[0,:].apply(lambda x: x.replace("\n", ""))
df2.columns = df2.iloc[0]
clean_df = df2.drop(df2.index[0])
clean_df = clean_df.set_index("County Name")
# convert clean_df to a .csv file
clean_df.to_csv("Texas county COVID cases data clean.csv")

