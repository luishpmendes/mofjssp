#include "solution/solution.hpp"
#include <cassert>
#include <fstream>
#include <iostream>
#include <random>

int main() {
    std::ifstream ifs;
    mofjssp::Instance instance;
    std::vector<double> key;
    std::mt19937 rng(2351389233);
    std::uniform_real_distribution<double> distribution(0.0, 1.0);

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

        key.resize(2 * instance.total_num_operations);

        for (double & k : key) {
            k = distribution(rng);
        }

        mofjssp::Solution solution(instance, key);

        assert(solution.is_feasible());

        std::cout << solution << std::endl;
    }

    std::cout << std::endl << "Solution Test PASSED" << std::endl;

    return 0;
}
