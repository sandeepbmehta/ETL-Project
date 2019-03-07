DROP DATABASE IF EXISTS soccer_players;

CREATE DATABASE soccer_players;

use soccer_players;

CREATE TABLE player_data (
  id int,
  name VARCHAR(30) NOT NULL,
  club varchar(30),
  age INT,
  mkt_value float,
  nationality varchar(30)
);