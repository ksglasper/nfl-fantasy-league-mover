import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

prefix = "https://content.codecademy.com/courses/beautifulsoup/"
webpage_response = requests.get('https://content.codecademy.com/courses/beautifulsoup/shellter.html')

webpage = webpage_response.content
soup = BeautifulSoup(webpage, "html.parser")

turtle_links = soup.find_all("a")
links = []
#go through all of the a tags and get the links associated with them"
for a in turtle_links:
  links.append(prefix+a["href"])
    
#Define turtle_data:
turtle_data = {}

#follow each link:
for link in links:
  webpage = requests.get(link)
  turtle = BeautifulSoup(webpage.content, "html.parser")
  turtle_name = turtle.select(".name")[0].get_text()
  
  stats = turtle.find("ul")
  appendList = [info for info in turtle.find("ul").get_text('|').split('|') if info != '\n']
  test = [ i for i in turtle.find("ul").get_text("|").split('|') if i != '\n']



  turtle_data[turtle_name] = appendList
  

turtle_df = pd.DataFrame.from_dict(turtle_data, orient='index')



# final_turtle_df = turtle_df.rename(columns={"0": "Age"})

# turtle_df = turtle_df.drop(turtle_df.columns[-1], axis=1)

final_df = turtle_df.reset_index()
turtle_df = turtle_df.reset_index().rename(columns={"index": "Name", 0: "Age (years)", 1 : "Weight (lbs)", 2 : "Sex", 3 : "Breed", 4 : "Source"})
# turtle_df['Age (years)'] = turtle_df['Age (years)'].apply(pd.to_numeric(errors='ignore'))
# pd.to_numeric(turtle_df['Age (years)'], errors='ignore')
# print(turtle_df)

turtle_df['Age (years)'] = turtle_df['Age (years)'].str.extract('([0-9]*[,.][0-9]*|\d+)').apply(pd.to_numeric)
turtle_df['Weight (lbs)'] = turtle_df['Weight (lbs)'].str.extract('([0-9]*[,.][0-9]*|\d+)').apply(pd.to_numeric)
turtle_df['Sex'] = turtle_df['Sex'].str.split().str[-1]
turtle_df['Breed'] = turtle_df['Breed'].str.extract('\ (.*)')
turtle_df['Source'] = turtle_df['Source'].str.extract('\ (.*)')
turtle_df['Source'] = turtle_df['Source'].str.title()

print(turtle_df)


# print(final_df)
