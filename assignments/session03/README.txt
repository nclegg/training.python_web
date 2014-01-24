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

The key used to match the data was the business address. There is no simple key for the two databases. Business names and even addresses are recorded differently. Longitude and latitude would have been a better key, but the number of digits is different between the two resources (6 vs 10) and the truncating/rounding rules are not obvious. 
 
