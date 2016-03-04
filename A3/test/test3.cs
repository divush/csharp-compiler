/*
 * C# Program to Get a Number and Display the Sum of the Digits 
 */
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
 
namespace Program
{
    class Program
    {
        static void Main(string[] args)
        {
            int num, sum = 0, r;
            Console.WriteLine("Enter a Number : ");
            num = int.Parse(Console.ReadLine());
            while (num != 0)
            {
                r = num % 10;
                num = num / 10;
                sum = sum + r;
            }
            Console.WriteLine("Sum of Digits of the Number : "+sum);
            Console.ReadLine();
 
        }
    }
}