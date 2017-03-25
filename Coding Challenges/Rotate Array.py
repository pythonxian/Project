'''
#############
  Challenge
#############
Rotate an array of n elements to the right by k steps.

For example, with n = 7 and k = 3, the array [1,2,3,4,5,6,7] is rotated to [5,6,7,1,2,3,4]

Could you do it in-place with O(1) extra space? 

#############
  Thoughts
#############

Honestly, this is not a easy challange. It is mathematical to say the least. 

initially, my thought on this would be just purly moving each of the element in the list accrodance with the given k steps. This can
be done if in-place is not a requirement. it means that no extra list or temp list to hold the referencing element between the two list
during the rotation on the original list. 

Then, i asked my friend google and i got this. 

eg, let say, i=[1,2,3,4,5,6,7], k=3. 
Then, the expected result should be [5,6,7,1,2,3,4]

How?

Fist, we need to determine how rotation round is needed. 
a rotation round means that the starting position or index of the element from the list equals to the finishing position during the 
rotation. 

i = [1,2,3,4,5,6], k=2. rotation starts with i[0] or 1, then you get, 1->3->5->1. Noticing that the starting and finishing position or
index being equal. then, we call this a round. 

How to determine the round?

It is the GCD (Greatest Common Divisor). 

eg, i=[1,2,3,4,5,6,7], k=3.

the length of i equals to 7. 

GCD of 7 and 3 equals to 1. 

7=1x7
3=1x3. 

Therefore, the greatest common divisor of these two is 1.

Second, by knowing the number of rotation round we need, we could go ahead to shift the element in place. 

back to the same example, i=[1,2,3,4,5,6,7]. the element will right-shift then back to the left. It is more like a circle. 
Because of the given list with length 7, a circle of 7 means the reminder of the modulus between 7 and the changing element equals 
to 0.

eg.

1->2->3->4->5->6-> 7 ->.....14

if we start left shifting from 1, a circle is complete when we get to 7. 
if we start left shifting from 1, two circles are complete when we get to 14.   
    
    
  
    
#####################
 Translated Solution
#####################
'''
	
class NumArray(object):

  def gcd(a,b):
	  if b==0:
                return a
        else:
                return gcd(b, a%b)
         
  def RotateArray(nums,k)
      n=len(nums)
      for i in range(gcd(n,k)):
	    pre = nums[i]
      s = i
        while (s+k)%n != i:
        	nums[(s+k)%n], pre = pre, nums[(j+k)%n]
                s = (s+k)%n
        nums[(s+k)%n] = pre


