#include<iostream>
#include<stdio.h>
#include<string.h>
#include<fstream>
#include<stdlib.h>
#include<vector>
using namespace std;

struct node
{
    string name;
    struct node* next;
    struct node* bef;
};

int main()
{
    fstream infile;
    infile.open("output.txt",ios_base::in);

    fstream outfile;
    outfile.open("for_tree.txt",ios_base::out);

    string word;
    while (infile >> word)
    {
        if(word == "Reduce")
    {
        infile>>word;
        if(word == "rule")
        {
            while(1)
            {
            infile>>word;
            int length = word.length();
            outfile<<word<<" ";
            if(word[length-1] == ']')
            {
                outfile<<"\n";
                break;
            }
            }
        }

    }
    }
    infile.close();
    outfile.close();


    infile.open("for_tree.txt",ios_base::in);

    fstream out_html;
    outfile.open("parser.txt",ios_base::out);

    string a[100000];
    string str ="";
    int i = 0;
    while(infile>>word)
    {
        int length = word.length();

        if(word[length - 1] == ']')
        {
            word = word.substr(0,length);
           str = str +" "+ word;
           a[i] = str;
            i = i + 1;
            continue;
        }


        if(word[0] == '[')
        {
            word = word.substr(1,length - 1);
            str = word;
            continue;
        }

        else
        {
            str = str + " " + word;
        }


    }




    infile.close();
    int j;
    for(j=i-1;j>=0;j--)
    {
           outfile<<a[j]<<"\n";
    }
    outfile.close();

   infile.open("parser.txt",ios_base::in);
   outfile.open("out.txt",ios_base::out);
   out_html.open("right_derivation.html",ios_base::out);
   out_html<<"<!DOCTYPE html>\n";
   out_html<<"<html>\n";
   out_html<<"<body>\n";
   out_html<<"<body bgcolor=\"#000000\">\n";
   out_html<<"<center>\n";
   out_html<<"<h1><font face = \"Segoe Keycaps\" style=\"color:#FF3D1D;\"> RIGHT DERIVATION OF THE PROGRAM</font><h1>\n";



   vector<int> colour;

   vector<string> previous_line;
   string pre;
   pre =  "compilation_unit";
   outfile<<pre<<" ]\n";
   previous_line.push_back(pre);
   int n = 1;
   int l = 1;
   int catch_;
   while(infile>>word)
   {
    for(i=n-1;i>=0;i--)
    {
        if(word == previous_line[i])
        {
            catch_ = i;
            colour.push_back(catch_);
            break;
        }
    }
    l++;

    vector<string> new_line;
    int count_ = 0;
    for(j=0;j<n;j++)
    {
        if(j!=catch_)
        {

        new_line.push_back(previous_line[j]);
        outfile<<previous_line[j]<<" ";
        count_++;
        }
        else
        {
            while(1)
            {
            infile>>word;
            if(word == "->")
            continue;
            if(word[word.length()-1]==']')
            {
            new_line.push_back(word.substr(0,word.length()-1));
            outfile<<word.substr(0,word.length()-1)<<" ";
            count_++;
            break;
            }
            else
            {
            new_line.push_back(word);
            outfile<<word<<" ";
            count_++;
            }
            }
        }

    }
    n = count_;
    outfile<<"]\n";
    previous_line = new_line;
   }
   infile.close();
   outfile.close();

   infile.open("out.txt",ios_base::in);
   i = 0;
   while(infile>>word)
   {

       if(colour[i] == 0)
       {
           out_html<<"<font size = \"2\" face = \"DotumChe\"";
           out_html<<"style=\"color:#9E4CCC;\">";
           out_html<<word<<"&nbsp";
           out_html<<"</font>";

           while(1)
           {

               infile>>word;
               if(word == "]")
               {
                out_html<<"<br>\n";
                break;
               }
               else
               {
               out_html<<"<font size = \"2\" face = \"DotumChe\"";
               out_html<<"style=\"color:#33FF55;\">";
               out_html<<word<<"&nbsp";
               out_html<<"</font>";
               }

           }
           i++;
           continue;

       }
       else
       {
           int toggle = 0;
             while(1)
           {
               if(toggle != colour[i])
               {
               if(word=="]")
                {
                out_html<<"<br>\n";
                break;
                }
               else
               {
               out_html<<"<font size = \"2\" face = \"DotumChe\"";
               out_html<<"style=\"color:#33FF55;\">";
               out_html<<word<<"&nbsp";
               out_html<<"</font>";
               }
               toggle++;
               infile>>word;
               continue;
               }
               else
               {
                if(word=="]")
                {
                    out_html<<"<br>\n";
                    break;
                }
               else
               {
               out_html<<"<font size = \"2\" face = \"DotumChe\"";
               out_html<<"style=\"color:#9E4CCC;\">";
               out_html<<word<<"&nbsp";
               out_html<<"</font>";
               }
               toggle++;
               infile>>word;
               }


           }
           i++;
       }


   }
   out_html<<"</center>\n";
   out_html<<"</body>";
   infile.close();
   out_html.close();
   cout<<"The html file has been created in right_derivation.html\n";
    return 0;
}
