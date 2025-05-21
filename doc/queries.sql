-- Electric vehicles registered per model year

SELECT model_year AS "Model Year", COUNT(*) AS "Number of electric vehicles registered"
FROM electric_vehicles
GROUP BY model_year;

-- Top 10 electric vehicle models by registration count

SELECT model AS "Model", COUNT(*) AS "Registration count"
FROM electric_vehicles
GROUP BY model
ORDER BY COUNT(*) DESC
LIMIT 10;

-- CAFV-eligible electric vehicles by state and county

SELECT state AS "State", county AS "County", COUNT(*) AS "Number of CAFV-eligible vehicles"
FROM electric_vehicles
WHERE clean_fuel_vehicle_eligibility = 'Clean Alternative Fuel Vehicle Eligible'
GROUP BY state, county
ORDER BY COUNT(*) DESC;

-- year-over-year change in electric vehicle registrations by county

SELECT 
	county, 
	model_year, 
	COUNT(*) AS "Vehicle registrations",
	LAG(COUNT(*)) OVER (PARTITION BY county ORDER BY model_year) AS "Previous year registrations",
	COUNT(*) - LAG(COUNT(*)) OVER (PARTITION BY county ORDER BY model_year) AS "Year-over-year change"
FROM electric_vehicles
GROUP BY county, model_year
ORDER BY county ASC;
