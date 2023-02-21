# WithPulley Ip Address Mapping Project


## How to Run

```js
git clone https://github.com/ConnorNusser/withPulleyProj.git
```

### To Run Main Function
```js
cd withPulleyProj
Python3 withPulley.py
```
First method to generate requests is within 
```py
def main(argv):
    #Example
    request_handle("11.12.14")
```

The better option though is: 

### To Generate a massive list of randomly constructed ips
```py
Python3 TextFilterCreation.py
```
Note: top100() is randomly generated and thrown in with the inputs

Additionally you can add in specific values/different max ip values by manipulating the request handle string
within TextFilterCreation.py
```py
knownipOne = 'request_handle("10.20.40.60")'
knownipTwo = 'request_handle("5.10.15.20")'
knownipThree = 'request_handle("00.00.11.20")'


for i in range(225):
    endArr.append(knownipOne)
for i in range(360):
    endArr.append(knownipTwo)    
for i in range(90):
    endArr.append(knownipThree)
``` 


## How It Works

The primary components of our system are the following:

1: An Array with custom ibjects called IpBucket

2: IpBucket which has a few properties,

   Two pointers so it can reference its next node and previous 
   
   A set to contain all elements of the same IpCount in the same object
   
   The current value or ipcount for that bucket

3: A dictionary to store our IpAddresses 
Key: IpName
Value: [IpHits, Reference to the IpBucket Object where its stored within our Array System]

General Concept:
We have an array that stores all of our Top 100 Ips.
First: It just fills the array with Top 100 Ips

After that When a new IpRequest comes through it checks to see if the Ip Exists within our array already. If it doesn't, or it's not above our minimum top ip value it just continues on. If it does it updates its location in the Array in o(1) time because we have the stored IpBucketObject. The reason for not just using an index for example is if (insertions occur or deletions occur) the index will not neccesarily correspond to the right element (you can Use an indexoffset which I have for our iteration but it gets complicated). Our pointers are used so we can jump to the next element without needing to do an Index Lookup, so O(1) time, (most expected operations that we'll have within our system will likely be jumping to the .Next bucket) meaning most updates will be O(1) 



## Question Section

