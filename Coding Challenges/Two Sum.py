'''
#############
  Challenge
#############
Given an array of integers that is already sorted in ascending order, find two numbers such that they add up to a specific target number.

The function twoSum should return indices of the two numbers such that they add up to the target, where index1 must be less than index2. Please note that your returned answers (both index1 and index2) are not zero-based.

You may assume that each input would have exactly one solution and you may not use the same element twice.

Input: numbers=[2, 7, 11, 15], target=9
Output: index1=1, index2=2 


#############
  Thoughts
#############

Getting the index by assigning the list index and list element to a dictionary for later referencing. 

eg, given list [2,7,11,15] and t=9. dic = {0:2,1:7,2:11,3:15} by enumerating the list while checking on the existence of the subtraction (t-list element) on the 
dictionary. if found, then its associating index would be returned. 

#####################
 Translated Solution
#####################
'''
class Solution(object):
    def twoSum(self, numbers, target):
        """
        :type numbers: List[int]
        :type target: int
        :rtype: List[int]
        """
        dic = {}
        
        for i, num in enumerate(numbers):
            if target - num in dic:
                return [dic[target - num] + 1, i + 1]
                
            dic[num] = i
        
        return []
