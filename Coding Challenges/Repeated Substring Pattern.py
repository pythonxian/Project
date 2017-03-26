
'''
#############
  Challenge
#############
Given a non-empty string check if it can be constructed by taking a substring of it and appending multiple copies of the substring together. 

Input: "abcabcabcabc"

Output: True

Explanation: It's the substring "abc" four times. (And the substring "abcabc" twice.)



#############
  Thoughts
#############

I can't think of any except for Brute Force/Exhaustive Search meaning trying all the combination of the element while enumerating 
the list. I dont think this is a good approach. Then again, i asked my friend Google. he gave me a very smart solution and also a
lesson learned for me. 

"Consider a string S="helloworld". Now, given another string T="lloworldhe", can we figure out if T is a rotated version of S? Yes, we can! We check if S is a substring of T+T.

Fine. How do we apply that to this problem? We consider every rotation of string S such that it's rotated by k units [k < len(S)] to the left. Specifically, we're looking at strings "elloworldh", "lloworldhe", "loworldhel", etc...

If we have a string that is periodic (i.e. is made up of strings that are the same and repeat R times), then we can check if the string is equal to some rotation of itself, and if it is, then we know that the string is periodic. Checking if S is a sub-string of (S+S)[1:-1] basically checks if the string is present in a rotation of itself for all values of R such that 0 < R < len(S)."


#####################
 Translated Solution
#####################
'''
	
def repeatedSubstringPattern(self, str):

        """
        :type str: str
        :rtype: bool
        """
        if not str:
            return False
            
        ss = (str + str)[1:-1]
        return ss.find(str) != -1
