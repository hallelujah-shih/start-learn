#include <cstdlib>
#include <iostream>
#include <string>

void *operator new(std::size_t n) 
{
	std::cout << "[Allocating " << n << " bytes]";
	return malloc(n);
}

void operator delete(void *p) throw()
{
	free(p);
}

int main(void)
{
	// 测试不同大小字符串在不同编译器下的处理方式（分配内存大小）
	for (std::size_t i = 0; i < 24; ++i)
	{
		std::cout << i << ": " << std::string(i, '=')  << std::endl;
	}

	// 测试是否是copy on write
	std::string a(50, 'c');
	std::cout << std::endl;
	std::string b = a;
	std::cout << std::endl;

	*const_cast<char *>(a.c_str()) = 'A';
	std::cout << "a: " << a << "\nb: " << b << std::endl;

	// 内存分配策略测试
	for (size_t i = 0; i < 1000000; ++i)
	{
		std::string s(i, '=');
		std::cout << i << std::endl;
	}

	return 0;
}