#include <stdint.h>
#include <vector>
#include <string>
#include <iterator>
#include <algorithm>
#include <iostream>
#include <numeric>
#include <functional>

template<typename C>
void print(const C &data)
{
	for (auto it = std::cbegin(data); it != std::cend(data); ++it)
	{
		std::cout << *it << " ";
	}
	std::cout << std::endl;
}

int main(int argc, char *argv[])
{
	std::vector<uint32_t> vec{ 1, 2, 3, 4, 5, 6, 7, 8, 9 };
	std::vector<std::string> str{ "programming", "in", "a", "functional", "style" };
	std::vector<uint32_t> vec1;

	// map
	std::transform(std::begin(vec), std::end(vec), std::begin(vec), [](uint32_t i) {
		return i * i;
	});
	std::transform(std::begin(str), std::end(str), std::back_inserter(vec1), [](std::string s) {
		return s.length();
	});

	std::cout << "print vec" << std::endl;
	print(vec);
	std::cout << "print vec1" << std::endl;
	print(vec1);

	// filter
	vec.erase(std::remove_if(std::begin(vec), std::end(vec), [](int i) {return ((i <= 10) || (i >= 30)); }), std::end(vec));
	std::cout << "print vec filter:" << std::endl;
	print(vec);
	
	// reduce
	std::string rt = std::accumulate(std::next(std::begin(str)), std::end(str), *str.begin(), [](std::string a, std::string b){
		return a + ":" + b;
	});
	std::cout << rt << std::endl;

	return 0;
}