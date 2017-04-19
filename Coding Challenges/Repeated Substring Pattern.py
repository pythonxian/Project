
'''
#############
  Challenge
#############
Given a non-empty string check if it can be constructed by taking a substring of it and appending multiple copies of the substring together. You may assume the given string consists of lowercase English letters only and its length will not exceed 10000.

Example 1:

Input: "abab"

Output: True

Explanation: It's the substring "ab" twice.


#############
  Thoughts
#############

Let's say T = S + S.
"S is Repeated => From T[1:-1] we can find S" is obvious.

If from T[1:-1] we found S at index p-1, which is index p in T and S.
let s1 = S[:p], S can be represented as s1s2...sn, where si stands for substring rather than character.
then we know T[p:len(S) + p] = s2s3...sn-1sns1 = S = s1s2...sn-2sn-1sn.
So s1 = s2, s2 = s3, ..., sn-1 = sn, sn = s1,Which means S is Repeated.

edit:
I should fix this because len(si) == len(sj) has not be proved. The procedure becomes complicated :-(
Let s1 = S[:p], S can be represented as s1X1.
then S = X1s1 = s1X1 (A).

    len(X1) < len(s1) is false because if so we should find S in T[1:-1] at index len(X1) rather than len(s1) = p.

    len(X1) == len(s1) and (A) => X1 = s1 => S is Repeated.

    len(X1) > len(s1) and (A) => X1 has prefix s1 so can be represented as s1X2.
    X1 = s1X2 and (A) => s1X2s1= s1s1X2 =>X2s1 = s1X2 (B).
    len(X2) < len(s1) is false because if so (A) and (B) => S = X2s1s1 = s1s1X2 and we should find S at index len(X2) rather than p.

    As long as len(Xi-1) > len(s1), we can get Xis1 = s1Xi through the prefix step and prove len(Xi) < len(s1) is false through the index step. Eventually we can get a Xn, len(Xn) == len(s1) and Xns1 = s1Xn => Xn = s1 => S = s1X1 = s1s1X2 = ... = s1s1...s1Xn-1 = s1s1...s1s1Xn => S is Repeated.



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
