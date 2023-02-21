from enum import Enum
import csv
import sys
import time

class IpBucket:
    def __init__(self, currVal = 1):
        #current Value for this bucket of values
        self.currVal = currVal
        # The set of different Ip Addresses
        self.ipBucketSet = set()
        # two pointers to point to the next and previous linked list points
        self.next = None
        self.prev = None
class IpMetadata(Enum):
    VALUE = 0
    INDEXPOSITION = 1
    
class Solution:
    def __init__(self):
        self.ipDictionary =  {}
        self.ipArray = [IpBucket()]
    
    def binarySearch(self, localVal):
        left = 0
        right = len(self.ipArray) - 1
        
        while(left <= right):
            mid = (left + right) // 2
            if self.ipArray[mid].currVal == localVal:
                return mid
            elif self.ipArray[mid].currVal < localVal:
                left = mid + 1
            else:
                right = mid - 1
        return 0
        
    # Runtime complexity o(1)
    def moveNextAppend(self, localVal, localBucket:IpBucket, ipName):
        #no reason to append a new value just update currVal
        if len(localBucket.ipBucketSet) == 1:
            localBucket.currVal = localVal
            return
        #discard from previous bucket add to new    
        localBucket.ipBucketSet.discard(ipName)
        self.ipArray.append(IpBucket(localVal))
        # add pointer references
        self.ipArray[-2].next = self.ipArray[-1]
        self.ipArray[-1].prev = self.ipArray[-2]
        # change obj reference for IpName
        self.ipDictionary[ipName][IpMetadata.INDEXPOSITION.value] = self.ipArray[-1]
        self.ipArray[-1].ipBucketSet.add(ipName)
    
    # Runtime complexity
    # O(1) for most cases
    # If removal of previous node is neccesary worst case: O(Log(n)) with the max n being 100       
    def moveNextArrow(self, localVal, localBucket:IpBucket, ipName):
        #add to new bucket
        localBucket.next.ipBucketSet.add(ipName)
        localBucket.ipBucketSet.discard(ipName)
        # change obj reference for ip Name
        self.ipDictionary[ipName][IpMetadata.INDEXPOSITION.value] = localBucket.next
        if len(localBucket.ipBucketSet) == 0:
            oldIndex = self.binarySearch(localVal - 1)
            if(oldIndex > 0):
                prevIndex = localBucket.prev
                nextIndex = localBucket.next
                # add pointers to new Index
                nextIndex.prev = prevIndex
                prevIndex.next = nextIndex
            # remove pointers from old Index
            localBucket.next = None
            localBucket.prev = None
            self.ipArray.pop(oldIndex)
    
    # Runtime complexity
    # Worst Case: O(Log(n)) with the max n being 100   
    # Best Case: O(1) which happens if its the only item in the bucket... or you get lucky with binarySearch       
    def moveNextSquare(self, localVal, localBucket: IpBucket, ipName):
        # No need to move pointers or do anything except update currVal if its the only item
        # O(1) runtime
        if len(localBucket.ipBucketSet) == 1:
            localBucket.currVal = localVal
            return
        
        # O(Log(n)) run time with max n being 100
        localBucket.ipBucketSet.discard(ipName)
        index = self.binarySearch(localVal - 1)
        newIndex = index + 1
        
        self.ipArray.insert(newIndex, IpBucket(localVal))
        #Get next ref
        next = localBucket.next
        # add in pointers for new object
        self.ipArray[newIndex].next = next
        self.ipArray[newIndex].prev = localBucket
        # switch pointers for
        next.prev = self.ipArray[newIndex]
        localBucket.next = self.ipArray[newIndex]
        #add in value to new bucket
        self.ipArray[newIndex].ipBucketSet.add(ipName)
        self.ipDictionary[ipName][IpMetadata.INDEXPOSITION.value] = self.ipArray[newIndex]
        
    def handle_initial_requests(self, ipName):
        localVal = self.ipDictionary[ipName][IpMetadata.VALUE.value]
        localBucket = self.ipDictionary[ipName][IpMetadata.INDEXPOSITION.value]
        
        if len(self.ipDictionary) == 1:
            self.ipDictionary[ipName][IpMetadata.INDEXPOSITION.value] = self.ipArray[0]
            localBucket = self.ipDictionary[ipName][IpMetadata.INDEXPOSITION.value]
            localBucket.ipBucketSet.add(ipName)
            localBucket.currVal = localVal
            return
            
        if localBucket == None:
            if self.ipArray[0].currVal == 1:
                self.ipDictionary[ipName][IpMetadata.INDEXPOSITION.value] = self.ipArray[0]
                self.ipArray[0].ipBucketSet.add(ipName)
                return 
            else:
                self.ipArray.insert(0, IpBucket(localVal))
                self.ipArray[0].ipBucketSet.add(ipName)
                self.ipDictionary[ipName][IpMetadata.INDEXPOSITION.value] = self.ipArray[0]
                #add pointers to next
                self.ipArray[0].next = self.ipArray[1]
                self.ipArray[1].prev = self.ipArray[0]
                return 
        else:
            self.primaryHandler(localVal, localBucket, ipName)
    
    def primaryHandler(self, localVal, localBucket, ipName):
        
        if localBucket.next == None:
            self.moveNextAppend(localVal, localBucket, ipName)
            return
        if localBucket.next.currVal == localVal:
            self.moveNextArrow(localVal, localBucket, ipName)
        else:
            self.moveNextSquare(localVal, localBucket, ipName)

    def popbottomElement(self):
        removed_val = self.ipArray[0].ipBucketSet.pop()
        self.ipDictionary[removed_val][IpMetadata.INDEXPOSITION.value] = None
    
    def checkRemoveFirst(self):
        if(len(self.ipArray[0].ipBucketSet) == 0):
            self.ipArray[1].prev = None
            del self.ipArray[0]
    
    def handle_stream_requests(self, ipName):
        #Find Index of ipName
        #O(1) Lookup
        localBucket = self.ipDictionary[ipName][IpMetadata.INDEXPOSITION.value]
        localValue = self.ipDictionary[ipName][IpMetadata.VALUE.value]
        
        # remove first array element if its now empty
        self.checkRemoveFirst()
        # did it this way instead of removal inside the code body because it eliminates a need for a bunch of checks in our other methods
        
        if(localValue <= self.ipArray[0].currVal):
            return
        # Value must be greater and if its not already in our system it should be in the next.index
        if(localBucket == None):
            # Edge Case essentially where the ipDictionary hit were only active once
            if len(self.ipArray) == 1:
                self.moveNextAppend(localValue,self.ipArray[0],ipName)
                self.popbottomElement()
                return
            elif self.ipArray[1].currVal == localValue:
                self.ipArray[1].ipBucketSet.add(ipName)
                self.ipDictionary[ipName][IpMetadata.INDEXPOSITION.value] = self.ipArray[1]
                self.popbottomElement()
                return
            else:
                # add in new element
                self.ipArray.insert(1, IpBucket(localValue))
                
                #next
                next = self.ipArray[0].next
                prev = self.ipArray[0]
                
                self.ipArray[1].next = next
                self.ipArray[1].prev = prev
                
                prev.next = self.ipArray[1]
                next.prev = self.ipArray[1]
                self.ipArray[1].ipBucketSet.add(ipName)
                self.ipDictionary[ipName][IpMetadata.INDEXPOSITION.value] = self.ipArray[1]
                self.popbottomElement()
                return
        
        #Update so it doesn't require any removal
        self.primaryHandler(localValue, localBucket, ipName)
        return
            
 
                    
    def request_handled(self, ip_address):
        if ip_address not in self.ipDictionary:
            self.ipDictionary[ip_address] = [1, None]
        else:
            self.ipDictionary[ip_address][IpMetadata.VALUE.value] = self.ipDictionary[ip_address][IpMetadata.VALUE.value] + 1
        if len(self.ipDictionary) <= 100:
            # go crazy fill the array as much as you can
            self.handle_initial_requests(ip_address)
            return
        self.handle_stream_requests(ip_address)
    def clear(self):
        self.ipDictionary =  {}
        self.indexOffSet = 0
        self.ipArray = [IpBucket()]
    def top100(self):
        currTime = time.time()
        lastNode = self.ipArray[-1]
        bracket_string = "---------"
        print(bracket_string)
        print("Ranking of top 100 in ASC to Desc Order")
        while(lastNode != None):
            print(f"IpHits:{lastNode.currVal} Ips:{lastNode.ipBucketSet}")
            lastNode = lastNode.prev
        print("Time to complete Operation: %s Seconds" % (time.time() - currTime))
        print(bracket_string)
        
            
    
    
def main(argv):
    sol = Solution()
    def request_handle(ip_address):
        sol.request_handled(ip_address)
    def top100():
        sol.top100()
    def clear():
        sol.clear()
    
    request_handle("10.20.40")
    request_handle("10.20.40")
    request_handle("10.20.40")
    request_handle("11.12.14")
    request_handle("11.12.24")
    request_handle("999")
    request_handle("10.20.40")
    request_handle("5.10.15.20")
    request_handle("10.20.40")
    request_handle("11.12.14")
    request_handle("11.12.24")
    top100()
    with open("./txtFile.csv", 'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            exec(row[0])

if __name__ == "__main__":
   main(sys.argv[1:])
