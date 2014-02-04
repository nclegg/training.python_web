restaurantQuest.py


This program finds local resaurants within 1 mile of a supplied address, and reports their distance, seating capacity, and how well they faired in the last health inspection.

To run the program:
    1. Use virtualenv and set up an environment.
    2. Activate the environment.
    2. Install the requests package in the environment.
    3. Obtain a MapQuest api_key from http://developer.mapquest.com/
          (the 'Join Now' button is at the bottom of the page)
    4. Type:   python restaurantQuest.py
    5. The program will return a list of some restaurants within 1 mile
       of Dahl Field, Wedgwood. Alter the address variable in 'main'
       for different results.


The program uses a MapQuest API that exposes a radius search. Restaurants within a radius of 1 mile of the provided address are returned in json format. The restaurants are then matched with the appropriate information from the King County Health Department inspection database:
https://data.kingcounty.gov/dataset/Food-Establishment-Inspection-Data/f29f-zza5

The key used to match the data was the business address. There is no simple key for the two databases. Business names and even addresses are recorded differently. Longitude and latitude would have been a better key, but the number of digits is different between the two resources (6 vs 10). Neither rounding nor truncating the numbers at 4 digits (about 11m?) resolved the problem. Only about 1/3 of all possible entries are captured. 
 

Example output:
Distance		Restaurant	Seating	InspectionDate	InspectionResult	ViolationCode
0.54 mile	I LOVE BENTO	13-50	2013-07-25	Satisfactory	None
0.82 mile	FIDDLER'S INN	51-150	2013-06-18	Satisfactory	4300 - Non-food contact surfaces maintained and clean
0.76 mile	CREPE CAFE & WINE BAR	13-50	2013-10-15	Not Accessible	None
0.92 mile	MAPLE LEAF GRILL	13-50	2013-10-09	Satisfactory	4200 - Food-contact surfaces maintained, clean, sanitized
0.75 mile	DA PINO	0-12	2013-10-15	Not Accessible	None
0.52 mile	COOPER'S ALEHOUSE	51-150	2013-08-06	Not Accessible	None
0.78 mile	DIVINE	13-50	2013-08-28	Unsatisfactory	3700 - In-use utensils properly stored
0.57 mile	SUBWAY	51-150	2014-01-06	Unsatisfactory	4300 - Non-food contact surfaces maintained and clean
0.76 mile	BAGEL OASIS	13-50	2013-10-15	Satisfactory	None
0.61 mile	CHIANG GOURMET RESTAURANT	51-150	2013-10-23	Unsatisfactory	4800 - Physical facilities properly installed,...

###########################################
