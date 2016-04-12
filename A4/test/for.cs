namespace HelloWorld
{
	class Hello 
	{
		int Main() 
		{
			int i = 6;
			char a;
			for (i = 6;i < 9 && i > 5 && i != 7; ++i){
				if (i > -1){
					a = "y";
				}
				else 
					a = "n";
			}
			return 0;
		}
	}
}