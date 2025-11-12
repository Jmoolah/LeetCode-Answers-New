class Solution {
    public int[] twoSum(int[] nums, int target) {
       HashMap<Integer,Integer> hm = new HashMap<>();

        int n = nums.length;

        for(int i =0; i < n; i++){
            Integer complement = target - nums[i];

            if(hm.containsKey(complement)){
                return new int[]{hm.get(complement), i};
            } 
            hm.put(nums[i], i);
        }
       
        

        return new int[]{};

    }
}