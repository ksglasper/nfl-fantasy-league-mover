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

total_head2head = {"Kyle" : [],
                   "Aaditya" : [],
                   "Matt T" : [],
                   "Matt" : [],
                   "Webster" : [],
                   "Nolan" : [],
                   "Arjun" : [],
                   "Ignacio" : [],
                   "Harsha" : [],
                   "Andrew" : [],
                   "Dominic" : [],
                   "Previn" : [],
                   "Matt Z" : [],
                   "Stanley" : [],
                   "Henry" : [],
                   "Ed" : []
                   }

######################## This section scrapes all drafting data by year ########################
for year in range(14, 24):
  print("Entering year 20" + str(year) + " ...")
  ## Get an updated dictionary of the year's owners and real name ##
  manager_names = "https://fantasy.nfl.com/league/2338570/history/20" + str(year) + "/owners"
  manager_web_response = requests.get(manager_names)
  manager_page = BeautifulSoup(manager_web_response.content, "html.parser")

  team_names_by_season = manager_page.find_all("a", class_="teamName")
  user_names_by_season = manager_page.find_all("td", class_="teamOwnerName")
  user_moves = manager_page.find_all("td", class_="teamTransactionCount numeric")
  user_trades = manager_page.find_all("td", class_="teamTradeCount numeric")

  season_team_name_master_list = []
  season_username_master_list = []
  moves = []
  trades = []
  cycle_count = 0
  alias = ["Xochimilco Axolotls", "West Loop Wyverns", "Toronto Angels", "Parry Sound Dragons", "Barrie Dragons" ]

  for manager in team_names_by_season:
    season_team_name_master_list.append(manager.get_text())
    name = user_names_by_season[cycle_count].get_text().strip()
    if name == "Jim":
      name = "Matt T"
    if string_in_list(alias, manager.get_text()):
       name = "Matt Z"
    season_username_master_list.append(name)
    moves.append(int(user_moves[cycle_count].get_text()))
    trades.append(int(user_trades[cycle_count].get_text()))
    cycle_count +=1

  team_to_player_dict = dict(zip(season_team_name_master_list, season_username_master_list))

  ## Create DataFrame with Player, Moves, and Trades by year ##
  move_trade_dict = {"Name" : season_username_master_list, "Moves" : moves, "Trades" : trades}
  name_moves_trade_df = pd.DataFrame.from_dict(move_trade_dict)
  name_moves_trade_df.index.name = "Season Transactions: Year 20" + str(year)
  # print(name_moves_trade_df)




  league_link = "https://fantasy.nfl.com/league/2338570/history/20" + str(year) + "/draftresults?draftResultsDetail=0&draftResultsTab=round&draftResultsType=results"
  
  nfl_webpage_response = requests.get(league_link)
  nfl_page = nfl_webpage_response.content
  nfl_soup = BeautifulSoup(nfl_page, "html.parser")

  nfl_draft_order = nfl_soup.find_all(attrs={"class": "count"})
  nfl_draft_players = nfl_soup.find_all(attrs={"class": "playerName"})
  draft_team_name_bs = nfl_soup.find_all("a", class_="teamName")
  nfl_draft_auction_for = nfl_soup.find_all("span", class_="auctionCost")

  draft_order = []
  auction_amount = []
  player_names = []
  draft_team_names = []
  cycle_count = 0

  for order in nfl_draft_order:
    order_to_number = order.get_text().split('.')[0]
    draft_order.append(int(order_to_number))
    player_names.append(nfl_draft_players[cycle_count].get_text())
    draft_team_names.append(team_to_player_dict.get(draft_team_name_bs[cycle_count].get_text()))
    cycle_count += 1
  
  cycle_count = 0

  for price in nfl_draft_auction_for:
    auction_to_number = (nfl_draft_auction_for[cycle_count].get_text()).split('$')[1]
    auction_amount.append(int(auction_to_number))

  if len(auction_amount) > 0:
    draft_2014_dict = {"Draft Number" : draft_order, "Player Name" : player_names, "Auction Amount": auction_amount, "Team Name": draft_team_names }
    draft_2014 = pd.DataFrame.from_dict(draft_2014_dict)
    draft_2014.index.name = "Auction Draft Results: Year 20" + str(year)
  else:
    draft_2014_dict = {"Draft Number" : draft_order, "Player Name" : player_names, "Team Name": draft_team_names }
    draft_2014 = pd.DataFrame.from_dict(draft_2014_dict)
    draft_2014.index.name = "Snake Draft Results: Year 20" + str(year)
  # print(draft_2014)

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
  # print(standings_df)

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
  # print(final_standings_df)

######################## This section scrapes all H2H data including win/loss, points for/against, and win pecentage against each player for the year data by year ########################
  reg_season = 14
  if(year >= 19 and year < 21):
    reg_season = 12
  elif year >= 21:
    reg_season = 13
  ## Get the Win/Loss Records, Points for/against, and regular season standings from Standings Page ##
  for team_num in range(1, len(season_username_master_list) + 1):
    league_link_head2head = "https://fantasy.nfl.com/league/2338570/history/20" + str(year) + "/schedule?standingsTab=schedule&scheduleType=team&leagueId=2338570&scheduleDetail=" + str(team_num)

    nfl_webpage_response_head2head = requests.get(league_link_head2head)
    nfl_soup_head2head = BeautifulSoup(nfl_webpage_response_head2head.content, "html.parser")

    ## Build opponent list, win/loss, and points
    yearly_head2head = {}

    ## This doesn't work because it assigns all member the same referenced dictionary and they all update together
    # week_opponent_stats_dict = {
    #   "Win" : 0,
    #   "Loss" : 0,
    #   "pf" : 0,
    #   "pa" : 0
    # }
    head2head_team = nfl_soup_head2head.find_all("h2", class_="teamName")
    head2head_opponent = nfl_soup_head2head.find_all("div", class_="teamImageAndNameWrap")
    head2head_wins_and_losses = nfl_soup_head2head.find_all("em", class_="resultText")
    head2head_points_for = nfl_soup_head2head.find_all("em", class_="teamTotal")

    opponent = []
    wins = []
    percent_WL = []
    points_for = []
    points_against = []
    reg_season_stats_name = team_to_player_dict.get(head2head_team[0].get_text().strip())



    for week in range(reg_season):

      weekOpponent = team_to_player_dict.get(head2head_opponent[week].get_text().strip())
      if yearly_head2head.get(weekOpponent) == None:
        yearly_head2head.update({weekOpponent : {
        "Win" : 0,
        "Loss" : 0,
        "pf" : 0,
        "pa" : 0
        }})
      
      yearly_head2head[weekOpponent][head2head_wins_and_losses[week].get_text()] += 1
      yearly_head2head[weekOpponent]["pf"] = round((yearly_head2head[weekOpponent]["pf"] + float(head2head_points_for[week * 2].get_text())), 2)
      yearly_head2head[weekOpponent]["pa"] = round((yearly_head2head[weekOpponent]["pa"] + float(head2head_points_for[week * 2 + 1].get_text())), 2)
    # print(yearly_head2head)
    total_head2head[reg_season_stats_name].append({"20" + str(year) : yearly_head2head})
  print("Exiting year 20" + str(year) + " ...")
  
# print(total_head2head["Kyle"])
def gather_total_stats(name):
  # index = 0
  stat_builder = {}
  for year in total_head2head[name]:
    for year_obj in year:
      for opponent in year[year_obj]:
        if stat_builder.get(opponent) == None:
          stat_builder[opponent] = {
          "Win" : year[year_obj][opponent]["Win"],
          "Loss" : year[year_obj][opponent]["Loss"],
          "pf" : year[year_obj][opponent]["pf"],
          "pa" : year[year_obj][opponent]["pa"]
          }
          continue
        stat_builder[opponent]["Win"] += year[year_obj][opponent]["Win"]
        stat_builder[opponent]["Loss"] += year[year_obj][opponent]["Loss"]
        stat_builder[opponent]["pf"] = round(stat_builder[opponent]["pf"] + year[year_obj][opponent]["pf"], 2)
        stat_builder[opponent]["pa"] = round(stat_builder[opponent]["pa"] + year[year_obj][opponent]["pa"], 2)
  return stat_builder
print(gather_total_stats("Kyle"))




    

        # "Win" : total_head2head[name][index][year][opponent]["Win"],
    







