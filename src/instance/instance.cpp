#include "instance/instance.hpp"
#include <algorithm>
#include <limits>

namespace mofjssp {

void Instance::compute_primal_bound() {
    double max_processing_time = 0.0;
    std::vector<double> working_time(this->num_machines, 0.0);

    this->primal_bound.resize(this->num_objectives, 0.0);
    this->primal_bound.assign(this->num_objectives, 0.0);

    for (const auto & [key, value] : this->processing_time) {
        const unsigned machine = std::get<2>(key);

        max_processing_time = std::max(max_processing_time, value);
        working_time[machine] += value;
    }

    this->primal_bound[0] = this->total_num_operations * max_processing_time;
    this->primal_bound[1] = this->num_jobs * this->total_num_operations * max_processing_time;

    for (unsigned machine = 0; machine < this->num_machines; machine++) {
        this->primal_bound[2] = std::max(this->primal_bound[2], working_time[machine]);
        this->primal_bound[3] += working_time[machine];
    }
}

Instance::Instance(const std::map<std::tuple<unsigned, unsigned, unsigned>, double> & processing_time) : 
        processing_time(processing_time),
        num_objectives(4),
        senses(4, NSBRKGA::Sense::MINIMIZE),
        primal_bound(num_objectives, 0.0) {
    std::vector<unsigned> jobs;
    std::vector<std::vector<unsigned>> operations;
    std::vector<unsigned> machines;

    for (const auto & [key, value] : this->processing_time) {
        const unsigned job = std::get<0>(key),
                       machine = std::get<2>(key);

        jobs.push_back(job);
        machines.push_back(machine);
    }

    this->num_jobs = jobs.size();
    this->num_machines = machines.size();
    this->num_operations.resize(this->num_jobs, 0);
    this->num_operations.assign(this->num_jobs, 0);
    this->total_num_operations = 0;
    this->machines_of_operation.resize(this->num_jobs,
                                       std::vector<std::vector<unsigned>>());
    this->machines_of_operation.assign(this->num_jobs,
                                       std::vector<std::vector<unsigned>>());
    this->operations_of_machine.resize(this->num_machines,
                                       std::vector<std::pair<unsigned, unsigned>>());
    this->operations_of_machine.assign(this->num_machines,
                                       std::vector<std::pair<unsigned, unsigned>>());

    operations.resize(jobs.size(), std::vector<unsigned>());
    operations.assign(jobs.size(), std::vector<unsigned>());

    for (const auto & [key, value] : this->processing_time) {
        const unsigned job = std::get<0>(key),
                       operation = std::get<1>(key);

        operations[job].push_back(operation);
    }

    for (unsigned job : jobs) {
        this->num_operations[job] = operations[job].size();
        this->total_num_operations += this->num_operations[job];
        this->machines_of_operation[job].resize(this->num_operations[job],
                                                std::vector<unsigned>());
        this->machines_of_operation[job].assign(this->num_operations[job],
                                                std::vector<unsigned>());
    }

    for (const auto & [key, value] : this->processing_time) {
        const unsigned job = std::get<0>(key),
                       operation = std::get<1>(key),
                       machine = std::get<2>(key);

        this->machines_of_operation[job][operation].push_back(machine);
        this->operations_of_machine[machine].push_back(std::make_pair(job,
                                                                      operation));
    }

    this->compute_primal_bound();
}

Instance::Instance(const Instance & instance) = default;

Instance::Instance() = default;

Instance Instance::operator = (const Instance & instance) {
    this->processing_time = instance.processing_time;
    this->num_jobs = instance.num_jobs;
    this->num_machines = instance.num_machines;
    this->num_operations = instance.num_operations;
    this->total_num_operations = instance.total_num_operations;
    this->machines_of_operation = instance.machines_of_operation;
    this->operations_of_machine = instance.operations_of_machine;
    this->processing_time = instance.processing_time;
    this->num_objectives = 4;
    this->senses = std::vector<NSBRKGA::Sense>(this->num_objectives, NSBRKGA::Sense::MINIMIZE);
    this->primal_bound = instance.primal_bound;
    return *this;
}

bool Instance::is_valid() const {
    if (this->num_jobs == 0) {
        return false;
    }

    if (this->num_machines == 0) {
        return false;
    }

    if (this->total_num_operations == 0) {
        return false;
    }

    for (unsigned job = 0; job < this->num_jobs; job++) {
        if (this->num_operations[job] == 0) {
            return false;
        }
    }

    for (unsigned job = 0; job < this->num_jobs; job++) {
        for (unsigned operation = 0; operation < this->num_operations[job]; operation++) {
            if (this->machines_of_operation[job][operation].empty()) {
                return false;
            }
        }
    }

    for (unsigned job = 0; job < this->num_jobs; job++) {
        for (unsigned operation = 0; operation < this->num_operations[job]; operation++) {
            for (unsigned machine : this->machines_of_operation[job][operation]) {
                if (std::find(this->operations_of_machine[machine].begin(), 
                              this->operations_of_machine[machine].end(),
                              std::make_pair(job, operation)) == 
                                    this->operations_of_machine[machine].end()) {
                    return false;
                }
            }
        }
    }

    for (unsigned machine = 0; machine < this->num_machines; machine++) {
        for (const auto & [job, operation] : this->operations_of_machine[machine]) {
            if (std::find(this->machines_of_operation[job][operation].begin(),
                          this->machines_of_operation[job][operation].end(),
                          machine) == 
                                this->machines_of_operation[job][operation].end()) {
                return false;
            }
        }
    }

    for (const auto & [key, value] : this->processing_time) {
        if (value < std::numeric_limits<double>::epsilon()) {
            return false;
        }
    }

    for (unsigned job = 0; job < this->num_jobs; job++) {
        for (unsigned operation = 0; operation < this->num_operations[job]; operation++) {
            for (unsigned machine : this->machines_of_operation[job][operation]) {
                if (this->processing_time.count(std::make_tuple(job, operation, machine)) == 0) {
                    return false;
                }
            }
        }
    }

    for (const auto & [key, value] : this->processing_time) {
        const unsigned job = std::get<0>(key),
                       operation = std::get<1>(key),
                       machine = std::get<2>(key);

        if (std::find(this->machines_of_operation[job][operation].begin(),
                      this->machines_of_operation[job][operation].end(),
                      machine) == 
                            this->machines_of_operation[job][operation].end()) {
            return false;
        }
    }

    for (unsigned machine = 0; machine < this->num_machines; machine++) {
        for (const auto & [job, operation] : this->operations_of_machine[machine]) {
            if (this->processing_time.count(std::make_tuple(job, operation, machine)) == 0) {
                return false;
            }
        }
    }

    for (const auto & [key, value] : this->processing_time) {
        const unsigned job = std::get<0>(key),
                       operation = std::get<1>(key),
                       machine = std::get<2>(key);

        if (std::find(this->operations_of_machine[machine].begin(),
                      this->operations_of_machine[machine].end(),
                      std::make_pair(job, operation)) == 
                            this->operations_of_machine[machine].end()) {
            return false;
        }
    }

    if (this->num_objectives != 4) {
        return false;
    }

    if (this->primal_bound.size() != this->num_objectives) {
        return false;
    }

    for (const double & coordinate : this->primal_bound) {
        if (coordinate < 0.0) {
            return false;
        }
    }

    return true;
}

std::istream & operator >>(std::istream & is, Instance & instance) {
    is >> instance.num_jobs >> instance.num_machines;

    instance.num_operations.resize(instance.num_jobs, 0);
    instance.num_operations.assign(instance.num_jobs, 0);
    instance.total_num_operations = 0;
    instance.machines_of_operation.resize(instance.num_jobs,
                                          std::vector<std::vector<unsigned>>());
    instance.machines_of_operation.assign(instance.num_jobs,
                                          std::vector<std::vector<unsigned>>());
    instance.operations_of_machine.resize(instance.num_machines,
                                          std::vector<std::pair<unsigned, unsigned>>());
    instance.operations_of_machine.assign(instance.num_machines, 
                                          std::vector<std::pair<unsigned, unsigned>>());
    instance.processing_time.clear();
    instance.num_objectives = 4;
    instance.senses = std::vector<NSBRKGA::Sense>(instance.num_objectives, NSBRKGA::Sense::MINIMIZE);

    for (unsigned job = 0; job < instance.num_jobs; job++) {
        is >> instance.num_operations[job];
        instance.total_num_operations += instance.num_operations[job];

        instance.machines_of_operation[job].resize(instance.num_operations[job],
                                                   std::vector<unsigned>());
        instance.machines_of_operation[job].assign(instance.num_operations[job],
                                                   std::vector<unsigned>());

        for (unsigned operation = 0; operation < instance.num_operations[job]; operation++) {
            unsigned num_machines_of_operation;

            is >> num_machines_of_operation;

            while (num_machines_of_operation--) {
                unsigned machine;
                double processing_time;

                is >> machine >> processing_time;

                instance.machines_of_operation[job][operation].push_back(machine);
                instance.operations_of_machine[machine].push_back(std::make_pair(job, operation));
                instance.processing_time[std::make_tuple(job, operation, machine)] = processing_time;
            }
        }
    }

    instance.compute_primal_bound();

    return is;
}

std::ostream & operator <<(std::ostream & os, const Instance & instance) {
    os << instance.num_jobs << instance.num_machines << std::endl;

    for (unsigned job = 0; job < instance.num_jobs; job++) {
        os << instance.num_operations[job];

        for (unsigned operation = 0; operation < instance.num_operations[job]; operation++) {
            os << ' ' << instance.machines_of_operation[job][operation].size();

            for (const unsigned & machine : instance.machines_of_operation[job][operation]) {
                os << ' ' << machine + 1 << ' ' << instance.processing_time.at(std::make_tuple(job,
                                                                                               operation,
                                                                                               machine));
            }

            os << std::endl;
        }
    }

    return os;
}

}
