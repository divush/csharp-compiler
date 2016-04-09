namespace Program {
    class Program {
        int max = 10;
    	int mul(int x, int y) {
            int z;
    		if (x > y) {
    			return x-y;
    		} else {
    			return y-x;
    		}
    		
    	}
        int Main() {
            int num =1;
            int[] numbers = {1, 2, 3, 4, 5};
            int y = mul(2,3);
            max = 5;
            numbers[2] = 3 + numbers[1];
            while ( max > num && num < 3) {
                num = num + 1;
            }
            max = num = 1;
			return 0;
        }
    }
}