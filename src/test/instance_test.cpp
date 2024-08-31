#include "instance/instance.hpp"
#include <cassert>
#include <fstream>
#include <iostream>

int main() {
    std::ifstream ifs;
    mofjssp::Instance instance;

    for (const std::string filename : {"instances/mk01.txt",
                                       "instances/mk02.txt",
                                       "instances/mk03.txt",
                                       "instances/mk04.txt",
                                       "instances/mk05.txt",
                                       "instances/mk06.txt",
                                       "instances/mk07.txt",
                                       "instances/mk08.txt",
                                       "instances/mk09.txt",
                                       "instances/mk10.txt",
                                       "instances/mk11.txt",
                                       "instances/mk12.txt",
                                       "instances/mk13.txt",
                                       "instances/mk14.txt",
                                       "instances/mk15.txt"}) {
        std::cout << filename << std::endl;

        ifs.open(filename);

        assert(ifs.is_open());

        ifs >> instance;

        ifs.close();

        assert(instance.is_valid());

        assert(instance.primal_bound[2] >= 37);
    }

    std::cout << std::endl << "Instance Test PASSED" << std::endl;

    return 0;
}
