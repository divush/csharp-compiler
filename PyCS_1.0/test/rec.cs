namespace HelloWorld
{
	class Hello 
	{
		int fact(int x)
		{
			if (x == 1) {
				return 1;
			}
			int t = fact(x-1);
			return x*t;
		}
		int Main() 
		{
			int a = 3;
			int i = fact(a);
			Writeline(i);
			return 0;
		}
	}
}