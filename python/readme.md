`gcc -shared -fPIC -I mickey.cpp -o mickey2-0.o`
```
c++ -O3 -Wall -shared -std=c++11 -fPIC `python3 -m pybind11 --includes` mickey.h -o mickey`python3-config --extension-suffix`
```
