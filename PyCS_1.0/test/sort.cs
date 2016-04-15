namespace HelloWorld
{
	class Hello 
	{
		int Main() 
		{
			int[] a = {4, 2, 1, 3};
			int n = 4;
			for(int i=0; i<n; i++)
			{
				int min = a[i], index = i;
				for(j=i+1;j<n;j++)
				{
					if(a[j]<min)
					{
						min = a[j];
						index = j;
					}
				}
				int temp = a[index];
				a[index] = a[i];
				a[i] = min;
			}
		}
	}
}