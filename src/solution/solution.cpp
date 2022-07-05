#include "solution/solution.hpp"

#include <algorithm>
#include <cmath>

namespace mofjssp {

bool Solution::dominates(const std::vector<double> & valueA,
                         const std::vector<double> & valueB) {
    if (valueA.size() != 3 || valueB.size() != 3) {
        return false;
    }

    // Checks if valueA is at least as good as valueB
    for (unsigned i = 0; i < valueA.size(); i++) {
        if (valueA[i] > valueB[i] + std::numeric_limits<double>::epsilon()) {
            return false;
        }
    }

    // Checks if valueA is better than valueB
    for (unsigned i = 0; i < valueA.size(); i++) {
        if (valueA[i] < valueB[i] - std::numeric_limits<double>::epsilon()) {
            return true;
        }
    }

    return false;
}

void Solution::compute_value() {
    // Computes the makespan
    this->value[0] = 0.0;

    for (unsigned job = 0; job < this->instance.num_jobs; job++) {
        if (this->value[0] < this->ending_time_of_operation[job].back()) {
            this->value[0] = this->ending_time_of_operation[job].back();
        }
    }

    // Computes the total workload of the machines
    this->value[1] = 0.0;

    for (unsigned machine = 0;
         machine < this->instance.num_machines;
         machine++) {
        double workload = 0.0;

        for (const auto & [job, operation] :
                this->operations_of_machine[machine]) {
            workload += this->instance.processing_time.at(
                    std::make_tuple(job, operation, machine));
        }

        this->value[1] += workload;
    }

    // Computes the maximal machine workload
    this->value[2] = 0.0;

    for (unsigned machine = 0;
         machine < this->instance.num_machines;
         machine++) {
        double workload = 0.0;

        for (const auto & [job, operation] :
                this->operations_of_machine[machine]) {
            workload += this->instance.processing_time.at(
                    std::make_tuple(job, operation, machine));
        }

        if (this->value[2] < workload) {
            this->value[2] = workload;
        }
    }
}

void Solution::init() {
    // Computes the operations processed by each machine and 
    // the time that each operations of each job ends processing
    for (unsigned job = 0; job < this->instance.num_jobs; job++) {
        for (unsigned operation = 0;
             operation < this->instance.num_operations[job];
             operation++) {
            const unsigned machine = this->machine_of_operation[job][operation];
            const double starting_time = this->starting_time_of_operation[job][operation],
                         processing_time = this->instance.processing_time.at(
                                std::make_tuple(job, operation, machine)),
                         ending_time = starting_time + processing_time;

            this->operations_of_machine[machine].push_back(
                    std::make_pair(job, operation));
            this->ending_time_of_operation[job][operation] = ending_time;
        }
    }

    this->compute_value();
}

Solution::Solution(const Instance & instance,
                   const std::vector<std::vector<unsigned>> & machine_of_operation,
                   const std::vector<std::vector<double>> & starting_time_of_operation) :
        Solution(instance) {
    this->init();
}

Solution::Solution(const Instance & instance,
                   const std::vector<double> & key) :
        Solution(instance) {
    std::vector<std::pair<double, unsigned>> permutation(
            this->instance.total_num_operations);

    // Uses the first half of the key to compute the machine that will 
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
                 j + std::numeric_limits<double>::epsilon() < key[i];
                 j += delta) {
                machine_iterator++;
            }

            this->machine_of_operation[job][operation] = *machine_iterator;
        }
    }

    // Uses the second half of the key to compute the order that each 
    // operation will be processed
    for (unsigned job = 0, i = 0; job < this->instance.num_jobs; job++) {
        for (unsigned operation = 0;
             operation < this->instance.num_operations[job];
             operation++, i++) {
            permutation[i] = std::make_pair(
                    key[this->instance.total_num_operations + i], job);
        }
    }

    std::sort(permutation.begin(), permutation.end());

    std::vector<unsigned> num_scheduled_operations_of_job(
            this->instance.num_jobs, 0);
    
    for (unsigned i = 0; i < permutation.size(); i++) {
        const unsigned job = permutation[i].second,
                       operation = num_scheduled_operations_of_job[job],
                       machine = this->machine_of_operation[job][operation];
        double starting_time = 0.0,
               ending_time = 0.0;

        if (operation > 0) {
            starting_time = this->ending_time_of_operation[job][operation - 1];
        }

        if (!this->operations_of_machine[machine].empty() && 
            starting_time < this->ending_time_of_operation
                [this->operations_of_machine[machine].back().first]
                [this->operations_of_machine[machine].back().second]) {
            starting_time = this->ending_time_of_operation
                            [this->operations_of_machine[machine].back().first]
                            [this->operations_of_machine[machine].back().second];
        }

        ending_time = starting_time + this->instance.processing_time.at(
                std::make_tuple(job, operation, machine));

        this->operations_of_machine[machine].push_back(
                std::make_pair(job, operation));
        
        this->starting_time_of_operation[job][operation] = starting_time;
        this->ending_time_of_operation[job][operation] = ending_time;

        num_scheduled_operations_of_job[job]++;
    }

    this->compute_value();
}

Solution::Solution(const Instance & instance) :
        instance(instance),
        machine_of_operation(instance.num_jobs),
        operations_of_machine(instance.num_machines),
        starting_time_of_operation(instance.num_jobs),
        ending_time_of_operation(instance.num_jobs),
        value(3) {
    for (unsigned job = 0; job < this->instance.num_jobs; job++) {
        this->machine_of_operation[job].resize(
            this->instance.num_operations[job]);
        this->starting_time_of_operation[job].resize(
            this->instance.num_operations[job]);
        this->ending_time_of_operation[job].resize(
            this->instance.num_operations[job]);
    }

    for (unsigned machine = 0;
         machine < this->instance.num_machines;
         machine++) {
        this->operations_of_machine[machine].reserve(
                this->instance.operations_of_machine[machine].size());
    }
}

bool Solution::is_feasible() const {
    if (!this->instance.is_valid()) {
        return false;
    }

    if (this->machine_of_operation.size() != this->instance.num_jobs) {
        return false;
    }

    if (this->operations_of_machine.size() != this->instance.num_machines) {
        return false;
    }

    if (this->starting_time_of_operation.size() != this->instance.num_jobs) {
        return false;
    }

    if (this->ending_time_of_operation.size() != this->instance.num_jobs) {
        return false;
    }

    if (this->value.size() != 3) {
        return false;
    }

    for (unsigned job = 0; job < this->instance.num_jobs; job++) {
        if (this->machine_of_operation[job].size() !=
            this->instance.num_operations[job]) {
            return false;
        }

        if (this->starting_time_of_operation[job].size() !=
            this->instance.num_operations[job]) {
            return false;
        }

        if (this->ending_time_of_operation[job].size() !=
            this->instance.num_operations[job]) {
            return false;
        }
    }

    for (unsigned machine = 0;
         machine < this->instance.num_machines;
         machine++) {
        if (this->operations_of_machine[machine].size() >
            this->instance.operations_of_machine[machine].size()) {
            return false;
        }
    }

    // Checks if the content of machine_of_operation matches
    // with the content of operations_of_machine
    for (unsigned job = 0; job < this->instance.num_jobs; job++) {
        for (unsigned operation = 0;
             operation < this->instance.num_operations[job];
             operation++) {
            const unsigned machine = this->machine_of_operation[job][operation];

            if (machine >= this->instance.num_machines) {
                return false;
            }

            if (std::find(this->operations_of_machine[machine].begin(),
                          this->operations_of_machine[machine].end(),
                          std::make_pair(job, operation)) ==
                    this->operations_of_machine[machine].end()) {
                return false;
            }
        }
    }

    // Checks if the content of operations_of_machine matches
    // with the content of machine_of_operation
    for (unsigned machine = 0;
         machine < this->instance.num_machines;
         machine++) {
        for (const auto & [job, operation] :
                this->operations_of_machine[machine]) {
            if (this->machine_of_operation[job][operation] != machine) {
                return false;
            }
        }
    }

    // Checks if the starting time of each operation is non-negative
    for (unsigned job = 0; job < this->instance.num_jobs; job++) {
        for (unsigned operation = 0;
             operation < this->instance.num_operations[job];
             operation++) {
            if (this->starting_time_of_operation[job][operation] < 0) {
                return false;
            }
        }
    }

    // Checks if the ending time of each operation is equal
    // to its starting time plus the processing time
    for (unsigned job = 0; job < this->instance.num_jobs; job++) {
        for (unsigned operation = 0;
             operation < this->instance.num_operations[job];
             operation++) {
            const unsigned machine = this->machine_of_operation[job][operation];

            if (fabs(this->starting_time_of_operation[job][operation] +
                     this->instance.processing_time.at(
                        std::make_tuple(job, operation, machine)) -
                     this->ending_time_of_operation[job][operation]) >
                        std::numeric_limits<double>::epsilon()) {
                return false;
            }
        }
    }

    // Checks if the ending time of each operation of a job is no greater
    // than the starting time of the next operation of the same job
    for (unsigned job = 0; job < this->instance.num_jobs; job++) {
        for (unsigned operation = 0;
             operation + 1 < this->instance.num_operations[job];
             operation++) {
            if (this->ending_time_of_operation[job][operation] >
                    this->starting_time_of_operation[job][operation + 1]) {
                return false;
            }
        }
    }

    // Checks if the ending time of each operation of a machine is no greater
    // than the starting time of the next operation of the same machine
    for (unsigned machine = 0;
         machine < this->instance.num_machines;
         machine++) {
        for (unsigned i = 0;
             i + 1 < this->operations_of_machine[machine].size();
             i++) {
            const unsigned job = this->operations_of_machine[machine][i].first;
            const unsigned operation = this->operations_of_machine[machine][i].second;
            const unsigned next_job = this->operations_of_machine[machine][i + 1].first;
            const unsigned next_operation = this->operations_of_machine[machine][i + 1].second;
            
            if (this->ending_time_of_operation[job][operation] >
                    this->starting_time_of_operation[next_job][next_operation]) {
                return false;
            }
        }
    }

    // Checks if the starting time of each operation is equal to the ending 
    // time of the previos operation of the same job or of the same machine
    for (unsigned machine = 0;
         machine < this->instance.num_machines;
         machine++) {
        if (!this->operations_of_machine[machine].empty()) {
            const auto & [first_job, first_operation] =
                    this->operations_of_machine[machine].front();

            if (first_operation != 0 &&
                fabs(this->starting_time_of_operation[first_job][first_operation] -
                    this->ending_time_of_operation[first_job][first_operation - 1])
                        > std::numeric_limits<double>::epsilon()) {
                return false;
            }

            for (unsigned i = 1;
                i < this->operations_of_machine[machine].size();
                i++) {
                const auto & [job, operation] =
                        this->operations_of_machine[machine][i];
                const auto & [prev_job, prev_operation] =
                        this->operations_of_machine[machine][i - 1];

                if ((operation != 0 &&
                    fabs(this->starting_time_of_operation[job][operation]
                    - this->ending_time_of_operation[job][operation - 1])
                    > std::numeric_limits<double>::epsilon()) &&
                    fabs(this->starting_time_of_operation[job][operation]
                    - this->ending_time_of_operation[prev_job][prev_operation])
                    > std::numeric_limits<double>::epsilon()) {
                    return false;
                }
            }
        }
    }

    for (unsigned job = 0; job < this->instance.num_jobs; job++) {
        if (this->value[0] < this->ending_time_of_operation[job].back()) {
            return false;
        }
    }

    if (this->value[0] > this->value[1]) {
        return false;
    }

    if (this->value[0] < this->value[2]) {
        return false;
    }

    for (unsigned i = 0; i < 3; i++) {
        if (this->value[i] > this->instance.upper_bound[i]) {
            return false;
        }
    }

    return true;
}

bool Solution::dominates(const Solution & solution) const {
    return Solution::dominates(this->value, solution.value);
}

std::istream & operator >>(std::istream & is, Solution & solution) {
    for (unsigned job = 0; job < solution.instance.num_jobs; job++) {
        solution.machine_of_operation[job].resize(
                solution.instance.num_operations[job]);
        solution.starting_time_of_operation[job].resize(
                solution.instance.num_operations[job]);
        
        for (unsigned operation = 0;
             operation < solution.instance.num_operations[job];
             operation++) {
            is >> solution.machine_of_operation[job][operation];
            is >> solution.starting_time_of_operation[job][operation];
        }
    }

    solution.init();

    return is;
}

std::ostream & operator <<(std::ostream & os, Solution & solution) {
    for (unsigned job = 0; job < solution.instance.num_jobs; job++) {
        for (unsigned operation = 0;
             operation < solution.instance.num_operations[job];
             operation++) {
            os << solution.machine_of_operation[job][operation] << ' '
               << solution.starting_time_of_operation[job][operation] << std::endl;
        }
    }

    return os;
}

}
