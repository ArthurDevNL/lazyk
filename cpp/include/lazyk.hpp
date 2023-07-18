#pragma once  
  
#include <optional>  
  
class Generator {  
public:  
    Generator(int start, int step);  
    std::optional<int> next();  
    Generator& operator++();  
  
private:  
    int m_current;  
    int m_step;  
};  
