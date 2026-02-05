class Solution:
    def targetIndices(self, nums: List[int], target: int) -> List[int]:
        targetArr = []
        nums.sort()
        for index in range(len(nums)):
            if nums[index] == target:
                targetArr.append(index)
        
        return targetArr
