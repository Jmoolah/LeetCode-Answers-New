class Solution {
    public double findMedianSortedArrays(int[] nums1, int[] nums2) {
        int[] merged = new int[nums1.length + nums2.length];
        int n = merged.length;
        double median;
        System.arraycopy(nums1, 0, merged, 0, nums1.length);
        System.arraycopy(nums2, 0, merged, nums1.length, nums2.length);
        Arrays.sort(merged);
        if (n % 2 == 1) {
            // odd length → middle element
            median = merged[n / 2];
        } else {
            // even length → average of two middle numbers
            median = (merged[n/2 - 1] + merged[n/2]) / 2.0;
        }
        return median;
        //test test
    }
}
