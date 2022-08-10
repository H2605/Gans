import json
import requests
import pymysql
import pandas as pd
import datetime
import keys
from keys import *


  
def temps(city, country):
    temps_city = []
    response = requests.get(f'http://api.openweathermap.org/data/2.5/forecast/?q='+city+','+country+'&appid='owmkey')
    response_city = response.json()["list"]
    for i in response_city:
        temps_dict={}
        
        temps_dict["weather"]=i["weather"][0]["description"]
        temps_dict['temparature'] = i['main']["temp"]
        temps_dict['feels_like'] = i['main']["feels_like"]
        temps_dict['humidity'] = i['main']["humidity"]
        temps_dict["timestamp"]= i["dt_txt"]
        temps_dict['windspeed']=i["wind"]["speed"]
        temps_dict['municipality_iso_country']=city+","+country
        #temps_dict["municipality_iso_country"]=np.where(city cities["city_ascii"]==,cities["municipality_iso_country"], "AAA" )
        temps_city.append(temps_dict)
        df_city_temp=pd.DataFrame(temps_city)
        #city_forecast=df_city_temp.merge(cities, how="left", left_on="city", right_on="city_ascii"
        df_city_temp["timestamp"]=pd.to_datetime(df_city_temp["timestamp"])
    return df_city_temp
    
    
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
    cursor.execute("DROP TABLE IF EXISTS weather")

    #response = requests.request("GET", url, headers=headers, params=querystring)
    #arrivals_berlin = response.json()['arrivals']
    #arrivals_berlin = pd.DataFrame([get_flight_info(flight, airport_icoa) for flight in arrivals_berlin])
    
    
    
    # Weather api
    city = "Stuttgart"
    country = "DE"
    weather=temps(city, country)

    # flights api
#    iata="BER"
#    arrivals_berlin=arflights8to19(iata)
    
    weather.to_sql('weather', if_exists='append', con=con, index=False)
