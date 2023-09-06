#pragma once

#include "chromosome.hpp"
#include "instance/instance.hpp"

namespace mofjssp {

class Decoder {
    public:
    const Instance & instance;

    std::vector<std::vector<std::vector<unsigned>>>
        machine_of_operation_of_thread;

    std::vector<std::vector<std::vector<std::pair<unsigned, unsigned>>>>
        operations_of_machine_of_thread;

    std::vector<std::vector<std::vector<double>>>
        starting_time_of_operation_of_thread;

    std::vector<std::vector<std::vector<double>>>
        ending_time_of_operation_of_thread;

    std::vector<std::vector<double>> value_of_thread;

    std::vector<std::vector<std::pair<double, unsigned>>> permutation_of_thread;

    std::vector<std::vector<unsigned>> num_scheduled_operations_of_job_of_thread;

    Decoder(const Instance & instance, unsigned num_threads);

    std::vector<double> decode(NSBRKGA::Chromosome & chromosome, bool rewrite);
};

}
