using System;
namespace HelloWorld
{
	class Hello 
	{
		struct T
		{
			char a;
			int b;
			char c;
			short d;
			char f;
		};
		void f (T x)
		{
			x.a = 'a';
			x.b = 47114711;
			x.c = 'c';
			x.d = 1234;
			x.f = '*';
		}
		void Main() 
		{
			T k;
			f(k);
			return 0;
		}
	}
}