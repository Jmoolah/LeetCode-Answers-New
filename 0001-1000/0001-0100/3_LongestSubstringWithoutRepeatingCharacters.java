class Solution {
    public int lengthOfLongestSubstring(String s) {
        char[] sArr = s.toCharArray();
       
    
        //test
        //test
        int count = 0;
        HashSet<Character> hs = new HashSet<>();
        for(int i =0; i < s.length();i++){

            hs.clear();

            for(int j = i; j < s.length(); j++){
                if(hs.contains(sArr[j])){
                    break;
                }
                hs.add(sArr[j]);

                
            }
            int check = hs.size();
                if (check > count){
                    count = check;
                }
            
        }
        return count;
    }
}
