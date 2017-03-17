'''
#############
  Challenge
#############

Given an integer array nums, find the sum of the elements between indices i and j (i ≤ j), inclusive.

Note:

Given nums = [-2, 0, 3, -5, 2, -1]

sumRange(0, 2) -> 1
sumRange(2, 5) -> -1
sumRange(0, 5) -> -3

#############
  Thoughts
#############

First thought, what about if we put the result from the sum of the list items as we iterate through (based on the list index) nums to another list (let say, sum = []). 
Then, we would know the final result by subtraction with given index j and i. 

eg, 
	i=1, j=4
	nums = [1,2,3,4,5]
		sum=[0,1,3,6,10,15]  
		 result = sum[j+1] - sum[i]

Second thought, given index j and i, we could start positioning our iteration on range in python. 

eg,  i=1, j=4
	nums = [1,2,3,4,5]
	result=0
	for x in range (i,j+1) 
		result+=nums[x]


#####################
 Translated Solution
#####################
'''
	
class NumArray(object):

    def __init__(self, nums):
        """
        :type nums: List[int]
        """
        size = len(nums)
        self.sums = [0] * (size + 1)
        for x in range(size):
            self.sums[x + 1] += self.sums[x] + nums[x]

    def sumRange(self, i, j):
        """
        :type i: int
        :type j: int
        :rtype: int
        """
        return self.sums[j + 1] - self.sums[i]
