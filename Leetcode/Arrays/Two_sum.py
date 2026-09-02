class Solution(object):
    def twoSum(self, nums, target):
    
        dict_nums = {}
        for i in range(0,len(nums)):
            if target - nums[i] in dict_nums:
                return [dict_nums[target-nums[i]],i]
            else:
                dict_nums[nums[i]] = i     

 
# Time Complexity: O(n)
# Space Complexity: O(n)
