namespace HelloWorld
{
	class Hello 
	{
		int Main() 
		{
			for (int i = 0;i < 10; ++i){
				for (int j = 0; j < 3; ++j) {
					Writeline(i*j);
				}
			}
			return 0;
		}
	}
}