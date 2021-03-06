#include "solver/nsbrkga/nsbrkga_solver.hpp"
#include <cassert>
#include <fstream>
#include <iostream>
#include <random>

int main() {
    std::ifstream ifs;
    mofjssp::Instance instance;
    mofjssp::NSBRKGA_Solver solver;

    for (const std::string & filename : {"instances/mk01.txt",
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

        solver = mofjssp::NSBRKGA_Solver(instance);

        solver.set_seed(2351389233);
        solver.time_limit = 5.0;
        solver.iterations_limit = 100;
        solver.max_num_solutions = 128;
        solver.population_size = 32;
        solver.max_num_snapshots = 16;

        assert(solver.seed = 2351389233);
        assert(fabs(solver.time_limit - 5.0) <
            std::numeric_limits<double>::epsilon());
        assert(solver.iterations_limit == 100);
        assert(solver.max_num_solutions == 128);
        assert(solver.population_size == 32);
        assert(solver.max_num_snapshots == 16);
        assert(fabs(solver.min_elites_percentage - 0.10) <
            std::numeric_limits<double>::epsilon());
        assert(fabs(solver.max_elites_percentage - 0.50) <
            std::numeric_limits<double>::epsilon());
        assert(fabs(solver.mutation_probability - 0.01) <
            std::numeric_limits<double>::epsilon());
        assert(fabs(solver.mutation_distribution - 50.0) <
            std::numeric_limits<double>::epsilon());
        assert(solver.num_total_parents == 3);
        assert(solver.num_elite_parents == 2);
        assert(solver.bias_type == BRKGA::BiasFunctionType::LOGINVERSE);
        assert(solver.diversity_type ==
            BRKGA::DiversityFunctionType::AVERAGE_DISTANCE_TO_CENTROID);
        assert(solver.num_populations == 1);
        assert(solver.pr_number_pairs = 100);
        assert(fabs(solver.pr_min_dist - 0.15) <
            std::numeric_limits<double>::epsilon());
        assert(solver.pr_selection ==
            BRKGA::PathRelinking::Selection::BESTSOLUTION);
        assert(fabs(solver.pr_percentage - 0.31) <
            std::numeric_limits<double>::epsilon());
        assert(solver.pr_interval == 0);
        assert(solver.shake_interval == 200);
        assert(solver.shake_intensity == 10);
        assert(solver.reset_interval == 500);
        assert(fabs(solver.reset_intensity - 0.5) <
            std::numeric_limits<double>::epsilon());
        assert(solver.num_threads == 1);

        solver.solve();

        assert(solver.solving_time > 0);

        assert(solver.num_iterations > 0);
        assert(solver.num_iterations <= solver.iterations_limit);

        assert(solver.best_solutions.size() > 0);
        assert(solver.best_solutions.size() <= solver.max_num_solutions);

        assert(solver.num_snapshots > 0);
        assert(solver.num_snapshots <= solver.max_num_snapshots + 1);

        assert(solver.best_solutions_snapshots.size() == solver.num_snapshots);
        assert(solver.num_non_dominated_snapshots.size() == solver.num_snapshots);
        assert(solver.num_fronts_snapshots.size() == solver.num_snapshots);
        assert(solver.populations_snapshots.size() == solver.num_snapshots);

        for (const auto & s1 : solver.best_solutions) {
            assert(s1.is_feasible());

            for (const auto & s2 : solver.best_solutions) {
                assert(!s1.dominates(s2));
                assert(!s2.dominates(s1));
            }
        }

        for (const auto & snapshot : solver.best_solutions_snapshots) {
            assert(std::get<0>(snapshot) >= 0);
            assert(std::get<0>(snapshot) <= solver.num_iterations);
            assert(std::get<1>(snapshot) >= 0.0);
            assert(std::get<1>(snapshot) <= solver.solving_time);
            assert(std::get<2>(snapshot).size() > 0);
            assert(std::get<2>(snapshot).size() <= solver.max_num_solutions);

            for (const auto & s : std::get<2>(snapshot)) {
                assert(s.size() == 3);
            }
        }

        for (const auto & snapshot : solver.num_non_dominated_snapshots) {
            assert(std::get<0>(snapshot) >= 0);
            assert(std::get<0>(snapshot) <= solver.num_iterations);
            assert(std::get<1>(snapshot) >= 0.0);
            assert(std::get<1>(snapshot) <= solver.solving_time);
            assert(std::get<2>(snapshot).size() > 0);
            assert(std::get<2>(snapshot).size() <= solver.max_num_solutions);

            for (const unsigned & num_non_dominated : std::get<2>(snapshot)) {
                assert(num_non_dominated > 0);
                assert(num_non_dominated <= solver.population_size);
            }
        }

        for (const auto & snapshot : solver.num_fronts_snapshots) {
            assert(std::get<0>(snapshot) >= 0);
            assert(std::get<0>(snapshot) <= solver.num_iterations);
            assert(std::get<1>(snapshot) >= 0.0);
            assert(std::get<1>(snapshot) <= solver.solving_time);
            assert(std::get<2>(snapshot).size() > 0);
            assert(std::get<2>(snapshot).size() <= solver.max_num_solutions);

            for (const unsigned & num_fronts : std::get<2>(snapshot)) {
                assert(num_fronts > 0);
                assert(num_fronts <= solver.population_size);
            }
        }

        for (const auto & snapshot : solver.populations_snapshots) {
            assert(std::get<0>(snapshot) >= 0);
            assert(std::get<0>(snapshot) <= solver.num_iterations);
            assert(std::get<1>(snapshot) >= 0.0);
            assert(std::get<1>(snapshot) <= solver.solving_time);
            assert(std::get<2>(snapshot).size() > 0);
            assert(std::get<2>(snapshot).size() <= solver.max_num_solutions);

            for (const auto & population : std::get<2>(snapshot)) {
                assert(population.size() == solver.population_size);

                for (const auto & s : population) {
                    assert(s.size() == 3);
                }
            }
        }

        std::cout << solver << std::endl;

        std::cout << "Num non dominated snapshots: ";
        for (unsigned i = 0;
            i < solver.num_non_dominated_snapshots.size() - 1;
            i++) {
            std::cout << std::get<2>(solver.num_non_dominated_snapshots[i]).front()
                    << " ";
        }
        std::cout << std::get<2>(solver.num_non_dominated_snapshots.back()).front()
                << std::endl;

        std::cout << "Num fronts snapshots: ";
        for (unsigned i = 0; i < solver.num_fronts_snapshots.size() - 1; i++) {
            std::cout << std::get<2>(solver.num_fronts_snapshots[i]).front()
                    << " ";
        }
        std::cout << std::get<2>(solver.num_fronts_snapshots.back()).front()
                << std::endl << std::endl;
    }

    std::cout << "NSBRKGA Solver Test PASSED" << std::endl;

    return 0;
}
