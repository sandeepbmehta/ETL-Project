from bs4 import BeautifulSoup
from splinter import Browser
import requests
import pymongo
import pandas as pd
import time
from sqlalchemy import create_engine
import pymysql
pymysql.install_as_MySQLdb()
from userpasswd import username, passwd
from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo

# Create an instance of Flask
app = Flask(__name__)

# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
# Define database and collection
db = client.soccer_db

#players = db.players_info.find()
player_info_df1 = pd.DataFrame(list(db.players_info.find()))
#player_info_df1.head()

player_info_df = player_info_df1[["name", "player_info", "full_image_url"]]
#player_info_df.head()

con_string = f'{username}:{passwd}@127.0.0.1:3306/soccer_players'
conn_string = con_string
engine = create_engine(f'mysql://{conn_string}')
conn = engine.connect()

# Route to render index.html template using data from Mongo
@app.route("/")
def welcome():
    return (
        f"Welcome - Enter player name after the /<br/>"
    )

# Route that will trigger the scrape function
@app.route("/<player_name>")
def display_data(player_name):
    #print(player_name)
    player_data_df = pd.read_sql('select * from player_data', con=engine)
    #print('test 1')
    player_data_df["Select"] = player_data_df["name"].str.contains(player_name, case=False, regex=False)
    #print('test 2')
    player_data_df = player_data_df.loc[player_data_df["Select"] == True, :]
    #print(player_data_df.head())
    # Merge the columns
    comb_df = pd.merge(player_data_df, player_info_df, on="name", how="inner")
    #print('DataFrame')
    #print(comb_df)
    if comb_df.index.empty:
        return jsonify({"error": f"Unable to find {player_name} try a different name"}), 404

    comb_dict = comb_df.to_dict('records')
    #print('List of Dictionary')
    #print(comb_dict)

    return render_template("player-page.html", player_data=comb_dict)
    

if __name__ == "__main__":
    app.run(debug=True)
