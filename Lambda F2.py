import json
import requests
import pandas as pd
import numpy as np
import pymysql
import datetime

def arflights8to19(iata):
    
    tommorrow=datetime.date.today()+ datetime.timedelta(days=1)
    tomrowstr=str(tommorrow)
    tomrowstr
    url_1 = "https://aerodatabox.p.rapidapi.com/airports/iata/"+iata+""

    headers = {
        "X-RapidAPI-Key": aerodatabox_key,
        "X-RapidAPI-Host": "aerodatabox.p.rapidapi.com"
    }

    response_1 = requests.request("GET", url_1, headers=headers)
    icaoc=response_1.json()["icao"]
    
    json_object=response_1.json()["icao"]
    
    url = "https://aerodatabox.p.rapidapi.com/flights/airports/icao/"+icaoc+"/"+tomrowstr+"T08:00/"+tomrowstr+"T19:00"

    querystring = {"withLeg":"true","withCancelled":"true","withCodeshared":"true","withCargo":"true","withPrivate":"true","withLocation":"false"}

    headers = {
        "X-RapidAPI-Key": aerodatabox_key,
        "X-RapidAPI-Host": "aerodatabox.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    data=response.json()["arrivals"]
    #print(response.text)
    flights=[]
    
    for i in data:
        flights_dic={}
        if "airport" in i["departure"].keys():#departure from
            flights_dic["departure_from"]=i["departure"]["airport"]["name"]
        else:
            flights_dic["departure_from"]="unknown"
        if "scheduledTimeLocal" in i["departure"].keys():
            flights_dic["departure_time"]=i["departure"]["scheduledTimeLocal"]#departure time local
        else:
            flights_dic["departure_time"]="unknown"
            
        if "scheduledTimeLocal" in i["arrival"].keys():
            flights_dic["arrival_time"]=i["arrival"]["scheduledTimeLocal"]#arrival time local
        else:
            flights_dic["arrival_time"]="unknown"
            
        if "number" in i.keys():
            flights_dic["flight_number"]=i["number"] #flight number
        else:
            flights_dic["flight_number"]="unknown"
            
        if "terminal" in i["arrival"].keys():#departure from
            flights_dic["terminal"]=i["arrival"]["terminal"]+
        else:
            flights_dic["terminal"]="unknown"
            
        if "airline" in i.keys():
            flights_dic["airline"]=i["airline"]["name"] #airline
        else:
            flights_dic["airline"]="unknown"
            
        if "aircraft" in i.keys(): #aicraft
            flights_dic["aircraft"]=i["aircraft"]["model"]
        else:
            flights_dic["aircraft"]="unknown"
        if "icao" in i["departure"]["airport"].keys():
            flights_dic["ICAO"]=i["departure"]["airport"]["icao"]  #icao
        else:
            flights_dic["ICAO"]="unknown"

        if "iata" in i["departure"]["airport"].keys():
            flights_dic["IATA"]=i["departure"]["airport"]["iata"] #iata
        else:
            flights_dic["IATA"]="unknown"

        flights.append(flights_dic)
        df_flights=pd.DataFrame(flights)
        df_flights["departure_time"]=df_flights["departure_time"].str.extract("(\d\d\d\d-\d\d-\d\d \d\d:\d\d)")
        df_flights["arrival_time"]=df_flights["arrival_time"].str.extract("(\d\d\d\d-\d\d-\d\d \d\d:\d\d)")
        df_flights["departure_time"]=pd.to_datetime(df_flights["departure_time"])
        df_flights["arrival_time"]=pd.to_datetime(df_flights["arrival_time"])
        df_flights = df_flights[df_flights["ICAO"] != "unknown"]
    return df_flights
    
    
def lambda_handler(event, context):
    schema="gans"
    host=rds_host
    user="admin" #MAYBE ROOT
    password=rds_pw
    port=3306
    con = f'mysql+pymysql://{user}:{password}@{host}:{port}/{schema}'
    

    conn = pymysql.connect(
    user='admin', password='roooooot', host='wbs-project3-db.c9gjvnfsb3gv.eu-west-2.rds.amazonaws.com', database='gans')
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS arrivals")


    # flights api
    #iata="BER"
    arrivals_berlin=arflights8to19("BER")
    
    #weather.to_sql('weather', if_exists='append', con=con, index=False)
    arrivals_berlin.to_sql('arrivals', if_exists='append', con=con, index=False)
