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
  # print(appendList)
  # stats_text = [i in stats.get_text("|")]
  # print(stats_text)
  # appendList = info for info in stats_text if info != '\n'
  turtle_data[turtle_name] = appendList
# print(turtle_data)
  

turtle_df = pd.DataFrame.from_dict(turtle_data, orient='index')
# turtle_df.drop(columns=1)
final_turtle_df = turtle_df.rename(columns={"0": "Age"})

print(final_turtle_df)
