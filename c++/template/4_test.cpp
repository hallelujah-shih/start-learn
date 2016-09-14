/*
 * =====================================================================================
 *
 *       Filename:  4_test.cpp
 *
 *    Description:  
 *
 *        Version:  1.0
 *        Created:  09/13/2016 11:20:16 AM
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  shih (Hallelujah), sh19871122@gmail.com
 *   Organization:  
 *
 * =====================================================================================
 */

#include <vector>
#include <iostream>
#include <algorithm>

template<typename T, int VAL>
T add_value(const T& t)
{
    return t + VAL;
}

template<const char *name>
class MyClass
{
public:
    MyClass()
    {
        std::cout << name << std::endl;
    }
};

// char const* s = "hello";
extern const char s[] = "hello";

template<int buf[5]>
class MyClass1 
{
};

int main(void)
{
    MyClass<s> s1;
    std::vector<int> v1;
    for (int i = 0; i < 10; i++)
        v1.push_back(i);

    std::transform(v1.begin(), v1.end(), v1.begin(), add_value<int, 5>);
    // std::transform(v1.begin(), v1.end(), v1.begin(), (int (*)(const int &))add_value<int, 5>);

    for (std::vector<int>::iterator it=v1.begin(); it != v1.end(); it++)
    {
        std::cout << *it << std::endl;
    }
    return 0;
}

