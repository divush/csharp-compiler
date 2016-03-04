using System;
namespace RectangleApplication
{
   class Rectangle 
   {
      /* member variables */
      double length;
      double width;
      void Acceptdetails()
      {
         length = 4;    
         width = 3;
      }
      
      double GetArea()
      {
         return length * width; 
      }
      
      void Display()
      {
         Console.WriteLine("Length: {0}", length);
         Console.WriteLine("Width: {0}", width);
         Console.WriteLine("Area: {0}", GetArea());
      }
   }
   
   class ExecuteRectangle 
   {
      void Main(string[] args) 
      {
         Rectangle r = new Rectangle();
         r.Acceptdetails();
         r.Display();
         Console.ReadLine(); 
      }
   }
}