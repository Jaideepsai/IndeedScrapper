
# coding: utf-8

# In[31]:


# Code for extracting data from Indeed reviews
import sys
import urllib
from random import randint
from selenium import webdriver
import pandas as pd
import numpy as np
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import csv
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


# In[32]:


# Code to remove special characters from the text
def cleanString(incomingString):
    newstring = incomingString
    newstring = newstring.replace("!","")
    newstring = newstring.replace("@","")
    newstring = newstring.replace("#","")
    newstring = newstring.replace("$","")
    newstring = newstring.replace("-","")
    newstring = newstring.replace("%","")
    newstring = newstring.replace("^","")
    newstring = newstring.replace(",","")
    newstring = newstring.replace("&"," and ")
    newstring = newstring.replace("*","")
    newstring = newstring.replace("(","")
    newstring = newstring.replace(")","")
    newstring = newstring.replace("+","")
    newstring = newstring.replace("=","")
    newstring = newstring.replace("?","")
    newstring = newstring.replace("\'","")
    newstring = newstring.replace("'","")
    newstring = newstring.replace("\"","")
    newstring = newstring.replace("{","")
    newstring = newstring.replace("}","")
    newstring = newstring.replace("[","")
    newstring = newstring.replace("]","")
    newstring = newstring.replace("<","")
    newstring = newstring.replace(">","")
    newstring = newstring.replace("~","")
    newstring = newstring.replace("`","")
    newstring = newstring.replace(":","")
    newstring = newstring.replace(";","")
    newstring = newstring.replace("|","")
    newstring = newstring.replace("\\","")
    newstring = newstring.replace("/","")
    newstring = newstring.replace("\n"," ")
    newstring = newstring.replace("\u2013"," ")
    return newstring


def get_date(strdate):
    splitstr = strdate.split(" ")
    slen = len(splitstr)
    ylen = slen-1
    dlen = slen-2
    mlen = slen-3
    month = splitstr[mlen]
    day   = splitstr[dlen]
    year  = splitstr[ylen]
    if int(year) < 2015:
        raise Exception('Year is greater than 2015');
    else:
        datestr =  day + "," + month + "," + year
        return datestr

def get_employee_status(job_status):
    splittitle = job_status.split(" ")
    titlelen = len(splittitle)
    flen = titlelen-5
    status = splittitle[flen]
    job_status = status.replace("(","")
    return job_status

def page_data(content,num_post):
    j=0
    while(j<num_post):
        job_title = content[j].find_element_by_class_name('cmp-reviewer').text
        val1 = cleanString(job_title)
        job_status = content[j].find_element_by_class_name('cmp-reviewer-job-title').text
        val5 = get_employee_status(job_status)
        job_location = content[j].find_element_by_class_name('cmp-reviewer-job-location').text
        val2 = cleanString(job_location)
        date = content[j].find_element_by_class_name('cmp-review-date-created').text
        strdate = cleanString(date)
        val3 = get_date(strdate)
        review_desc = content[j].find_element_by_class_name('cmp-review-description').text
        val4 = cleanString(review_desc)
        dstr =  val1 + "," + val5 + "," + val2 + "," + val3 + "," + val4
        print(dstr)
        print(row[1])
        f.append(val1)
        g.append(val2)
        f1.append(val3)
        g1.append(val4)
        f2.append(val5)
        g2.append(str(row[1]))
        time.sleep(randint(0,2))
        j=j+1


# Code for next page
def next_page():
    time.sleep(randint(0,10))
    driver.find_element_by_link_text("Next").click()


def write_data():
    i=0
    while(i<6000):
        content = driver.find_elements_by_xpath("//div[@class='cmp-review']")
        num_post = len(content)
        try:
            page_data(content,num_post)
        except:
            print '<-----nextURl should start---->';
            break;
        time.sleep(3)
        try:
            next_page()
        except:
            break;
        i=i+1

def write_csv():
    df_list = pd.DataFrame(
                {
                    'symbol':g2,
                 'job_title':f,
                 'job_location':g,
                    'date':f1,
                 'review_desc':g1,
                      'job_status':f2
                })
    df_list.to_csv("first20.csv", encoding="utf-8",sep=',')


# In[33]:


# Calling driver function and Indeed review webpage
def main():
    time.sleep(3)
    write_data();
    write_csv();
    
if __name__ == "__main__":
    d=[];e=[];f=[];g=[];f1=[];g1=[];f2=[];g2=[];d1=[]
    data=pd.read_csv("IC-RevGrowthData-V2.csv")
    df = pd.DataFrame(data)
    driver = webdriver.Firefox()
    for row in df.itertuples():
        print(row[12])
        indeed_url=str(row[12]);
        driver.get(indeed_url + "/reviews")
        main()    
    driver.close()


# In[34]:


df_list2 = pd.DataFrame(
                {
                    'symbol':g2,
                 'job_title':f,
                 'job_location':g,
                    'date':f1,
                 'review_desc':g1,
                      'job_status':f2
                })
df_list2.to_csv("first20_v1.csv", encoding="utf-8",sep=',')


# In[35]:


df_list2

