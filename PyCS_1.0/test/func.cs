namespace HelloWorld
{
	class Hello 
	{
		int foo(int x, int y)
		{
			return x / y;
		}
		int Main() 
		{
			int a = 4, b = 2;
			int i = a+ b +foo(a,b);
			Writeline(i);
			return 0;
		}
	}
}