from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from decimal import *



#Helper Functions
def string_in_list(list, string):
   if string in list:
      return True
   else:
      return False

#Core Data Scraping


######################## This section scrapes all drafting data by year ########################
for year in range(14, 15):
  ## Get an updated dictionary of the year's owners and real name ##
  manager_names = "https://fantasy.nfl.com/league/2338570/history/20" + str(year) + "/owners"
  manager_web_response = requests.get(manager_names)
  manager_page = BeautifulSoup(manager_web_response.content, "html.parser")
  team_name = []
  user_name = []
  moves = []
  trades = []
  team_names = manager_page.find_all("a", class_="teamName")
  user_names = manager_page.find_all("td", class_="teamOwnerName")
  user_moves = manager_page.find_all("td", class_="teamTransactionCount numeric")
  user_trades = manager_page.find_all("td", class_="teamTradeCount numeric")

  cycle_count = 0
  alias = ["Xochimilco Axolotls", "West Loop Wyverns", "Toronto Angels", "Parry Sound Dragons", "Barrie Dragons" ]

  for manager in team_names:
    team_name.append(manager.get_text())
    name = user_names[cycle_count].get_text()
    if name == "Jim":
      name = "Matt T"
    if string_in_list(alias, manager.get_text()):
       name = "Matt Z"
    user_name.append(name)
    moves.append(int(user_moves[cycle_count].get_text()))
    trades.append(int(user_trades[cycle_count].get_text()))
    cycle_count +=1

  team_to_player_dict = dict(zip(team_name, user_name))

  ## Create DataFrame with Player, Moves, and Trades by year ##
  move_trade_dict = {"Name" : user_name, "Moves" : moves, "Trades" : trades}
  name_moves_trade_df = pd.DataFrame.from_dict(move_trade_dict)
  name_moves_trade_df.index.name = "Season Transactions: Year 20" + str(year)
  print(name_moves_trade_df)




  league_link = "https://fantasy.nfl.com/league/2338570/history/20" + str(year) + "/draftresults?draftResultsDetail=0&draftResultsTab=round&draftResultsType=results"
  
  nfl_webpage_response = requests.get(league_link)
  nfl_page = nfl_webpage_response.content
  nfl_soup = BeautifulSoup(nfl_page, "html.parser")

  nfl_draft_order = nfl_soup.find_all(attrs={"class": "count"})
  nfl_draft_players = nfl_soup.find_all(attrs={"class": "playerName"})
  team_name = nfl_soup.find_all("a", class_="teamName")
  nfl_draft_auction_for = nfl_soup.find_all(attrs={"class": "auctionCost"})
  draft_order = []
  auction_amount = []
  player_names = []
  team_names = []
  cycle_count = 0
  for order in nfl_draft_order:
    order_to_number = order.get_text().split('.')[0]
    draft_order.append(int(order_to_number))
    player_names.append(nfl_draft_players[cycle_count].get_text())
    team_names.append(team_to_player_dict.get(team_name[cycle_count].get_text()))
    cycle_count += 1
  for price in nfl_draft_auction_for:
    auction_to_number = nfl_draft_auction_for[cycle_count].get_text().split('$')[1]
    auction_amount.append(int(auction_to_number))
  if len(auction_amount) > 0:
    draft_2014_dict = {"Draft Number" : draft_order, "Player Name" : player_names, "Auction Amount": auction_amount, "Team Name": team_names }
    draft_2014 = pd.DataFrame.from_dict(draft_2014_dict)
    draft_2014.index.name = "Auction Draft Results: Year 20" + str(year)
  else:
    draft_2014_dict = {"Draft Number" : draft_order, "Player Name" : player_names, "Team Name": team_names }
    draft_2014 = pd.DataFrame.from_dict(draft_2014_dict)
    draft_2014.index.name = "Snake Draft Results: Year 20" + str(year)
  print(draft_2014)

######################## This section scrapes all Win/Loss, Winning %, Regular Season Rankings, Points For/Against data by year ########################
  
  ## Get the Win/Loss Records, Points for/against, and regular season standings from Standings Page ##

  league_link_Standings = "https://fantasy.nfl.com/league/2338570/history/20" + str(year) + "/standings?historyStandingsType=regular"

  nfl_webpage_response_Standings = requests.get(league_link_Standings)
  nfl_soup_Standings = BeautifulSoup(nfl_webpage_response_Standings.content, "html.parser")

  ## Build ranking, name, win, loss, percent, points for, and points against arrays for DataFrame

  rank = []
  name = []
  wins = []
  losses = []
  percent_WL = []
  points_for = []
  points_against = []

  standings_rank = nfl_soup_Standings.find_all("span", class_="teamRank")
  standings_name = nfl_soup_Standings.find_all("a", class_="teamName")
  standings_wins_and_losses = nfl_soup_Standings.find_all("td", class_="teamRecord numeric")
  standings_percent_WL = nfl_soup_Standings.find_all("td", class_="teamWinPct numeric")
  standings_points_for = nfl_soup_Standings.find_all("td", class_="teamPts stat numeric")
  standings_points_against = nfl_soup_Standings.find_all("td", class_="teamPts stat numeric last")

  #reset cycle_count for next task  
  cycle_count = 0
  for team in standings_rank:
    rank.append(int(team.get_text()))
    user_team_match = team_to_player_dict.get(standings_name[cycle_count].get_text())
    name.append(user_team_match)
    win_loss_split = standings_wins_and_losses[cycle_count].get_text().split('-')
    wins.append(int(win_loss_split[0]))
    losses.append(int(win_loss_split[1]))
    percent_WL.append(float(standings_percent_WL[cycle_count].get_text()))
    points_for.append(float(standings_points_for[cycle_count].get_text().replace(',', '')))
    points_against.append(float(standings_points_against[cycle_count].get_text().replace(',', '')))
    cycle_count += 1

  #create DataFrame from arrays placed in dictionary
  standings_dict = {"Name" : name, "Rank" : rank, "Wins" : wins, "Losses" : losses, "Pct" : percent_WL, "Points For" : points_for, "Points Against" : points_against}
  standings_df = pd.DataFrame.from_dict(standings_dict)
  standings_df.index.name = " Regular Season Standings: Year 20" + str(year)
  print(standings_df)

  ## Get Final Standings for each season ##
  nfl_final_standings_link = requests.get("https://fantasy.nfl.com/league/2338570/history/20" + str(year) + "/standings")
  nfl_final_standings_soup = BeautifulSoup(nfl_final_standings_link.content, "html.parser")

  ## Build final standing and name arrays for Dataframe ##
  final_standing = []
  person = []

  final_standing_tags = nfl_final_standings_soup.find_all("div", class_="place")
  person_tags = nfl_final_standings_soup.find_all("a", class_="teamName")
  
  #reset cycle_count for next task  
  cycle_count = 1
  for place in final_standing_tags:
    final_standing.append(place.get_text())
    person.append(team_to_player_dict.get(person_tags[cycle_count].get_text()))
    cycle_count += 1
  
  #create DataFrame for arrays into dictionary
  final_standings_dict = {"Name" : person, "Place" : final_standing}
  final_standings_df = pd.DataFrame.from_dict(final_standings_dict)
  final_standings_df.index.name = "Season Final Standings: Year 20" + str(year)
  print(final_standings_df)

    







