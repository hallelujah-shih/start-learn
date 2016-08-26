/*
 * =====================================================================================
 *
 *       Filename:  test.cpp
 *
 *    Description:  
 *
 *        Version:  1.0
 *        Created:  08/16/2016 11:01:23 AM
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
#include <stdexcept>
#include <typeinfo>
#include <string>
#include <map>

template<typename Function>
struct function_traits: public function_traits<decltype(&Function::operator())>{};

template<typename ClassType, typename ReturnType, typename... Args>
struct function_traits<ReturnType(ClassType::*)(Args...) const>
{
    typedef ReturnType (*pointer)(Args...);
    typedef std::function<ReturnType(Args...)> function;
};

template<typename Function>
typename function_traits<Function>::pointer to_function_pointer (Function &lambda)
{
    return static_cast<typename function_traits<Function>::pointer>(lambda);
}

template<typename Function>
typename function_traits<Function>::function to_function(Function &lambda)
{
    return static_cast<typename function_traits<Function>::function>(lambda);
}

class CallBack final
{
    struct call_back final
    {
        void *function;
        const std::type_info *signature;
    };

public:
    CallBack(void)
    {}

    ~CallBack(void)
    {
        for (auto entry: call_backs_)
        {
            delete static_cast<std::function<void()>*>(entry.second.function);
        }
    }

    template<typename Function>
    void add(std::string name, Function lambda)
    {
        if (call_backs_.find(name) != call_backs_.end())
        {
            throw std::invalid_argument("the callback already exists!");
        }

        auto function = new decltype(to_function(lambda))(to_function(lambda));
        call_backs_[name].function = static_cast<void *>(function);
        call_backs_[name].signature = &typeid(function);
        std::cout << "add cb name:" << name << " signature:" << call_backs_[name].signature->name() << std::endl;
    }

    void remove(std::string name)
    {
        auto func_pair = call_backs_.find(name);
        if (func_pair == call_backs_.end())
            return;
        call_backs_.erase(func_pair);
        delete static_cast<std::function<void()>*>(func_pair->second.function);
    }

    template<typename... Args>
    void call(std::string name, Args... args)
    {
        auto call_back = call_backs_.at(name);
        auto function = static_cast<std::function<void(Args...)>*>(call_back.function);
        std::cout << "call name: " << name << " type_id:" << typeid(function).name() << std::endl;

        if (typeid(function) != *(call_back.signature))
            throw std::bad_typeid();

        (*function)(args...);
    }

private:
    std::map<std::string, call_back> call_backs_;
};

int main(int argc, const char *argv[])
{
    CallBack cb;

    cb.add("hello", [](int a, int b)
            {
                 std::cout << "a: " << a << std::endl;
                 std::cout << "b: " << b << std::endl;
            });

    cb.call("hello", 123, 234);

    cb.remove("hello");

    cb.add("world", [](int a, int b){
            std::cout << a + b << std::endl;
            });

    cb.call("world", 321, 1234);

    return 0;
}
