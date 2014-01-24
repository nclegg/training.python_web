#!/usr/bin/env python

import operator
import sys
from json import load

import requests


def mapquest_radius_url(mq_key, postal_address, search_code, radius=1): 
    '''Returns a radius search url for a fixed distance around an
       address.
    '''

    service = "http://www.mapquestapi.com/search/v2/radius"

    # make url with fixed radius search of 1 mile; and 100 listings
    # requests and urllib.urlencode introduce errors in the key & hostedData
    # strings
    parameters = ["key=%s" % mq_key,
                  "origin=%s" % postal_address,
                  "hostedData=mqap.ntpois|group_sic_code=?|%s" % search_code,
                  "radius=%i" % radius,
                  "maxMatches=100"]
    return service + "?" + '&'.join(parameters)


def mapquest_nearby_restaurants(found_results):
    '''Return a dict of restaurants found using the MapQuest API.

       Returns dictionary[address][restaurant|distance]
    '''

    restaurants = {}
    for result in found_results:
        address = result['fields']['address'].upper()
        restaurants[address] = {'name': result['name'].upper(),
                                #'latitude': result['fields']['lat'],
                                #'longitude': result['fields']['lng'],
                               'zip_code': result['fields']['postal_code'],
                               'distance': str(result['distance']) + ' mile' }
    return restaurants


def recent_restaurant_inspection(restaurants):
    '''Yield a dict of information about the most recent health
       inspection of a restaurant.

       The function receives a list of dicts and yields an anonymous
       dict containing a 'name' key that identifies the restaurant.
    '''

    restaurants.sort(key=operator.itemgetter('name', 'inspection_date'),
                     reverse=True)

    name = restaurants[0]['name']
    inspections = []

    for restaurant in restaurants:
        if restaurant['name'] == name:
            inspections.append(restaurant)
        else:
            yield inspections[0]
            name = restaurant['name']
            inspections = [restaurant]


def seating_capacity(restaurant):
    if restaurant['description'].startswith("Seating"):
        seats = restaurant['description'].split()[1]
    else:
        seats = "unknown"
    return seats


def print_restaurant_summary(local_restaurants, inspections):
    '''Match up and print local restaurants with inspections.'''

    print "\t".join(['Distance', '', 'Restaurant', 
                     'Seating', 'InspectionDate',
                     'InspectionResult', 'ViolationCode'])

    # get the most recent inspection for each nearby restaurant
    for restaurant in recent_restaurant_inspection(inspections):
        address = restaurant['address'].rstrip()
        if address in local_restaurants:
            seating = seating_capacity(restaurant)
            print '\t'.join([local_restaurants[address]['distance'],
                             restaurant['name'], '', 
                             seating,
                             restaurant['inspection_date'].split('T')[0],
                             restaurant['inspection_result'],
                             restaurant.get('violation_description', "None")])


def main():

    ## MapQuest ##

    api_key = ""

    if not api_key:
        print "An api_key is needed for this program."
        sys.exit()


    address = "7700 25th Ave NE, Seattle, WA, 98115"  # Dahl Field Park
    #address = "1100 Fairview Ave N, Seattle, WA, 98109" # FHCRC

    restaurant_code='581208'
    restaurant_url = mapquest_radius_url(api_key, address, restaurant_code) 

    mq_response = requests.get(restaurant_url, params={})
    mq_response.raise_for_status()

    search_results = mq_response.json()['searchResults'] # lod
    nearby_restaurants = mapquest_nearby_restaurants(search_results)

    # just choose one postal code
    zip_code = {nearby_restaurants[x]['zip_code'] 
                for x in nearby_restaurants}.pop()

        
    ## KingCounty ##

    hostname = "http://data.kingcounty.gov/resource/f29f-zza5.json"
    parameters = { 'zip_code' : zip_code,
                   'inspection_type' : 'Routine Inspection/Field Review' }

    kc_response = requests.get(hostname, params=parameters)
    kc_response.raise_for_status()
    inspections = kc_response.json()  # all inspections within the zip_code

    ## Mashup ##

    print_restaurant_summary(nearby_restaurants, inspections)

if __name__ == '__main__':

    main()
