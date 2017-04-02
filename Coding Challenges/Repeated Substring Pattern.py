
'''
#############
  Challenge
#############
Given a string s and a non-empty string p, find all the start indices of p's anagrams in s.

Strings consists of lowercase English letters only and the length of both strings s and p will not be larger than 20,100.

The order of output does not matter.

Input:
s: "cbaebabacd" p: "abc"

Output:
[0, 6]

Explanation:
The substring with start index = 0 is "cba", which is an anagram of "abc".
The substring with start index = 6 is "bac", which is an anagram of "abc".

#############
  Thoughts
#############

The given non-empty string is like a window of element you would like to match against the string s. Sliding window matching
is the solution for this task. Starting from the left of the string s till end. 


#####################
 Translated Solution
#####################
'''
	
class Solution(object):
    def findAnagrams(self, s, p):
        """
        :type s: str
        :type p: str
        :rtype: List[int]
        """
        output = []
        for i in range(len(p)-1, len(s)):
            if sorted(s[i-len(p)+1]:i+1) == sorted(p):
                output.append(i-len(p)+1)

        return output
