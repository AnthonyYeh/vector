#include <iostream>
#include <algorithm>
#include <vector>
#include <string>
#include "gnuplot.h"
std::string range(std::vector<double> vals, char type)
{

   std::string str="set ";
   str.append(1, type);
   str.append("range[");
   double max=vals[0];
   double min=vals[0];
   for(int i=1; i<vals.size(); i++)
   {
       if(vals[i]<min){
           min=vals[i];
       }
       if(vals[i]>max){
           max=vals[i];
       }
   }
   str.append(std::to_string(min));
   str.append(":");
   str.append(std::to_string(max));
   str.append("]");
   return str;
}
std::string draw_vector(std::vector<double> a)
{
    std::string str;
    str="set arrow from 0,0,0 to ";
    str.append(std::to_string(a[0]));
    str.append(",");
    str.append(std::to_string(a[1]));
    str.append(",");
    str.append(std::to_string(a[2]));
    return str;
}
double dot_2_vectors(std::vector<double> a, std::vector<double> b)
{
    double sum=0;
    if(a.size()==b.size())
    {
        for(int i=0; i<a.size(); i++)
        {
            sum+=a[i]*b[i];
        }
    }
    return sum;
}

std::vector<double> cross_2_vectors(std::vector<double> a, std::vector<double> b)
{
    std::vector<double> cross_product={0, 0, 0};
    if(a.size()==3&&b.size()==3)
    {
        cross_product[0]=a[1]*b[2]-a[2]*b[1];
        cross_product[1]=a[2]*b[0]-a[0]*b[2];
        cross_product[2]=a[0]*b[1]-a[1]*b[0];
    }
    return cross_product;
}
int main()
{

    std::vector<double> v1={6, 5, 0};
    std::vector<double> v2={4, -3, 0};

    std::cout<<"a dot b = b dot a = "<<dot_2_vectors(v1, v2)<<'\n';

    std::vector<double> cross_product= cross_2_vectors(v1, v2);
    std::cout<<"a cross b = ("<<cross_product[0]<<")*i+("<<cross_product[1]<<")*j+("<<cross_product[2]<<")*k\n";

    GnuplotPipe gp;
    std::vector<double> x_args={v1[0], v2[0], cross_product[0]};
    std::vector<double> y_args={v1[1], v2[1], cross_product[1]};
    std::vector<double> z_args={v1[2], v2[2], cross_product[2]};

    gp.sendLine(range(x_args, 'x'));
    gp.sendLine(range(y_args, 'y'));
    gp.sendLine(range(z_args,  'z'));



    gp.sendLine(draw_vector(v1));
    gp.sendLine(draw_vector(v2));
    gp.sendLine(draw_vector(cross_product));

    gp.sendLine("splot NaN t ''");



    return 0;
}
/* set xrange[0:5]
gnuplot> set yrange[0:5]
gnuplot> set arrow from 0,0 to 3,4
gnuplot> set arrow from 0,0 to 2,5
gnuplot> plot NaN t ''*/