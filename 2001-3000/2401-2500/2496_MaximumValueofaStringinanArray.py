class Solution:
    def maximumValue(self, strs: List[str]) -> int:
        lengths = []

        for string in strs:
            if string.isdigit():
                lengths.append(int(string))
            else:
                lengths.append(len(string))
        
        return max(lengths)
