from typing import List

def find_first_occurrence(nums: List[int], target: int) -> int:
    left, right = 0, len(nums) - 1
    result = -1
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            result = mid
            right = mid - 1 # Look Left
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return result

def find_last_occurrence(nums: List[int], target: int) -> int:
    left, right = 0, len(nums) - 1
    result = -1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if nums[mid] == target:
            result = mid
            left = mid+1
            
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
            
    return result