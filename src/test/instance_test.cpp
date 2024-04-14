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
                                       "instances/mk10.txt"}) {
        std::cout << filename << std::endl;

        ifs.open(filename);

        assert(ifs.is_open());

        ifs >> instance;

        ifs.close();

        assert(instance.is_valid());

        assert(instance.primal_bound[2] >= 37);
        std::cout << "primal_bound: " << std::endl;
        for (unsigned i = 0; i < 4; i++) {
            std::cout << (instance.primal_bound[i]) << std::endl;
        }
    }

    std::cout << std::endl << "Instance Test PASSED" << std::endl;

    return 0;
}
