DROP TABLE IF EXISTS coffees;

CREATE TABLE coffees(
	id SERIAL PRIMARY KEY,
	name TEXT,
	hot BOOLEAN,
	cost DECIMAL,
	season TEXT
);

INSERT INTO coffees(name, hot, cost, season) 
	VALUES ( 'Drip', true, 4, 'all year'),
	 	   ('Pour Over', true,6,'all year'),
		   ('Iced', false, 8, 'all year'),
		   ('Orange Mocha Frappuccino', false, 5, 'all year'),
		   ('gingerbread latte', true, 10, 'winter'),
		   ('peppermint frappuccino', false, 12, 'winter'),
		   ('pumpkin spice latte', true, 13, 'fall');

SELECT COUNT(*) AS menu_size FROM coffees;
SELECT AVG(cost) AS avg_cost FROM coffees;

SELECT hot,
	   AVG(cost) AS avg_cost
  FROM coffees 
  GROUP BY hot;
  
SELECT season,
	   AVG(cost) AS avg_cost
  FROM coffees 
  GROUP BY season;
  
SELECT season,
	   AVG(cost) AS avg_cost,
	   COUNT(*) AS num_drinks
  FROM coffees 
  GROUP BY season;

--- What if I take out GROUP BY
-- SELECT season,
-- 	   AVG(cost) AS avg_cost,
-- 	   COUNT(*) AS num_drinks
--   FROM coffees 
-- ERROR on this one

SELECT season,
	   hot,
	   AVG(cost) AS avg_cost,
	   COUNT(*) AS num_drinks
  FROM coffees 
  GROUP BY season, hot;
  
-- SELECT season,
-- 	   hot,
-- 	   AVG(cost) AS avg_cost,
-- 	   COUNT(*) AS num_drinks,
-- 	   STRING_AGG(name, ', ') AS drinks
--   FROM coffees 
--   ;

SELECT season,
	   hot,
	   AVG(cost) AS avg_cost,
	   COUNT(*) AS num_drinks,
	   JSON_AGG(name) AS drinks
  FROM coffees 
  GROUP BY season, hot
  HAVING season='winter';

