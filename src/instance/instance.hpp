#pragma once

#define NSBRKGA_MULTIPLE_INCLUSIONS

#include "nsbrkga.hpp"
#include <istream>
#include <ostream>
#include <map>
#include <tuple>
#include <vector>

namespace mofjssp {
/********************************************************
 * The Instance class represents an instance of the 
 * Multi-Objective Flexible Job Shop Scheduling Problem.
 ********************************************************/
class Instance {
    public:
    /***************************************************************************
     * The processing time of each operation of each job in each machine.
     ***************************************************************************/
    std::map<std::tuple<unsigned, unsigned, unsigned>, double> processing_time;

    /**********************
     * The number of jobs.
     **********************/
    unsigned num_jobs;

    /****************************************
     * The number of operations of each job.
     ****************************************/
    std::vector<unsigned> num_operations;

    /***************************************************
     * The sum of the number of operations of all jobs.
     ***************************************************/
    unsigned total_num_operations;

    /**************************
     * The number of machines.
     **************************/
    unsigned num_machines;

    /**********************************************************************
     * Machines that can be used for each operation of each job.
     **********************************************************************/
    std::vector<std::vector<std::vector<unsigned>>> machines_of_operation;

    /******************************************************************************
     * Operations that can be processed by each machine.
     ******************************************************************************/
    std::vector<std::vector<std::pair<unsigned, unsigned>>> operations_of_machine;

    /***************************
     * The number of objectives
     ***************************/
    unsigned num_objectives;

    /*********************************
     * The optimization senses.
     *********************************/
    std::vector<NSBRKGA::Sense> senses;

    /********************************
     * This instance primal bounds.
     ********************************/
    std::vector<double> primal_bound;

    private:
    /*********************************************
     * Computes the primal bounds of the instance.
     *********************************************/
    void compute_primal_bound();

    public:
    /*********************************************************************************************
     * Constructs a new instance.
     *
     * @param processing_time The processing time of each operation of each job in each machine.
     *********************************************************************************************/
    Instance(const std::map<std::tuple<unsigned, unsigned, unsigned>, double> & processing_time);

    /*********************************************
     * Copy constructor.
     *
     * @param instance the instance been copied.
     ********************************************/
    Instance(const Instance & instance);

    /********************************
     * Constructs an empty instance.
     ********************************/
    Instance();

    /************************************************
     * Copy assignment operator.
     *
     * @param instance the instance been copied.
     *
     * @return this instance
     ************************************************/
    Instance operator = (const Instance & instance);

    /***********************************************************
     * Verifies whether this instance is valid.
     *
     * @return true if this instance is valid; false otherwise.
     ***********************************************************/
    bool is_valid() const;

    /**************************************************************************
     * Standard input operator.
     *
     * @param is       standard input stream object.
     * @param instance the instance.
     *
     * @return the stream object.
     **************************************************************************/
    friend std::istream & operator >>(std::istream & is, Instance & instance);

    /*************************************************************
     * Standard output operator.
     *
     * @param os       standard output stream object.
     * @param instance the instance.
     *
     * @return the stream object.
     *************************************************************/
    friend std::ostream & operator <<(std::ostream & os,
                                      const Instance & instance);
};

}
