# Swiss Tournament

  This program sets up a database to track a SwissPairing style tournament. It tracks registering an even number of players and records the wins and matches as the tournament progresses.

### Installation

  * Install [PYTHON 2.7.x](https://www.python.org/downloads/) for your specific operating system
  * Install [Git Bash](https://openhatch.org/missions/windows-setup/install-git-bash)
  * Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
  * Install [Vagrant](https://www.vagrantup.com/downloads.html)
  * Open Git Bash and enter the following command
  ```
  $ git clone https://github.com/bm8839/Swiss_Tournament
  ```

### Usage

  How to run:
  Navigate to the vagrant directory and start the
  Vagrant VM. After vagrant is up and running log into it and navigate to the tournament directory.
  You should see 3 files: tournament.sql (sets up the relational database schema using psql server), tournament_test.py (python file written to test the functions of the program), and tournament.py (python file containing the
  functions that track the tournment)

  Once in the tournament directory start the psql server as follows:

  vagrant@vagrant-ubuntu-trusty-32:/vagrant/tournament$ psql

  Create the tournament database and table by executing the tournament.sql file
  as follows:

  vagrant=> \i tournament.sql


  Disconnect from the tournament database as follows:

  tournament=> \q


  Execute the tournament_test file as follows:

  vagrant@vagrant-ubuntu-trusty-32:/vagrant/tournament$ python tournament_test.py


### Design and Implementation
  The database contains two tables. Table named
  players has two columns (id and player_name). Table named matches has three columns (id, winner, and loser). When a player is registered their name is placed into the players table and the players.id is serially assigned by the
  system. The winner's player.id and loser's player.id of each match is recorded in the matches table.

### License
  Swiss Tournament is released under the [MIT License](https://github.com/bm8839/Swiss_Tournament/blob/master/License.txt)