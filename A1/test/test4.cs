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
            int n`um, sum = 0, r;           //num is 'invalid token' on purpose.
            Console.WriteLine("Enter a Number : ");
            num = int.Parse(Console.ReadLine());
            while (num != 0)
            {
                r = nu`m % 10;          //Invalid token
                num = n~um / 10;           //Invalid token
                sum = sum + r;
            }
            Consol"e.WriteLine("Sum of Digits of the Number : "+sum);   //Inserting invalid double quotes!
            Console.ReadLine();
 
        }
    }
}