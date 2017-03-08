-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
--
-- This file creates a database named "tournament" and then connects to that
-- database and creates two tables with names "players" and "matches". This file
-- needs to be executed once from the vagrant prompt after launching the psql
-- server, for example:
-- vagrant@vagrant-ubuntu-trusty-32:/vagrant/tournament$ psql
-- and then at the prompt vagrant=> \i tournament.sql
-- After this file is executed, disconnect from the tournament database and
-- run the tournament_test python file.



DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

\c tournament;

CREATE TABLE players (id serial primary key, 
                      player_name text);

CREATE TABLE matches (id serial primary key,
                      winner int REFERENCES players(id),
                      loser int REFERENCES players(id));

