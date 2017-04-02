
'''
#############
  Challenge
#############
Given a non-empty integer array, find the minimum number of moves required to make all array elements equal, where a move is incrementing a selected element by 1 or decrementing a selected element by 1.

You may assume the array's length is at most 10,000.

Example:

Input:
[1,2,3]

Output:
2

Explanation:
Only two moves are needed (remember each move increments or decrements one element):

[1,2,3]  =>  [2,2,3]  =>  [2,2,2]

#############
  Thoughts
#############

The minimum moves can be calculated by summing up the number of calculation around the median positioned element on the list. 

eg, given list  =  [1,2,3],. hence, the median element being 2 whose neighbors are the result of its +&- 1 calculation. so, the minimum moves
equals to 2. 

#####################
 Translated Solution
#####################
'''
class Solution(object):
    def minMoves2(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        nums.sort()
        median = nums[len(nums) / 2]
        return sum(abs(num - median) for num in nums)

