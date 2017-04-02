
'''
#############
  Challenge
#############
A binary watch has 4 LEDs on the top which represent the hours (0-11), and the 6 LEDs on the bottom represent the minutes (0-59).

Each LED represents a zero or one, with the least significant bit on the right.

For example, the above binary watch reads "3:25".

Given a non-negative integer n which represents the number of LEDs that are currently on, return all possible times the watch could represent.

Example:

Input: n = 1
Return: ["1:00", "2:00", "4:00", "8:00", "0:01", "0:02", "0:04", "0:08", "0:16", "0:32"]


#############
  Thoughts
#############

Hour representation 1-12, can also be represented in binary format: 8,4,2,1
Same goes to the miniutes 0-60, in binary formst: 32,16,8,4,2,1

so, given the int N to represent the number of LEDs are on. in another word, it means the number of 1s in binary format. 

Therefore, the solution is that we need to calculate the number of 1. 



#####################
 Translated Solution
#####################
'''
class Solution(object):
    def readBinaryWatch(self, num):
        """
        :type num: int
        :rtype: List[str]
        """
        ans = []
        for h in range(12):
            for m in range(60):
                if (bin(h)+ bin(m)).count('1') == num:
                    ans.append('%d:%02d' % (h, m))
        return ans
