namespace HelloWorld
{
	class Hello 
	{
		int fact(int n)
		{
			int ans=1;
			for(int j=2; j<=n; ++j)
			{
				ans = ans * j;
			}
			return ans;
		}
		int Main() 
		{
			int f = fact(5);
			Writeline(f);
			return 0;
		}
	}
}