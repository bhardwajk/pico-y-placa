 This is a python utility to check if a vehicle with plate number is allowed to run on a particular date/time depending upon the Pica Y Placa rules
 
 Correct Input Format python pico_y_placa <plate_number> <date> <time> 
 Example: python pico_y_placa 'abcd 09 8890' '29-04-2017' '08:00PM'
 
 Program prints whether vehicle is allowed to run or not. 
 Current Restrictions (Mon to Fri) between 6AM to 8.30AM & 3PM to 7.30PM:
 Even digit cars on even days
 Odd digit cars on odd days
 No restrictions on other days or time (weekends)
