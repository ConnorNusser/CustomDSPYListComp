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

Additionally, you can add in specific values/different max ip values by manipulating the request handle string
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

   * Two pointers so it can reference its next node and previous 
   
   * A set to contain all elements of the same IpCount in the same object
   
   * The current value or ipcount for that bucket

3: A dictionary to store our IpAddresses 
 * Key: IpName
 * Value: [IpHits, Reference to the IpBucket Object where its stored within our Array System]

General Concept:
We have an array that stores all of our Top 100 Ips.
<small>
First: It just fills the array with Top 100 Ips After when a new IpRequest comes through it checks if the Ip Exists within our array. If it doesn't exist within our array or meet a minimum value, its continues on. If it does it updates its location in the Array in O(1) time. The reason because we have the stored IpBucketObject. Note: The reason for not just using an index for example, is if (insertions occur or deletions occur) the index will not neccesarily correspond to the right element (you can use an indexoffset which I have for anohter iteration but it gets complicated). Our pointers are used so we can jump to the next element without needing to do an Index Lookup, so O(1) time. Most of the expected operations within our system will likely be jumping to the .Next meaning most updates will be O(1). 
<small/>



## Question Section



### How would you test this to ensure it’s working correctly?
I'd probably alter TextFilterCreation.py where it could be called with specific inputs and then get an actual return value from our Main Project.

You could input certain IpHandles and the count for those IpHandles and then evalute whether the returned count is equivalent.
Ex: Assert.True(TextFilterCreationPy("10.20.40.50, 15) == 15)

What is the runtime complexity of each function?
Top100()
Runtime complexity: O(N) N being just our top 100 elements.


### HandleStreamRequests(ipname)
#### All of the runtime complexities for Log(N) are relative to just the top 100 so technically its O(Log(100)) or O(10) 
Runtime complexity: Worst Case O(log(n)) N being just our top 100 elements. Best Case O(1)
HandleStreamRequests is comprised of essentially four functions.
    Inserting New Element not in Array: Runtime O(1)
    
    Adding Element to End of Array (moveNextAppend): Runtime O(1)
    
    Moving to the next pointer (moveNextArrow): Worst Case O(log(n)) N being just our top 100 elements, most cases O(1) only when a previous node needs to be removed will it be O(log(n))
    
    Moving to the next pointer (moveNextSquare): Worst Case O(log(n)) N being just our top 100 elements, though in cases where its only element in the bucket it'll be O(1)
    
    
### What would you do differently if you had more time?
Another thing I thought of adding if this was a real world scenario is you could use multiple channels, (my mention of  concurrency). The base problem being, if you push elements randomly into the channel it'll be hard to know whats the "top 100" because, maybe a set of ips got "unlucky", and all got separated so it may not look like a potential top 100. 

But what I would do is divide the IpAddresses into sets

So Example 

Ip "00.00.00" to "22.22.22" would go to channel 1

Ip "22.22.22" to "44.44.44" would go to channel 2

Ip "44.44.44" to "66.66.66" would go to channel 3

And then when top 100 is called you call all Top 100 Elements from channel 1, 2 and 3. 

Sort them, grab the top 100 of the channels and then return back to each channel a new minimum value of Top 100. 

This new minimum value would inevitably also speed up each channel because now you would only need to  do insertions relative to the most recent real top 100, vs before the top 100 being localized to the channel.

What other approaches did you decide not to pursue?
My other approach which is here: https://github.com/ConnorNusser/ListAtmpt has O(1) runtime for everything but has really bad space complexity. It has a space complexity relative to the highest IpCount(in top 100) - min IpCount (in top 100). 
I thought generally the space complexity could get problematic. Say a single user was making a huge number of requests or intentionally messing with the system it might create a space complexity of maybe 1 Million or something over the day.
Additionally, my other solution (this one) is O(1) pretty much all the time and O(log(n)) but with only 100 items O(10) isn't that big of a deal in my opinion. 

If we had to get say top1000() or top10000() I'd probably use my other method.

