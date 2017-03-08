#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
from contextlib import contextmanager


@contextmanager
def db_helper():
    """
    Database helper function using context lib. Creates a cursor from a
    database connection object, yields that cursor to the other functions to
    perform queries and then cleans up making the commits and closures.
    """
    db = connect()
    c = db.cursor()
    try:
        yield c
    except:
        raise
    else:
        db.commit()
    finally:
        c.close()
        db.close()


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        return psycopg2.connect("dbname='tournament'")
    except:
        print ("Connection failed")


def deleteMatches():
    """Removes all the match records from the database."""

    with db_helper() as c:
        c.execute("TRUNCATE matches")


def deletePlayers():
    """Removes all the player records from the database."""

    with db_helper() as c:
        c.execute("TRUNCATE players CASCADE")


def countPlayers():
    """Returns the number of players currently registered."""

    with db_helper() as c:
        c.execute("SELECT count (*) FROM players")
        return c.fetchone()[0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """

    with db_helper() as c:
        query1 = "INSERT INTO players (player_name) VALUES (%s);"
        data = (name,)
        c.execute(query1, data)


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list will be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    with db_helper() as c:
        c.execute(
            """SELECT players.id, players.player_name, count(matches.winner)as wins,
                 (SELECT count(*) FROM matches
                 WHERE matches.loser = players.id
                 OR matches.winner = players.id) as matches
               FROM players LEFT JOIN matches
               ON players.id = matches.winner
               GROUP BY players.id
               ORDER BY wins DESC
               """)
        rows = c.fetchall()
    player_standings = []
    for row in rows:
        player_standings.append(row)

    return player_standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    with db_helper() as c:
        query = "INSERT INTO matches (winner, loser) VALUES (%s, %s);"
        winner_id = (winner,)
        loser_id = (loser,)
        c.execute(query, (winner_id, loser_id))


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

    players_id_name = []
    players = playerStandings()
    for row in players:
        player_id_name = (row[0], row[1])
        players_id_name.append(player_id_name)
    pairings = []
    index = 0
    while index < len(players_id_name):
        pairings.append(players_id_name[index] + players_id_name[index+1])
        index += 2

    return pairings
