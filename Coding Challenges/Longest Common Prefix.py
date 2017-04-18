'''
#############
  Challenge
#############
Write a function to find the longest common prefix string amongst an array of strings. 
eg, give list =  ['leet', 'leed','letd','lees']
common = 'le'
#############
  Thoughts
#############
The easiest way to get around is by using the Counter from the collection module. 
eg, given list =  ['leet', 'leed','letd','lees']
    Counter(list[0]) & Counter(list[1]) will return the in common which is 'lee', but in dict though. 
    
    therefore, we will need to convert the dict into a string which is then again referenced with the rest list.


#####################
 Translated Solution
#####################
        
class Solution(object):

    def longestCommonPrefix(self, strs):
        """
        :type strs: List[str]
        :rtype: str
        """
        if not strs:
            return ''
        str = strs[0]
        for i in range(1,len(strs)):
	        k = collections.Counter(str) & collections.Counter(strs[i])
	        str=""
	        for i in dict(k):
		        str+=i*k[i]
		        
        return str
	
