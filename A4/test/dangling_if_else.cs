namespace test
{
	class test 
	{
		int Main() 
		{
			int i = 0;
			char j="charvar";
			int[] a = {1,2,3};
			if (i < 4)
				++a[i];
			if (i > 1)
				--a[i];
			else 
				a[i] = 1;
			Writeline(a[i]);
		}
	}
}