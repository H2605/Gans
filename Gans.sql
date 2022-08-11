drop database if exists  gans;
create database if not exists  gans;
use gans;
drop table if exists cities;
create table if not exists cities(
		city text,
		city_ascii varchar(200),
        latitude text,
        longitude text, 
        country text,
        iso2 text,
        iso3 text,
        admin_name text,
        capital text,
        population int,
        id varchar(200),
        municipality_iso_country varchar(200) collate utf8_bin
        ,primary key (municipality_iso_country)
        ,unique key (municipality_iso_country) 
        #,foreign key (municipality_iso_country) references exp.airports_cities(municipality_iso_country)
        );
drop table if exists weather;
create table if not exists weather(
		weather_id int auto_increment, 
        weather text,
        temparature float,
        feels_like float,
        humidity int,
        timestamp datetime,
        windspeed float,
        municipality_iso_country varchar(200) collate utf8_bin,
        primary key (weather_id) 
        ,foreign key (municipality_iso_country) references cities(municipality_iso_country)
        );

drop table if exists airport_cities;
create table if not exists airport_cities(
	name text, 
    type text,
    iso_country varchar(10), 
    iso_region varchar(10),    
    municipality text, 
    icao_code varchar(4), 
    iata_code varchar(6), 
    municipality_iso_country varchar(200) collate utf8_bin,
	latitude float, 
    longitude float 
    ,primary key(icao_code)
    ,foreign key (municipality_iso_country) references cities(municipality_iso_country)
);
select* from airport_cities;
       

drop table if exists arrivals; 
create table if not exists arrivals(
	arrivals_id int auto_increment 
    ,departure_from text 
    ,departure_time datetime 
    ,arrival_time datetime
    ,flight_number text
    ,terminal text
    ,airline text
	,aircraft text
    ,ICAO varchar(4)
    ,IATA varchar(6)
    ,primary key (arrivals_id)
    ,foreign key (ICAO) references airport_cities(icao_code)
);



select * from cities;
select * from airport_cities;
select * from arrivals;
select * from weather;



