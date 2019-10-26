#!/usr/bin/env python
# coding: utf-8

# This is my first JupyterLab Notebook

# In[1]:




#load libraries
from google.cloud import bigquery
from google.oauth2 import service_account
from bs4 import BeautifulSoup
from decimal import Decimal
import requests
import re
import pandas as pd
import string
import sys

import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import Select


# In[2]:



key_path='/home/wallacel_wong/My First Project-7dc573b964c1.json'
print("X")
credentials = service_account.Credentials.from_service_account_file(
    key_path,
    scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

bigquery_client=bigquery.Client(credentials=credentials,
                                project='sunny-influence-196423')

dataset_ref = bigquery_client.dataset('gthl_standings')
table_ref = dataset_ref.table('standings_v2')
table = bigquery_client.get_table(table_ref)  # API call\
print(credentials.project_id)
print(table.schema)
#test_rows = [[10],[20],[30]]
test_rows=[['2019-10-30 12:00:00', 'Minor Atom', 'A', 'East', '19-20', 1, 'Don Mills Mustangs ', 8, '8-0-0', 16, 1.0, 7.0, 1.5, '5-0-0', '3-0-0', '8-0-0', 'Won 8', 0]]
row=[]
row.append(test_rows)
print(row)
#print("XX")
#print(type(test_rows[0]))
#test_rows =[('','Peewee','A','East','19-20','1','Leaside',1,'0-0-0',1,'100',1,1,1,1,0,1,0)]#errors = bigquery_client.insert_rows(table, test_rows)  # API request

#print (errors)

# uncomment to debug table inserts
errors = bigquery_client.insert_rows(table, test_rows)  # API Call to insert           
#sys.exit(1)


dateTimeObj = datetime.datetime.now()
timestring=dateTimeObj.strftime("%Y-%m-%d %H:%M:%S")
print(timestring);
print(dateTimeObj)

driver = webdriver.PhantomJS()

menu_list = [['Minor Atom','A','East','19-20'],['Atom','A','East','19-20'],['Minor Peewee','A','East','19-20'],['Peewee','A','East','19-20'], 
             ['Minor Bantam','A','East','19-20'],['Bantam','A','East','19-20'],['Minor Midget','A','East','19-20'],['Midget Junior','A','East','19-20'],
             ['Midget','A','East','19-20'],
             ['Minor Atom','A','West','19-20'],['Atom','A','West','19-20'],['Minor Peewee','A','West','19-20'],['Peewee','A','West','19-20'], 
             ['Minor Bantam','A','West','19-20'],['Bantam','A','West','19-20'],['Minor Midget','A','West','19-20'],['Midget Junior','A','West','19-20'],
            ]
             
             #,['U21','A','','19-20']]
                                                                          
driver.get('https://www.gthlcanada.com/leaguestandings/')
driver.switch_to.frame("iframed-stats")

columns = ['Timestamp','Division','Category','Region','Season','Rank','Team','GP','W-L-T','PTS','WIN%','GFA','GAA','Home','Away','P10','Streak','PIM']
gthlstandings_df=pd.DataFrame(columns=columns)

#sys.exit(0)

# assign parameter inputs
for div_item in menu_list:
        division=div_item[0]
        category=div_item[1]
        region=div_item[2]
        season=div_item[3]
        
        print (division+" "+category+" "+region+" "+season)

        dd_division = Select(driver.find_element_by_id('ddlDiv'))
        dd_division.select_by_visible_text(division)
        dd_category = Select(driver.find_element_by_id('ddlCat'))
        dd_category.select_by_visible_text(category)
        dd_season = Select(driver.find_element_by_id('ddlSeason'))
        dd_season.select_by_visible_text(season)
        dd_category = Select(driver.find_element_by_id('ddlRegion'))
        dd_category.select_by_visible_text(region)

        html = driver.page_source

        html_lines=html.splitlines()
        
        #line_num=0
        #for x in html_lines:
        #    line_num=line_num+1
        #    if "st_wrapper" in x:
        #            print ("found ")
        #            break
        #    print(str(line_num)+"*" + x)


        # delete uncessary page code
        #del html_lines[0:yy]
        #print(len(html_lines))
        #for x in html_lines:
        #    print(x)

        #print(html)

        #sys.exit()


        # Read file
        #file1="/home/jupyter/tutorials/bigquery/test"
        #page=open(file1)
        #content=BeautifulSoup(page.read())
        content=BeautifulSoup(html)

        #print(content)
        #sys.exit(0)

        # Create the data frame
        metrics = [['Leaside flames',6,'6-0-0-',12,1.000,4.17,1.50,'3-0-0','3-0-0','6-0-0','Won 6',0],['Leaside flames',6,'6-0-0-',12,1.000,4.17,1.50,'3-0-0','3-0-0','6-0-0','Won 6',0]]
        #print(type(metrics))
        #columns = ['Team','GP','W-L-T','PTS','WIN%','GFA','GAA','Home','Away','P10','Streak','PIM']
        #gthlstandings_df=pd.DataFrame(columns=columns)

        #print(gthlstandings_df)

        #print(content)

       
        standings=content.find_all('tr',{'class':'st_RepeaterBody'})
        #print(standings)
        rank=0
        for standing in standings:
            team=standing.find_all('td',{'class':'tblTeam'})
            #team1=team.find_all('td')
            #print(type(team))
            #print(team)
            #print(team[0]['data'])
            list=[]
            #list.append(dateTimeObj)
            #list.append('')
            #list.append(None)
            list.append(timestring)
            list.append(division)
            list.append(category)
            list.append(region)
            list.append(season)
            rank=rank+1
            list.append(rank)
            list.append(team[0]['data'])
            
            #print(team[0].div.input['class'])
            data=standing.find_all('td',{'class':re.compile('^cBlack fArialS8N aCenter')})
            #print(data)

            #print("*******",list)
            
            index=0
            for x in data:
                
               # print(x.contents[0])
                if(index==0 or index==2 or index==10):
                     #print(x.contents[0])
                     list.append(int(x.contents[0]))
                elif (index==3 or index==4 or index==5):
                     list.append(float(x.contents[0]))
                else:
                    list.append(x.contents[0])
                index=index+1
            #print(list)
            #print("****")
            #print (type(list))
            insert_list=[]
            insert_list.append(list)
            gthlstandings_df.loc[len(gthlstandings_df)]=list
            test_data=[None, 'Minor Atom', 'A', 'East', '19-20', 1, 'Don Mills Mustangs ', 8, '8-0-0', 16, 1.0, 7.0, 1.5, '5-0-0', '3-0-0', '8-0-0', 'Won 8', 0]
            errors = bigquery_client.insert_rows(table, insert_list)  # API Call to insert
            
           
print(gthlstandings_df.to_string())

#print (type(gthlstandings_df))
#errors = bigquery_client.insert_rows(table, gthlstandings_df)  # API request


# In[4]:


#pip install BeautifulSoup4


# In[8]:


#pip install -U Selenium


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




