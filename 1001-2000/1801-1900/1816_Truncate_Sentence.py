class Solution:
    def truncateSentence(self, s: str, k: int) -> str:
        words = s.split()           # Split into a list of words
        truncated = words[:k]        # Take the first k words
        return " ".join(truncated)   # Join them back into a string with spaces
