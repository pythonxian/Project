'''
#############
  Challange
#############
The Hamming distance between two integers is the number of positions at which the corresponding bits are different.

Given two integers x and y, calculate the Hamming distance.

Note:
0 ≤ x, y < 231.

Example:

Input: x = 1, y = 4

Output: 2

Explanation:
1   (0 0 0 1)
4   (0 1 0 0)
       ↑   ↑

The above arrows point to positions where the corresponding bits are different.

#############
  Thoughts
#############

As shown from the example, we need to count the total number of different positions at which the corresponding bits are different. So, the first thing we do is to convert the given integer in binary format. 

1   (0 0 0 1)
4   (0 1 0 0)
       ↑   ↑
      
By observing the given example, noticing that the first bit on the right and  the third bit on the left are different. If we could tell the code to count them, then our job would be done. So how do we do that in python? The answer is the Bitwise Operator. with 1^0 = 1, all we need is to count how many 1 post the operation on the given integer.  

'''

#####################
 Translated Solution
#####################

class Solution(object):
    def hammingDistance(self, x, y):
        """
        :type x: int
        :type y: int
        :rtype: int
        """
        return bin(x ^ y).count('1')
