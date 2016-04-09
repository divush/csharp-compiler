namespace Program {
    class Program {
        int d = 2;
        int l = 6, m = d, p;
    	int fact(int y) {
            if (y == 1) {
                return 1;
            }
            return y*fact(y-1) ; 		
    	}
        int doublefact(int x) {
            return d*fact(x);
        }
        int Main() {
            int y = 10;
            int x = fact(y, c);
        }
    }
}