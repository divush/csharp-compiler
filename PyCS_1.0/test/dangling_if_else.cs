namespace test
{
	class test 
	{
		int Main() 
		{
			int j = 0;
			while (j < 3) {
				int i = 2;
				if (i < 4 && i > 2) {
					Writeline(1);
				}
				if (i > 1) {
					Writeline(2);
				}
				else {
					if (i > 2) {
						Writeline(3);
					}
				}
				j = j + 1;
			}
			return 0;
		}
	}
}