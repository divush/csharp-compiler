namespace HelloWorld
{
	class Hello 
	{
		int Main() 
		{
			int[] a = {4, 2, 1, 3};
			Writeline(a[0]);
			Writeline(a[1]);
			Writeline(a[2]);
			Writeline(a[3]);
			a[0] = 1;
			a[1] = 3;
			a[2] = 3;
			a[3] = 4;
			Writeline(a[0]);
			Writeline(a[1]);
			Writeline(a[2]);
			Writeline(a[3]);
			int i = a[0] + a[1] + a[2] + a[3];
			Writeline(i);			
			return 0;
		}
	}
}