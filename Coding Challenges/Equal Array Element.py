
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

with the given example, it is obvious that the number of moves equal to the sum of the move(+1 or -1) from the median element of the list.

eg, [1,2,3]

median = 2. +1 gets to 3 and -1 gets to 1. so the sum of move equal 2.

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
