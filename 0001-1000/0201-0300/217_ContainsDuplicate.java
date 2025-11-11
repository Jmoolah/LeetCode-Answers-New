class Solution {
    public boolean containsDuplicate(int[] nums) {
        HashSet<Integer> set = new HashSet<>();

        for(int x: nums){
            boolean added = set.add(x);
            if (!added){
                return true;
            }
        }
        return false;
    }
}