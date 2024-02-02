# import codecademylib3_seaborn
from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


prefix = "https://content.codecademy.com/courses/beautifulsoup/"
webpage_response = requests.get('https://content.codecademy.com/courses/beautifulsoup/cacao/index.html')


webpage = webpage_response.content
soup = BeautifulSoup(webpage, "html.parser")

######################## This section scrapes all drafting data by year ############
# for year in range(14, 24):
#   league_link = "https://fantasy.nfl.com/league/2338570/history/20" + str(year) + "/draftresults?draftResultsDetail=0&draftResultsTab=round&draftResultsType=results"
#   print(league_link)
  
#   nfl_webpage_response = requests.get(league_link)
#   nfl_page = nfl_webpage_response.content
#   nfl_soup = BeautifulSoup(nfl_page, "html.parser")

#   nfl_draft_order = nfl_soup.find_all(attrs={"class": "count"})
#   nfl_draft_players = nfl_soup.find_all(attrs={"class": "playerName"})
#   team_name = nfl_soup.find_all("li", class_="first last")
#   nfl_draft_auction_for = nfl_soup.find_all(attrs={"class": "auctionCost"})
#   draft_order = []
#   auction_amount = []
#   player_names = []
#   team_names = []
#   for order in nfl_draft_order:
#     order_to_number = order.get_text().split('.')[0]
#     draft_order.append(int(order_to_number))
#   for price in nfl_draft_auction_for:
#     auction_to_number = price.get_text().split('$')[1]
#     auction_amount.append(int(auction_to_number))

#   for name in nfl_draft_players:
#     player_names.append(name.get_text())

#   for name in team_name:
#     team_names.append(name.get_text())
  
#   if len(auction_amount) > 0:
#     draft_2014_dict = {"Draft Number" : draft_order, "Player Name" : player_names, "Auction Amount": auction_amount, "Team Name": team_name }
#     draft_2014 = pd.DataFrame.from_dict(draft_2014_dict)
#   else:
#     draft_2014_dict = {"Draft Number" : draft_order, "Player Name" : player_names, "Team Name": team_name }
#     draft_2014 = pd.DataFrame.from_dict(draft_2014_dict)
  
#   print(draft_2014)

######################## This section scrapes all Win/Loss data by year ############
for year in range(14, 24):
  ######### Get an updated dictionary of the year's owners and real name ######## 
  manager_names = "https://fantasy.nfl.com/league/2338570/history/20" + str(year) + "/owners"
  manager_web_response = requests.get(manager_names)
  manager_page = BeautifulSoup(manager_web_response.content, "html.parser")
  team_name = []
  user_name = []
  team_names = manager_page.find_all("a", class_="teamName")
  user_names = manager_page.find_all("td", class_="teamOwnerName")
  # print()
  user_name_count = 0
  for manager in team_names:
    team_name.append(manager.get_text())
    name = user_names[user_name_count].get_text()
    if name == "Jim":
      name = "Matt T"
    user_name.append(name)
    user_name_count +=1
  team_to_player_dict = dict(zip(team_name, user_name))
  #use dict.get() method to change the Matts
  print(team_to_player_dict)

  ######### Get the Win/Loss Records and Points for ######## 

  # league_link_WL = "https://fantasy.nfl.com/league/2338570/history/20" + str(year) + "/draftresults?draftResultsDetail=0&draftResultsTab=round&draftResultsType=results"

  # nfl_webpage_response_WL = requests.get(league_link)
  # nfl_page_WL = nfl_webpage_response.content
  # nfl_soup_WL = BeautifulSoup(nfl_page, "html.parser")









chocolate_ratings = soup.find_all(attrs={"class": "Rating"})

ratings = []

for rating in chocolate_ratings[1:]:
    ratings.append(float(rating.get_text()))



# print(ratings)

names = []
company_names = soup.select(".Company")
# print(company_names)
for name in company_names[1:]:
    names.append(name.get_text())

# print(names)
percents = []
cocoa_percents = soup.select(".CocoaPercent")
for percent in cocoa_percents[1:]:
  num_to_add = float(percent.get_text().split('%')[0])
  percents.append(num_to_add)
    
d = {"Company" : names, "Ratings" : ratings, "CocoaPercent": percents }
chocolate_df = pd.DataFrame.from_dict(d)
# print(chocolate_df.nlargest(4, 'Ratings', keep='all'))
average_rating = chocolate_df.groupby(['Company']).Ratings.mean()
# top_ten = average_rating.nlargest(10)
# print(top_ten)
# chocolate_df.index += 1
# print(chocolate_df)

# plt.scatter(chocolate_df.CocoaPercent, chocolate_df.Ratings)
# z = np.polyfit(chocolate_df.CocoaPercent, chocolate_df.Ratings, 1)
# line_function = np.poly1d(z)
# plt.plot(chocolate_df.CocoaPercent, line_function(chocolate_df.CocoaPercent), "r--")

# plt.show()





