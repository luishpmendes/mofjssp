#pragma once

#include "instance/instance.hpp"

namespace mofjssp {
/********************************************************
 * The Solution class represents an solution of the 
 * Multi-Objective Flexible Job Shop Scheduling Problem.
 ********************************************************/
class Solution {
    public:
    /************************************************************
     * Returns true if valueA dominates valueB; false otherwise.
     *
     * @param valueA the first value been compared.
     * @param valueB the second value been compared.
     *
     * @return true if valueA dominates valueB; false otherwise.
     ************************************************************/
    static bool dominates(const std::vector<double> & valueA,
                          const std::vector<double> & valueB);

    /****************************
     * The instance been solved.
     ****************************/
    const Instance & instance;

    /***********************************************************
     * The machine that is used for each operation of each job.
     ***********************************************************/
    std::vector<std::vector<unsigned>> machine_of_operation;

    /******************************************************************************
     * The operations that are processed by each machine, in order.
     ******************************************************************************/
    std::vector<std::vector<std::pair<unsigned, unsigned>>> operations_of_machine;

    /**************************************************************
     * The time that each operation of each job starts processing.
     **************************************************************/
    std::vector<std::vector<double>> starting_time_of_operation;

    /************************************************************
     * The time that each operation of each job ends processing.
     ************************************************************/
    std::vector<std::vector<double>> ending_time_of_operation;

    /**************************************************************************
     * The value of the solution, that consists of:
     * - the makespan, i.e., maximal completion time of the jobs
     * - the total completion time of the jobs
     * - the maximal machine workload, i.e., the maximum working time spent on
     *   any machine
     * - total workload of the machines, which represents the total working 
     *   time of all machines.
     **************************************************************************/
    std::vector<double> value;

    private:
    /**************************************
     * Computes the value of the solution.
     **************************************/
    void compute_value();

    /******************************
     * Initializes a new solution.
     ******************************/
    void init();

    public:
    /********************************************************************************
     * Constructs a new solution.
     *
     * @param instance                   the instance been solved.
     * @param machine_of_operation       the machine that is used for each operation
     *                                   of each job.
     * @param starting_time_of_operation the time that each operations of each job
     *                                   starts processing.
     ********************************************************************************/
    Solution(const Instance & instance,
             const std::vector<std::vector<unsigned>> & machine_of_operation,
             const std::vector<std::vector<double>> & starting_time_of_operation);

    /**********************************************************************
     * Constructs a new solution.
     *
     * @param instance     the instance been solved.
     * @param key          the key representing the machine assignment and
     *                     scheduling of each operation of each job.
     **********************************************************************/
    Solution(const Instance & instance,
             const std::vector<double> & key);

    /********************************************
     * Constructs a new solution.
     *
     * @param instance the instance been solved.
     ********************************************/
    Solution(const Instance & instance);

    /*********************************************
     * Verifies whether this solution is
     * feasible for the instance been solved.
     *
     * @return true if this solution is feasible;
     *         false otherwise.
     *********************************************/
    bool is_feasible() const;

    /*******************************************************************
     * Verifies whether this solution dominates the specified one.
     *
     * @param solution the solution whose domination is to be verified.
     *
     * @return true if this instance dominated the specified one;
     *         false otherwise.
     *******************************************************************/
    bool dominates(const Solution & solution) const;

    /*******************************************************
     * Standard input operator.
     *
     * @param is       standard input stream object.
     * @param solution the solution.
     *
     * @return the stream object.
     *******************************************************/
    friend std::istream & operator >>(std::istream & is,
                                      Solution & solution);

    /*************************************************************
     * Standard output operator.
     *
     * @param os       standard output stream object.
     * @param solution the solution.
     *
     * @return the stream object.
     *************************************************************/
    friend std::ostream & operator <<(std::ostream & os,
                                      const Solution & solution);
};

}
