import yaml

import random
DaysString = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
DaysCoef = [20,12,18,12,15,10,4]
Dates = ["2020-04-20","2020-04-21","2020-04-22","2020-04-23","2020-04-24","2020-04-25","2020-04-26"]
Hours = ["08-00-00","09-00-00","10-00-00","11-00-00","12-00-00","13-00-00","14-00-00","15-00-00","16-00-00","17-00-00","18-00-00","19-00-00"]
HoursCoef = [17,18,19,19,25,25,20,20,16,16,20,15]
ParkCoef = [15,50,35]
Parkinglots = []
#['08-00-00']*15 + ['10-00-00']*18 + ['12-00-00']*30 + ['14-00-00']*20 + ['16-00-00']*12 + ['18-00-00']*10 + ['20-00-00']*5
i=1
while(i<=113):
    Parkinglots.append(["M"+str(i), "Mid Car Park", "Available",None,None,None])
    i=i+1
i=1
while(i<=315):
    Parkinglots.append(["T"+str(i), "TM Car Park", "Available",None,None,None])
    i=i+1
i=1
while(i<=155):
    Parkinglots.append(["Y"+str(i), "YDB Car Park", "Available",None,None,None])
    i=i+1
#['Mid'] * 15 + ['YDB'] * 35 + ['TM'] * 50



dayCounter = 0
dumpsArray=[]
for day in DaysString:
    for hour in Hours:
        hourCounter = 0
        for park in Parkinglots:
            prob = 0
            prob += DaysCoef[dayCounter]
            prob += HoursCoef[hourCounter]
            if(park[0] == "M"):
                prob +=ParkCoef[0]
            elif(park[0] == "T"):
                prob += ParkCoef[1]
            else:
                prob += ParkCoef[2]

            temp = random.randint(1, 100)
            status = None

            if temp < prob :
                status = "Occupied"
            else:
                status = "Available"

            data = dict(
                ParkingLot=park[0],
                ParkingLotStatus=status,
                ParkZoneName=park[1],
                Date=Dates[dayCounter],
                Day=day,
                Hour=hour
            )
            dumpsArray.append(data)
        hourCounter = hourCounter + 1
    dayCounter = dayCounter + 1


print(dumpsArray)
with open('logYeni.yaml', 'w') as outfile:
    yaml.dump(dumpsArray, outfile, default_flow_style=False)
