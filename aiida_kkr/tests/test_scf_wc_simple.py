#!/usr/bin/env python

import pytest

# helper function
def print_clean_inouts(node):
    from pprint import pprint
    inputs = node.get_inputs_dict()
    outputs = node.get_outputs_dict()
    for key in outputs.keys():
        try:
            int(key.split('_')[-1])
            has_id = True
        except:
            has_id = False
        if 'CALL' in key or 'CREATE' in key or has_id:
            outputs.pop(key)
    print 'inputs:'
    pprint(inputs)
    print '\noutputs:'
    pprint(outputs)


# tests
@pytest.mark.usefixtures("aiida_env")
class Test_scf_workflow():
    """
    Tests for the scf workfunction
    """
    
    def test_scf_wc_Cu_simple(self):
        """
        simple Cu noSOC, FP, lmax2 full example using scf workflow
        """
        from aiida.orm import Code, load_node, DataFactory
        from aiida.work import run
        from aiida_kkr.tools.kkr_params import kkrparams
        from aiida_kkr.workflows.kkr_scf import kkr_scf_wc
        from pprint import pprint
        from scipy import array
       
        ParameterData = DataFactory('parameter')
        StructureData = DataFactory('structure')
       
        alat = 6.83 # in a_Bohr
        abohr = 0.52917721067 # conversion factor to Angstroem units
        # bravais vectors
        bravais = array([[0.5, 0.5, 0.0], [0.5, 0.0, 0.5], [0.0, 0.5, 0.5]])
       
        a = 0.5*alat*abohr
        Cu = StructureData(cell=[[a, a, 0.0], [a, 0.0, a], [0.0, a, a]])
        Cu.append_atom(position=[0.0, 0.0, 0.0], symbols='Cu')
       
        Cu.store()
        print(Cu)
       
        # here we create a parameter node for the workflow input (workflow specific parameter) and adjust the convergence criterion.
        wfd = kkr_scf_wc.get_wf_defaults()
       
        wfd['convergence_criterion'] = 10**-4
        wfd['check_dos'] = False 
        wfd['kkr_runmax'] = 5
        wfd['nsteps'] = 50 
        wfd['queue_name'] = ''
        wfd['resources']['num_machines'] = 1 
        wfd['use_mpi'] = False #True
       
        wfd['num_rerun'] = 2
        wfd['natom_in_cls_min'] = 20
       
        KKRscf_wf_parameters = ParameterData(dict=wfd)
       
        # The scf-workflow needs also the voronoi and KKR codes to be able to run the calulations
        VoroCode = Code.get_from_string('voronoi@my_mac')
        KKRCode = Code.get_from_string('KKRcode@my_mac')
       
        # Finally we use the kkrparams class to prepare a valid set of KKR parameters that are stored as a ParameterData object for the use in aiida
        ParaNode = ParameterData(dict=kkrparams(LMAX=2, RMAX=7, GMAX=65, NSPIN=1, RCLUSTZ=1.9).get_dict())
       
        label = 'KKR-scf for Cu bulk'
        descr = 'KKR self-consistency workflow for Cu bulk'
        try:
          out = run(kkr_scf_wc, structure=Cu, calc_parameters=ParaNode, voronoi=VoroCode, 
                    kkr=KKRCode, wf_parameters=KKRscf_wf_parameters, _label=label, _description=descr)
        except:
          print 'some Error occured in run of kkr_scf_wc'
       
       
        # load node of workflow
        print out
        n = load_node(out[1])
       
        print '\noutputs of workflow\n-------------------------------------------------'
        pprint(n.get_outputs_dict())
       
        # get output dictionary
        n = n.get_outputs()[-1]
        out = n.get_dict()
        print '\n\noutput dictionary:\n-------------------------------------------------'
        pprint(out)
       
        # finally check some output
        print '\n\ncheck values ...\n-------------------------------------------------'
       
        print 'voronoi_step_success', out['voronoi_step_success']
        assert out['voronoi_step_success']
       
        print 'kkr_step_success', out['kkr_step_success']
        assert out['kkr_step_success']
       
        print 'successful', out['successful']
        assert out['successful']
       
        print 'error', out['errors']
        assert out['errors'] == []
       
        print 'warning', out['warnings']
        assert out['warnings'] == []
       
        print 'convergence_reached', out['convergence_reached']
        assert out['convergence_reached']
       
        print 'convergence_value', out['convergence_value']
        assert out['convergence_value'] < 10**-4
       
        print 'charge_neutrality', abs(out['charge_neutrality'])
        assert abs(out['charge_neutrality']) < 5*10**-4
       
        print 'used_higher_accuracy', out['used_higher_accuracy']
        assert out['used_higher_accuracy']
       
        print '\ndone with checks\n'
 
#run test manually
if __name__=='__main__':
   from aiida import is_dbenv_loaded, load_dbenv
   if not is_dbenv_loaded():
      load_dbenv()
   Test = Test_scf_workflow()
   Test.test_scf_wc_Cu_simple()
