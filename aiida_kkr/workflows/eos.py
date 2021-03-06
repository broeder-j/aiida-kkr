#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this module you find the base workflow for a dos calculation and
some helper methods to do so with AiiDA
"""

from aiida.orm import Code, DataFactory
from aiida.work.workchain import WorkChain, while_
from aiida_kkr.calculations.kkr import KkrCalculation


__copyright__ = (u"Copyright (c), 2017, Forschungszentrum Jülich GmbH, "
                 "IAS-1/PGI-1, Germany. All rights reserved.")
__license__ = "MIT license, see LICENSE.txt file"
__version__ = "0.1"
__contributors__ = u"Philipp Rüßmann"


RemoteData = DataFactory('remote')
StructureData = DataFactory('structure')
ParameterData = DataFactory('parameter')
KkrProcess = KkrCalculation.process()

class kkr_eos_wc(WorkChain):
    """
    Workchain of an equation of states calculation with KKR.
    """

    _workflowversion = "0.1.0"
    _wf_default = {'queue_name' : '',                        # Queue name to submit jobs too
                   'resources': {"num_machines": 1},         # resources to allowcate for the job
                   'walltime_sec' : 60*60,                   # walltime after which the job gets killed (gets parsed to KKR)
                   'mpirun' : False,                         # execute KKR with mpi or without
                   'custom_scheduler_commands' : '',         # some additional scheduler commands 
                   'dos_params' : {"nepts": 61,              # DOS params: number of points in contour
                                   "tempr": 200,             # DOS params: temperature
                                   "emin": -1,               # DOS params: start of energy contour
                                   "emax": 1}                 # DOS params: end of energy contour
                   }

    @classmethod
    def define(cls, spec):
        """
        Defines the outline of the workflow. 
        """
        # Take input of the workflow or use defaults defined above
        super(kkr_eos_wc, cls).define(spec)
        spec.input("wf_parameters", valid_type=ParameterData, required=False,
                   default=ParameterData(dict=cls._wf_default))
        spec.input("remote_data", valid_type=RemoteData, required=False)
        spec.input("kkr", valid_type=Code, required=True)

        # Here the structure of the workflow is defined
        spec.outline(
            # 1. initialize workflow
            cls.start,
            # 2. encode for loop in condition
            # asyncronously submit the kkr calculations and extract total energy etc.
            while_(cls.condition)(cls.kkr_scf_etot),
            # 3. collect results, do fitting and return output nodes
            cls.return_results
        )


    