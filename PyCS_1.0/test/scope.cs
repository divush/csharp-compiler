namespace test
{
	class test 
	{
		int Main() 
		{
			int j = 0;
			while (j < 3) {
				int k = 0;
				while (k < 3) {
					Writeline(j);
					k = k + 1;
				}
				j = j + 1;
			}
			return 0;
		}
	}
}