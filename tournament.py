#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    curs = conn.cursor()
    curs.execute("UPDATE player SET player_matchs = 0, player_wins = 0")
    conn.commit()
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    curs = conn.cursor()
    curs.execute("DELETE FROM player")
    conn.commit()
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    curs = conn.cursor()
    curs.execute("SELECT count(*) as num from player")
    num = curs.fetchone()[0]
    conn.close()
    return num

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """    
    conn = connect()
    curs = conn.cursor()
    curs.execute("INSERT INTO player (player_name) VALUES (%s)",(name,))
    conn.commit()
    conn.close()



def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    curs = conn.cursor()
    curs.execute("SELECT player_id, player_name, player_wins, player_matchs FROM \
        player ORDER BY player_wins DESC")
    table = curs.fetchall()
    conn.close()
    return table

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    curs = conn.cursor()
    curs.execute("UPDATE player SET player_matchs = player_matchs + 1, \
        player_wins = player_wins + 1 \
        WHERE player_id = (%s)", (winner,))
    curs.execute("UPDATE player SET player_matchs = player_matchs + 1 \
        WHERE player_id = (%s)", (loser,))
    conn.commit()
    conn.close()

 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    conn = connect()
    curs = conn.cursor()
    curs.execute("SELECT player_id, player_name FROM \
        player ORDER BY player_wins DESC")
    table = curs.fetchall()
    conn.close()
    result = []
    pair = []
    pair_flag = False
    for row in table:
        for i in range(2):
            pair.append(row[i])
    
        if pair_flag:
            result.append(pair)
            pair = []
        pair_flag = not pair_flag 
    return result



