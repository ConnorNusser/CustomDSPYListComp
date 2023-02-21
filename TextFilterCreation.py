import random
import time
import csv 
ipSet = set()
ipArr = []
start_time = time.time()

# Generates the initial number of ips
for i in range(2 * 10 ** 5):
  ip = '{}.{}.{}.{}'.format(*__import__('random').sample(range(0,255),4))
  request_HandlerString = 'request_handle("%s")' % ip
  if request_HandlerString in ipSet:
    continue
  ipSet.add(request_HandlerString)
  ipArr.append(request_HandlerString)
  
endArr = []
# this then cycles through the same list to mimic people going to the same site every day
for i in range(10 ** 6):
    random_element = random.randrange(0, len(ipArr))
    top100_flag = random.randrange(0, 100)
    #top 100 is thrown in the request List randomly with a 1 in a 100 chance
    if top100_flag == 99:
        endArr.append("top100()")
    endArr.append(ipArr[random_element])

knownipOne = 'request_handle("10.20.40.60")'
knownipTwo = 'request_handle("5.10.15.20")'
knownipThree = 'request_handle("00.00.11.20")'


for i in range(225):
    endArr.append(knownipOne)
for i in range(360):
    endArr.append(knownipTwo)    
for i in range(90):
    endArr.append(knownipThree)
random.shuffle(endArr)

    
    
with open("txtFile.csv", mode="w") as file:

    # create a CSV writer object
    writer = csv.writer(file)

    # write each item in the list as a new row in the CSV file
    for item in endArr:
        writer.writerow([item])
 
print("--- %s seconds ---" % (time.time() - start_time))
    

    

