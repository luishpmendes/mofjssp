#include "solver/nsbrkga/decoder.hpp"
#include <algorithm>
#include <limits>

namespace mofjssp {

Decoder::Decoder(const Instance & instance,
                 unsigned num_threads)
    : instance(instance),
      machine_of_operation_of_thread(num_threads,
                                     std::vector<std::vector<unsigned>>(
                                            instance.num_jobs)),
      operations_of_machine_of_thread(
            num_threads,
            std::vector<std::vector<std::pair<unsigned, unsigned>>>(
                    instance.num_machines)),
      starting_time_of_operation_of_thread(num_threads,
                                           std::vector<std::vector<double>>(
                                                instance.num_jobs)),
      ending_time_of_operation_of_thread(num_threads,
                                           std::vector<std::vector<double>>(
                                                instance.num_jobs)),
      value_of_thread(num_threads,
                      std::vector<double>(instance.num_objectives)),
      permutation_of_thread(num_threads,
                            std::vector<std::pair<double, unsigned>>(
                                    instance.total_num_operations)),
      num_scheduled_operations_of_job_of_thread(num_threads,
                                                std::vector<unsigned>(
                                                        instance.num_jobs, 0)) {
    for (unsigned thread = 0; thread < num_threads; thread++) {
        for (unsigned job = 0; job < this->instance.num_jobs; job++) {
            this->machine_of_operation_of_thread[thread][job].resize(
                this->instance.num_operations[job]);
            this->starting_time_of_operation_of_thread[thread][job].resize(
                this->instance.num_operations[job]);
            this->ending_time_of_operation_of_thread[thread][job].resize(
                this->instance.num_operations[job]);
        }

        for (unsigned machine = 0;
            machine < this->instance.num_machines;
            machine++) {
            this->operations_of_machine_of_thread[thread][machine].reserve(
                    this->instance.operations_of_machine[machine].size());
        }
    }
}

std::vector<double> Decoder::decode(NSBRKGA::Chromosome & chromosome,
                                    bool /* not used */) {
#   ifdef _OPENMP
        std::vector<std::vector<unsigned>> & machine_of_operation =
            this->machine_of_operation_of_thread[omp_get_thread_num()];
        std::vector<std::vector<std::pair<unsigned, unsigned>>> &
            operations_of_machine =
                this->operations_of_machine_of_thread[omp_get_thread_num()];
        std::vector<std::vector<double>> & starting_time_of_operation =
            this->starting_time_of_operation_of_thread[omp_get_thread_num()];
        std::vector<std::vector<double>> & ending_time_of_operation = 
            this->ending_time_of_operation_of_thread[omp_get_thread_num()];
        std::vector<double> & value =
            this->value_of_thread[omp_get_thread_num()];
        std::vector<std::pair<double, unsigned>> & permutation = 
            this->permutation_of_thread[omp_get_thread_num()];
        std::vector<unsigned> & num_scheduled_operations_of_job =
            this->num_scheduled_operations_of_job_of_thread[
                omp_get_thread_num()];
#   else
        std::vector<std::vector<unsigned>> & machine_of_operation =
            this->machine_of_operation_of_thread.front();
        std::vector<std::vector<std::pair<unsigned, unsigned>>> &
            operations_of_machine =
                this->operations_of_machine_of_thread.front();
        std::vector<std::vector<double>> & starting_time_of_operation =
            this->starting_time_of_operation_of_thread.front();
        std::vector<std::vector<double>> & ending_time_of_operation =
            this->ending_time_of_operation_of_thread.front();
        std::vector<double> & value = this->value_of_thread.front();
        std::vector<std::pair<double, unsigned>> & permutation =
            this->permutation_of_thread.front();
        std::vector<unsigned> & num_scheduled_operations_of_job =
            this->num_scheduled_operations_of_job_of_thread.front();
#   endif

    for (unsigned machine = 0;
        machine < this->instance.num_machines;
        machine++) {
        operations_of_machine[machine].clear();
        operations_of_machine[machine].reserve(
                this->instance.operations_of_machine[machine].size());
    }

    // Uses the first half of the chromosome to compute the machine that will 
    // process each operation
    for (unsigned job = 0, i = 0; job < this->instance.num_jobs; job++) {
        for (unsigned operation = 0;
             operation < this->instance.num_operations[job];
             operation++, i++) {
            const unsigned num_machines_of_operation =
                    this->instance.machines_of_operation[job][operation].size();
            const double delta = 1.0 / ((double) num_machines_of_operation);
            auto machine_iterator =
                this->instance.machines_of_operation[job][operation].begin();

            for (double j = delta;
                 j + std::numeric_limits<double>::epsilon() < chromosome[i];
                 j += delta) {
                machine_iterator++;
            }

            machine_of_operation[job][operation] = *machine_iterator;
        }
    }

    // Uses the second half of the chromosome to compute the order that each 
    // operation will be processed
    for (unsigned job = 0, i = 0; job < this->instance.num_jobs; job++) {
        for (unsigned operation = 0;
             operation < this->instance.num_operations[job];
             operation++, i++) {
            permutation[i] = std::make_pair(
                    chromosome[this->instance.total_num_operations + i], job);
        }
    }

    std::sort(permutation.begin(), permutation.end());

    num_scheduled_operations_of_job.assign(this->instance.num_jobs, 0);

    for (unsigned i = 0; i < permutation.size(); i++) {
        const unsigned job = permutation[i].second,
                       operation = num_scheduled_operations_of_job[job],
                       machine = machine_of_operation[job][operation];
        double starting_time = 0.0,
               ending_time = 0.0;

        if (operation > 0) {
            starting_time = ending_time_of_operation[job][operation - 1];
        }

        if (!operations_of_machine[machine].empty() && 
            starting_time < ending_time_of_operation
                [operations_of_machine[machine].back().first]
                [operations_of_machine[machine].back().second]) {
            starting_time = ending_time_of_operation
                            [operations_of_machine[machine].back().first]
                            [operations_of_machine[machine].back().second];
        }

        ending_time = starting_time + this->instance.processing_time.at(
                std::make_tuple(job, operation, machine));

        operations_of_machine[machine].push_back(std::make_pair(job, operation));
        
        starting_time_of_operation[job][operation] = starting_time;
        ending_time_of_operation[job][operation] = ending_time;

        num_scheduled_operations_of_job[job]++;
    }

    // Computes the makespan and the total completion time
    value[0] = 0.0;
    value[1] = 0.0;

    for (unsigned job = 0; job < this->instance.num_jobs; job++) {
        if (value[0] < ending_time_of_operation[job].back()) {
            value[0] = ending_time_of_operation[job].back();
        }

        value[1] += ending_time_of_operation[job].back();
    }

    // Computes the maximal machine workload
    // and the total workload of the machines
    value[2] = 0.0;
    value[3] = 0.0;

    for (unsigned machine = 0;
         machine < this->instance.num_machines;
         machine++) {
        double workload = 0.0;

        for (const auto & [job, operation] : operations_of_machine[machine]) {
            workload += this->instance.processing_time.at(
                    std::make_tuple(job, operation, machine));
        }

        if (value[2] < workload) {
            value[2] = workload;
        }

        value[3] += workload;
    }

    return value;
}

}
