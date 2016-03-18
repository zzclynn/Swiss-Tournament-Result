-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- creat and connect to the tournament if needed
CREATE DATABASE tournament;
\c tournament


/* The player table includes player id, player_name, player win 
records.
*/
DROP TABLE IF EXISTS player;
CREATE TABLE player (
	player_id		SERIAL	PRIMARY KEY,
	player_name		TEXT	NOT NULL,
	player_wins		INT		DEFAULT 0,
	player_matchs	INT		DEFAULT 0
);
