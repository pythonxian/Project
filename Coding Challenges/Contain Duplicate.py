
'''
#############
  Challenge
#############
Given an array of integers and an integer k, return true if and only if there are two distinct indices i and j in the array such that nums[i] = nums[j] and the difference between i and j is at most k.

#############
  Thoughts
#############

let say, given an array of [1,2,4,5,3,1,6], k=5. The duplicated being 1, and idx(5) - idx(0) <=5, which is True. 

So, all we need is to figure out the index of the same element on the list. This can be done by using a dictionary which does not
allow the existence of any duplicate element. its use with element assignment from the list can be referenced for getting the index number
of the element should any duplication occur. 


#####################
 Translated Solution
#####################
'''
class Solution:
    # @param {integer[]} nums
    # @param {integer} k
    # @return {boolean}
    def containsNearbyDuplicate(self, nums, k):
        numDict = dict()
        for x in range(len(nums)):
            idx = numDict.get(nums[x])
            if idx >= 0 and x - idx <= k:
                return True
            numDict[nums[x]] = x
        return False
