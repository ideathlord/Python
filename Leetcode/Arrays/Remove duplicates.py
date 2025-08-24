class Solution(object):
    def removeDuplicates(self, nums):
        slow = 1

        for fast in range(1,len(nums)):
            if nums[fast] != nums[fast-1]:
                nums[slow] = nums[fast]
                slow = slow + 1

        return slow        

# Time Complexity: O(n)
# Space Complexity: O(1)
