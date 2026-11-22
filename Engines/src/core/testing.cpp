#include "binary_processing.hpp"
#include <iostream>
#include <string>

int main(){
    std::string f = "Test";

    auto filetype = analyse_filetype(f);
    if (filetype.has_value()){
        std::cout << *filetype << std::endl;
    } else {
        std::cout << "unknown filetype" << std::endl;
    }
    return 0;
}
