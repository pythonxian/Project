'''
#############
  Challenge
#############
Given a string s and a non-empty string p, find all the start indices of p's anagrams in s.

Strings consists of lowercase English letters only and the length of both strings s and p will not be larger than 20,100.

The order of output does not matter.

Example 1:

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

A sliding window solution. 
The given P string is like a window of element that we would need to search as we enumerate the given string S starting with the end index of the window P.
''

#####################
 Translated Solution
#####################

output = []
str="cbaebabacd"
p="abc"

for i in range(len(p)-1, len(str)):
	if sorted(str[i-len(p)+1:i+1]) == sorted(p):
		output.append(i-len(p)+1)

print output
