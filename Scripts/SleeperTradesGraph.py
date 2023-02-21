#!python3
"""The purpose of this script is to graph out the number of trades each of your Sleeper leaguemates have made
for a season and plot visualize them"""

# imports
import requests
import pandas as pd
import json
import matplotlib.pyplot as plt

# Get the users Sleeper League ID. This is found in the URL of the individual league on sleeper.app or in the settings of the sleeper mobile app
league_id = input('Enter your league ID: ')

# Get league info using the league ID above
response = requests.get(f'https://api.sleeper.app/v1/league/{league_id}')
league_info = response.json() 

# Get all of the users in the league
response = requests.get(f'https://api.sleeper.app/v1/league/{league_id}/users')
league_users = response.json()

# Get all rosters in the league
response = requests.get(f'https://api.sleeper.app/v1/league/{league_id}/rosters')
league_rosters = response.json()

# Transactions in the league are saved by the week in the sleeper API, looks like week 1 includes pre-season trades so we just go through weeks 1-18 to find
# all transactions and put them in a list called 'all_transactions'
all_transactions = []

for i in range(1, 18):
    response = requests.get(f'https://api.sleeper.app/v1/league/{league_id}/transactions/{i}')
    league_transactions = response.json()
    for j, k in enumerate(league_transactions):
        all_transactions.append(k)

# All transactions includes free agent/waive claims, filtering the list so we only see trades
only_trades = []

for i, j in enumerate(all_transactions):
    if all_transactions[i]['type'] == 'trade':
        only_trades.append(j)
        
# Making a list that will have the owner's identifier, their roster id, and a trade counter that we'll increment whenever we see them involved in a trade
new_dict = []

for i, j in enumerate(league_rosters):
    new_dict += [{'display_name':league_rosters[i]['owner_id'], 'roster_id':league_rosters[i]['roster_id'], 'trade_counter': 0}]
    
# Gonna replace their owner ID with their actual display name
for i, j in enumerate(new_dict):
    for k, l in enumerate(league_users):
        if new_dict[i]['display_name'] == league_users[k]['user_id']:
            new_dict[i]['display_name'] = league_users[k]['display_name']
            
# Now we cycle through the list of trades and just increment each user's trade counter by 1 whenever they're involved in a trade
for i, j in enumerate(only_trades):
    for k, l in enumerate(new_dict):
        for o, p in enumerate(only_trades[i]['roster_ids']):
            if new_dict[k]['roster_id'] == only_trades[i]['roster_ids'][o]:
                new_dict[k]['trade_counter'] += 1
                
# Save all of our data to a pandas dataframe
df = pd.DataFrame(new_dict)

# Renaming the display name column to use as our x axis label
df.rename(columns={'display_name': 'Manager'}, inplace=True)
df = df.set_index('Manager')

# Sort least trades to most trades
df_sorted = df.sort_values('trade_counter')

# Plotting the trades on a bar graph
df_sorted['trade_counter'].plot.bar(title='Trades per Manager', ylabel='Number of Trades')

plt.tight_layout()
plt.show()
