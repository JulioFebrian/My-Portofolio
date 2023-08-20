DROP TABLE IF EXISTS players;
DROP TABLE IF EXISTS teams;
DROP TABLE IF EXISTS cities;
DROP TABLE IF EXISTS played_for;

CREATE TABLE cities(
	id	 SERIAL PRIMARY KEY,
	name TEXT NOT NULL DEFAULT ''
);

INSERT INTO cities(id, name) VALUES
  (1, 'Los Angeles'),
  (2, 'Orlando');

CREATE TABLE teams(
	id	 	 SERIAL PRIMARY KEY,
	name 	 TEXT NOT NULL DEFAULT '',
	city_id	 INTEGER NOT NULL
);

INSERT INTO teams(id, name, city_id) VALUES
  (1, 'Lakers', 1),
  (2, 'Clippers', 1),
  (3, 'Magic', 2);

CREATE TABLE players(
	id	 SERIAL PRIMARY KEY,
	name TEXT NOT NULL DEFAULT ''
);

INSERT INTO players(id, name) VALUES
  (1, 'Kobe Bryant'),
  (2, 'Shaquille O''Neal');

CREATE TABLE played_for(
	id	       SERIAL PRIMARY KEY,
	player_id  INTEGER NOT NULL,
	team_id	   INTEGER NOT NULL,
	start_year INTEGER NOT NULL,
	end_year   INTEGER NOT NULL
);

INSERT INTO played_for(id, player_id, team_id, start_year, end_year) VALUES
  (1,1,1,1996,2016),
  (2,2,2,1992,1996),
  (3,2,1,1996,2004);

-- SELECT * FROM players;
--
-- SELECT players.name,
--        played_for.start_year,
-- 	     played_for.end_year,
-- 	     end_year - start_year AS tenure
--   FROM players
--    INNER JOIN played_for ON players.id=played_for.player_id
--    INNER JOIN teams      ON played_for.team_id=teams.id
--    INNER JOIN cities     ON teams.city_id=cities.id
--   WHERE end_year - start_year >= 20
--     AND cities.name = 'Los Angeles'

--- AGGREGATION QUERIES
-- SELECT players.name, 
--        COUNT(*) - 1 AS num_trades
--   FROM players 
--   INNER JOIN played_for 
--     ON played_for.player_id = players.id
--  GROUP BY players.id