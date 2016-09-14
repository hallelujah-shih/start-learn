/*
 * =====================================================================================
 *
 *       Filename:  func_ptr_from_lambda.cpp
 *
 *    Description:  
 *
 *        Version:  1.0
 *        Created:  08/16/2016 10:50:35 AM
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  shih (Hallelujah), sh19871122@gmail.com
 *   Organization:  
 *
 * =====================================================================================
 */

#include <iostream>
#include <functional>
#include <string>

using namespace std;


int main(int argc, const char *argv[])
{
    auto lambda_func = [](int a, float b) {
        cout << "a: " << a << endl;
        cout << "b: " << b << endl;
    };

    auto func_ptr = static_cast<void(*)(int, float)>(lambda_func);
    func_ptr(123, 123.23);

    auto func_function_obj = static_cast<function<void(int, float)>>(lambda_func);
    func_function_obj(234, 321.123);

    return 0;
}

