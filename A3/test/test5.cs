/*
 * C# Program to Swap the Contents of two Numbers using Bitwise XOR Operation
 */
using System;
class program
{
    public static void Main()
    {
        int i, k;
        Console.WriteLine("Enter two integers \n");
        i = int.Parse(Console.ReadLine());
        k = int.Parse(Console.ReadLine());
        Console.WriteLine("\n Before swapping i= {0} and k = {1}", i, k);
        i = i ^ k;
        k = i ^ k;
        i = i ^ k;
        Console.WriteLine("\n After swapping i= {0} and k = {1}", i, k);
        Console.ReadLine();
    }
}