# -*- coding: utf-8 -*-
"""
@author: ruess
"""

import pytest
from aiida_kkr.tools.voroparser_functions import parse_voronoi_output
    
class Test_voronoi_parser_functions():
    """
    Tests for the voronoi parser functions
    """
    #some global definitions
    global dref, grouping_ref, outfile, potfile, atominfo, radii, inputfile
    dref = {'volumes_group': {'volume_total': 3.00000186, 'volume_unit': 'alat^3', 'volume_atoms': [{'iatom': 1, 'v_atom': 0.50000031}, {'iatom': 2, 'v_atom': 0.50000031}, {'iatom': 3, 'v_atom': 0.50000031}, {'iatom': 4, 'v_atom': 0.50000031}, {'iatom': 5, 'v_atom': 0.50000031}, {'iatom': 6, 'v_atom': 0.50000031}]}, 'parser_version': 'some_version_number', 'emin': -0.5, 'alat_unit': 'a_Bohr', 'radii_atoms_group': [{'rout': 0.5590171328, 'iatom': 1, 'dist_nn': 0.8660255824, 'rout_over_dist_nn': 64.55, 'rmt0_over_rout': 77.46, 'rmt0': 0.4330127912}, {'rout': 0.5590171328, 'iatom': 2, 'dist_nn': 0.8660255824, 'rout_over_dist_nn': 64.55, 'rmt0_over_rout': 77.46, 'rmt0': 0.4330127912}, {'rout': 0.5590171328, 'iatom': 3, 'dist_nn': 0.8660247659, 'rout_over_dist_nn': 64.55, 'rmt0_over_rout': 77.46, 'rmt0': 0.4330127912}, {'rout': 0.5590171328, 'iatom': 4, 'dist_nn': 0.8660247659, 'rout_over_dist_nn': 64.55, 'rmt0_over_rout': 77.46, 'rmt0': 0.4330127912}, {'rout': 0.5590171328, 'iatom': 5, 'dist_nn': 0.8660255824, 'rout_over_dist_nn': 64.55, 'rmt0_over_rout': 77.46, 'rmt0': 0.4330127912}, {'rout': 0.5590171328, 'iatom': 6, 'dist_nn': 0.8660255824, 'rout_over_dist_nn': 64.55, 'rmt0_over_rout': 77.46, 'rmt0': 0.4330127912}, {'radii_units': 'alat'}], 'shapes': [1, 1, 1, 1, 1, 1], 'code_info_group': {'code_version': 'v1.0-6-gf0c2ac3', 'calculation_serial_number': 'voro_v1.0-6-gf0c2ac3_serial_20171207092915', 'compile_options': 'serial-O2 -r8 -traceback -i8-mkl -Wl,-stack_size,0x40000000,-stack_addr,0xf0000000'}, 'fpradius_atoms_unit': 'alat', 'alat': 5.423514, 'parser_warnings': [], 'start_from_jellium_potentials': True, 'emin_units': 'Ry', 'fpradius_atoms': [0.4696902, 0.4696902, 0.4696902, 0.4696902, 0.4696902, 0.4696902], 'cluster_info_group': {'cluster_info_atoms': [{'rmt_ref': 2.3166, 'refpot': 1, 'iatom': 1, 'tb_cluster_id': 1, 'sites': 27}, {'rmt_ref': 2.3166, 'refpot': 1, 'iatom': 2, 'tb_cluster_id': 1, 'sites': 27}, {'rmt_ref': 2.3166, 'refpot': 1, 'iatom': 3, 'tb_cluster_id': 1, 'sites': 27}, {'rmt_ref': 2.3166, 'refpot': 1, 'iatom': 4, 'tb_cluster_id': 1, 'sites': 27}, {'rmt_ref': 2.3166, 'refpot': 1, 'iatom': 5, 'tb_cluster_id': 1, 'sites': 27}, {'rmt_ref': 2.3166, 'refpot': 1, 'iatom': 6, 'tb_cluster_id': 1, 'sites': 27}, {'rmt_ref': 2.3166, 'refpot': 1, 'iatom': 7, 'tb_cluster_id': 1, 'sites': 27}, {'rmt_ref': 2.3166, 'refpot': 1, 'iatom': 8, 'tb_cluster_id': 1, 'sites': 27}], 'number_of_clusters': 1},
            'core_states_group': {'descr_highest_lying_core_state_per_atom': ['no core states','no core states','no core states','no core states','3p','3p','3p','3p','no core states','no core states','no core states','no core states'],
                                  'energy_highest_lying_core_state_per_atom': [None,None,None,None,-3.3287908000000002,-3.3287908000000002,-3.3287908000000002,-3.3287908000000002,None,None,None,None],
                                  'energy_highest_lying_core_state_per_atom_unit': 'Rydberg',
                                  'number_of_core_states_per_atom': [0,0,0,0,5,5,5,5,0,0,0,0]}}
    grouping_ref = ['volumes_group', 'radii_atoms_group', 'code_info_group', 'cluster_info_group']
    path0 = '../tests/files/voronoi/'
    outfile = path0+'out_voronoi'
    potfile = path0+'output.pot'
    atominfo = path0+'atominfo.txt'
    radii = path0+'radii.dat'
    inputfile = path0+'inputcard'
    
    def test_complete_voro_output(self):
        """
        Parse complete output of voronoi calculation and compare out_dict, grouping, warnings
        """
        out_dict = {'parser_version': 'some_version_number'}
        success, msg_list, out_dict = parse_voronoi_output(out_dict, outfile, potfile, atominfo, radii, inputfile)
        out_dict['parser_warnings'] = msg_list
        assert success
        return out_dict
        assert out_dict == dref
        assert msg_list == []
        groups = [i for i in out_dict.keys() if 'group' in i]
        assert set(groups) == set(grouping_ref)
        
    def test_missing_outfile(self):
        """
        Parse output where out_voronoi is missing and compare error messages/rest of out_dict
        """
        out_dict = {'parser_version': 'some_version_number'}
        success, msg_list, out_dict = parse_voronoi_output(out_dict, '', potfile, atominfo, radii, inputfile)
        out_dict['parser_warnings'] = msg_list
        dref2 = {'parser_warnings': ['Error parsing output of voronoi: Version Info', "Error parsing output of voronoi: 'EMIN'", 'Error parsing output of voronoi: Cluster Info', 'Error parsing output of voronoi: Jellium startpot', 'Error parsing output of voronoi: SHAPE Info', 'Error parsing output of voronoi: Volume Info', 'Error parsing output of voronoi: radii.dat Info', 'Error parsing output of voronoi: full potential radius'], 'alat_unit': 'a_Bohr', 'parser_version': 'some_version_number', 'alat': 5.423514,
                 'core_states_group': {'descr_highest_lying_core_state_per_atom': ['no core states','no core states','no core states','no core states','3p','3p','3p','3p','no core states','no core states','no core states','no core states'],
                                       'energy_highest_lying_core_state_per_atom': [None,None,None,None,-3.3287908000000002,-3.3287908000000002,-3.3287908000000002,-3.3287908000000002,None,None,None,None],
                                       'energy_highest_lying_core_state_per_atom_unit': 'Rydberg',
                                       'number_of_core_states_per_atom': [0,0,0,0,5,5,5,5,0,0,0,0]},
                 'radial_meshpoints': [484.0 for i in range(12)]}
        assert not success
        assert out_dict == dref2
        assert msg_list == ['Error parsing output of voronoi: Version Info', "Error parsing output of voronoi: 'EMIN'", 'Error parsing output of voronoi: Cluster Info', 'Error parsing output of voronoi: Jellium startpot', 'Error parsing output of voronoi: SHAPE Info', 'Error parsing output of voronoi: Volume Info', 'Error parsing output of voronoi: radii.dat Info', 'Error parsing output of voronoi: full potential radius']
        
    def test_missing_atominfo(self):
        """
        Parse output where atominfo.txt is missing and compare error messages/rest of out_dict
        """
        out_dict = {'parser_version': 'some_version_number'}
        success, msg_list, out_dict = parse_voronoi_output(out_dict, outfile, potfile, 'wrong_name', radii, inputfile)
        out_dict['parser_warnings'] = msg_list
        dref2 = {'parser_version': 'some_version_number', 'emin': -0.5, 'alat_unit': 'a_Bohr', 'code_info_group': {'code_version': 'v1.0-6-gf0c2ac3', 'calculation_serial_number': 'voro_v1.0-6-gf0c2ac3_serial_20171207092915', 'compile_options': 'serial-O2 -r8 -traceback -i8-mkl -Wl,-stack_size,0x40000000,-stack_addr,0xf0000000'}, 'alat': 5.423514, 'parser_warnings': ['Error parsing output of voronoi: SHAPE Info', 'Error parsing output of voronoi: Volume Info', 'Error parsing output of voronoi: radii.dat Info', 'Error parsing output of voronoi: full potential radius'], 'start_from_jellium_potentials': True, 'emin_units': 'Ry', 'cluster_info_group': {'cluster_info_atoms': [{'rmt_ref': 2.3166, 'refpot': 1, 'iatom': 1, 'tb_cluster_id': 1, 'sites': 27}, {'rmt_ref': 2.3166, 'refpot': 1, 'iatom': 2, 'tb_cluster_id': 1, 'sites': 27}, {'rmt_ref': 2.3166, 'refpot': 1, 'iatom': 3, 'tb_cluster_id': 1, 'sites': 27}, {'rmt_ref': 2.3166, 'refpot': 1, 'iatom': 4, 'tb_cluster_id': 1, 'sites': 27}, {'rmt_ref': 2.3166, 'refpot': 1, 'iatom': 5, 'tb_cluster_id': 1, 'sites': 27}, {'rmt_ref': 2.3166, 'refpot': 1, 'iatom': 6, 'tb_cluster_id': 1, 'sites': 27}, {'rmt_ref': 2.3166, 'refpot': 1, 'iatom': 7, 'tb_cluster_id': 1, 'sites': 27}, {'rmt_ref': 2.3166, 'refpot': 1, 'iatom': 8, 'tb_cluster_id': 1, 'sites': 27}], 'number_of_clusters': 1},
                 'emin_minus_efermi': -12.370853917196168, 'emin_minus_efermi_Ry': -0.90924099999999997, 'emin_minus_efermi_Ry_units': 'Ry', 'emin_minus_efermi_units': 'eV',
                 'core_states_group': {'descr_highest_lying_core_state_per_atom': ['no core states','no core states','no core states','no core states','3p','3p','3p','3p','no core states','no core states','no core states','no core states'],
                                       'energy_highest_lying_core_state_per_atom': [None,None,None,None,-3.3287908000000002,-3.3287908000000002,-3.3287908000000002,-3.3287908000000002,None,None,None,None],
                                       'energy_highest_lying_core_state_per_atom_unit': 'Rydberg',
                                       'number_of_core_states_per_atom': [0,0,0,0,5,5,5,5,0,0,0,0]},
                 'radial_meshpoints': [484.0 for i in range(12)]}
        assert not success
        assert out_dict == dref2
        assert msg_list == ['Error parsing output of voronoi: SHAPE Info', 'Error parsing output of voronoi: Volume Info', 'Error parsing output of voronoi: radii.dat Info', 'Error parsing output of voronoi: full potential radius']
        return out_dict

    def test_missing_inputfile(self):
        """
        Parse output where inputcard is missing and compare error messages/rest of out_dict
        """
        out_dict = {'parser_version': 'some_version_number'}
        success, msg_list, out_dict = parse_voronoi_output(out_dict, outfile, potfile, atominfo, radii, 'wrong_name')
        out_dict['parser_warnings'] = msg_list
        dref2 = {'volumes_group': {'volume_total': 3.00000186, 'volume_unit': 'alat^3', 'volume_atoms': [{'iatom': 1, 'v_atom': 0.50000031}, {'iatom': 2, 'v_atom': 0.50000031}, {'iatom': 3, 'v_atom': 0.50000031}, {'iatom': 4, 'v_atom': 0.50000031}, {'iatom': 5, 'v_atom': 0.50000031}, {'iatom': 6, 'v_atom': 0.50000031}]}, 'parser_version': 'some_version_number', 'emin': -0.5, 'radii_atoms_group': [{'rout': 0.5590171328, 'iatom': 1, 'dist_nn': 0.8660255824, 'rout_over_dist_nn': 64.55, 'rmt0_over_rout': 77.46, 'rmt0': 0.4330127912}, {'rout': 0.5590171328, 'iatom': 2, 'dist_nn': 0.8660255824, 'rout_over_dist_nn': 64.55, 'rmt0_over_rout': 77.46, 'rmt0': 0.4330127912}, {'rout': 0.5590171328, 'iatom': 3, 'dist_nn': 0.8660247659, 'rout_over_dist_nn': 64.55, 'rmt0_over_rout': 77.46, 'rmt0': 0.4330127912}, {'rout': 0.5590171328, 'iatom': 4, 'dist_nn': 0.8660247659, 'rout_over_dist_nn': 64.55, 'rmt0_over_rout': 77.46, 'rmt0': 0.4330127912}, {'rout': 0.5590171328, 'iatom': 5, 'dist_nn': 0.8660255824, 'rout_over_dist_nn': 64.55, 'rmt0_over_rout': 77.46, 'rmt0': 0.4330127912}, {'rout': 0.5590171328, 'iatom': 6, 'dist_nn': 0.8660255824, 'rout_over_dist_nn': 64.55, 'rmt0_over_rout': 77.46, 'rmt0': 0.4330127912}, {'radii_units': 'alat'}], 'shapes': [1, 1, 1, 1, 1, 1], 'code_info_group': {'code_version': 'v1.0-6-gf0c2ac3', 'calculation_serial_number': 'voro_v1.0-6-gf0c2ac3_serial_20171207092915', 'compile_options': 'serial-O2 -r8 -traceback -i8-mkl -Wl,-stack_size,0x40000000,-stack_addr,0xf0000000'}, 'fpradius_atoms_unit': 'alat', 'parser_warnings': ['Error parsing output of voronoi: alat'], 'start_from_jellium_potentials': True, 'emin_units': 'Ry', 'fpradius_atoms': [0.4696902, 0.4696902, 0.4696902, 0.4696902, 0.4696902, 0.4696902], 'cluster_info_group': {'cluster_info_atoms': [{'rmt_ref': 2.3166, 'refpot': 1, 'iatom': 1, 'tb_cluster_id': 1, 'sites': 27}, {'rmt_ref': 2.3166, 'refpot': 1, 'iatom': 2, 'tb_cluster_id': 1, 'sites': 27}, {'rmt_ref': 2.3166, 'refpot': 1, 'iatom': 3, 'tb_cluster_id': 1, 'sites': 27}, {'rmt_ref': 2.3166, 'refpot': 1, 'iatom': 4, 'tb_cluster_id': 1, 'sites': 27}, {'rmt_ref': 2.3166, 'refpot': 1, 'iatom': 5, 'tb_cluster_id': 1, 'sites': 27}, {'rmt_ref': 2.3166, 'refpot': 1, 'iatom': 6, 'tb_cluster_id': 1, 'sites': 27}, {'rmt_ref': 2.3166, 'refpot': 1, 'iatom': 7, 'tb_cluster_id': 1, 'sites': 27}, {'rmt_ref': 2.3166, 'refpot': 1, 'iatom': 8, 'tb_cluster_id': 1, 'sites': 27}], 'number_of_clusters': 1},
                 'emin_minus_efermi': -12.370853917196168, 'emin_minus_efermi_Ry': -0.90924099999999997, 'emin_minus_efermi_Ry_units': 'Ry', 'emin_minus_efermi_units': 'eV',
                 'core_states_group': {'descr_highest_lying_core_state_per_atom': ['no core states','no core states','no core states','no core states','3p','3p','3p','3p','no core states','no core states','no core states','no core states'],
                                       'energy_highest_lying_core_state_per_atom': [None,None,None,None,-3.3287908000000002,-3.3287908000000002,-3.3287908000000002,-3.3287908000000002,None,None,None,None],
                                       'energy_highest_lying_core_state_per_atom_unit': 'Rydberg',
                                       'number_of_core_states_per_atom': [0,0,0,0,5,5,5,5,0,0,0,0]},
                 'radial_meshpoints': [484.0 for i in range(12)]}
        assert not success
        assert out_dict == dref2
        assert msg_list == ['Error parsing output of voronoi: alat']
        return out_dict
        
    def test_missing_potfile(self):
        """
        Parse output where output.pot is missing and compare error messages/rest of out_dict
        """
        out_dict = {'parser_version': 'some_version_number'}
        success, msg_list, out_dict = parse_voronoi_output(out_dict, outfile, 'wrong_name', atominfo, radii, inputfile)
        out_dict['parser_warnings'] = msg_list
        dref2 = {'volumes_group': {'volume_total': 3.00000186, 'volume_unit': 'alat^3', 'volume_atoms': [{'iatom': 1, 'v_atom': 0.50000031}, {'iatom': 2, 'v_atom': 0.50000031}, {'iatom': 3, 'v_atom': 0.50000031}, {'iatom': 4, 'v_atom': 0.50000031}, {'iatom': 5, 'v_atom': 0.50000031}, {'iatom': 6, 'v_atom': 0.50000031}]}, 'parser_version': 'some_version_number', 'fpradius_atoms': [0.4696902, 0.4696902, 0.4696902, 0.4696902, 0.4696902, 0.4696902], 'alat_unit': 'a_Bohr', 'shapes': [1, 1, 1, 1, 1, 1], 'code_info_group': {'code_version': 'v1.0-6-gf0c2ac3', 'calculation_serial_number': 'voro_v1.0-6-gf0c2ac3_serial_20171207092915', 'compile_options': 'serial-O2 -r8 -traceback -i8-mkl -Wl,-stack_size,0x40000000,-stack_addr,0xf0000000'}, 'fpradius_atoms_unit': 'alat', 'alat': 5.423514, 'parser_warnings': ["Error parsing output of voronoi: 'EMIN'", 'Error parsing output of voronoi: core_states', 'Error parsing output of voronoi: radial meshpoints'], 'start_from_jellium_potentials': True, 'radii_atoms_group': [{'rout': 0.5590171328, 'iatom': 1, 'dist_nn': 0.8660255824, 'rout_over_dist_nn': 64.55, 'rmt0_over_rout': 77.46, 'rmt0': 0.4330127912}, {'rout': 0.5590171328, 'iatom': 2, 'dist_nn': 0.8660255824, 'rout_over_dist_nn': 64.55, 'rmt0_over_rout': 77.46, 'rmt0': 0.4330127912}, {'rout': 0.5590171328, 'iatom': 3, 'dist_nn': 0.8660247659, 'rout_over_dist_nn': 64.55, 'rmt0_over_rout': 77.46, 'rmt0': 0.4330127912}, {'rout': 0.5590171328, 'iatom': 4, 'dist_nn': 0.8660247659, 'rout_over_dist_nn': 64.55, 'rmt0_over_rout': 77.46, 'rmt0': 0.4330127912}, {'rout': 0.5590171328, 'iatom': 5, 'dist_nn': 0.8660255824, 'rout_over_dist_nn': 64.55, 'rmt0_over_rout': 77.46, 'rmt0': 0.4330127912}, {'rout': 0.5590171328, 'iatom': 6, 'dist_nn': 0.8660255824, 'rout_over_dist_nn': 64.55, 'rmt0_over_rout': 77.46, 'rmt0': 0.4330127912}, {'radii_units': 'alat'}], 'cluster_info_group': {'cluster_info_atoms': [{'rmt_ref': 2.3166, 'refpot': 1, 'iatom': 1, 'tb_cluster_id': 1, 'sites': 27}, {'rmt_ref': 2.3166, 'refpot': 1, 'iatom': 2, 'tb_cluster_id': 1, 'sites': 27}, {'rmt_ref': 2.3166, 'refpot': 1, 'iatom': 3, 'tb_cluster_id': 1, 'sites': 27}, {'rmt_ref': 2.3166, 'refpot': 1, 'iatom': 4, 'tb_cluster_id': 1, 'sites': 27}, {'rmt_ref': 2.3166, 'refpot': 1, 'iatom': 5, 'tb_cluster_id': 1, 'sites': 27}, {'rmt_ref': 2.3166, 'refpot': 1, 'iatom': 6, 'tb_cluster_id': 1, 'sites': 27}, {'rmt_ref': 2.3166, 'refpot': 1, 'iatom': 7, 'tb_cluster_id': 1, 'sites': 27}, {'rmt_ref': 2.3166, 'refpot': 1, 'iatom': 8, 'tb_cluster_id': 1, 'sites': 27}], 'number_of_clusters': 1}}
        assert not success
        assert out_dict == dref2
        assert msg_list == ["Error parsing output of voronoi: 'EMIN'", 'Error parsing output of voronoi: core_states', 'Error parsing output of voronoi: radial meshpoints']
        return out_dict
        
    def test_missing_radii(self):
        """
        Parse output where radii.dat is missing and compare error messages/rest of out_dict
        """
        out_dict = {'parser_version': 'some_version_number'}
        success, msg_list, out_dict = parse_voronoi_output(out_dict, outfile, potfile, atominfo, 'wrong_name', inputfile)
        out_dict['parser_warnings'] = msg_list
        dref2 = {'volumes_group': {'volume_total': 3.00000186, 'volume_unit': 'alat^3', 'volume_atoms': [{'iatom': 1, 'v_atom': 0.50000031}, {'iatom': 2, 'v_atom': 0.50000031}, {'iatom': 3, 'v_atom': 0.50000031}, {'iatom': 4, 'v_atom': 0.50000031}, {'iatom': 5, 'v_atom': 0.50000031}, {'iatom': 6, 'v_atom': 0.50000031}]}, 'parser_version': 'some_version_number', 'emin': -0.5, 'alat_unit': 'a_Bohr', 'shapes': [1, 1, 1, 1, 1, 1], 'code_info_group': {'code_version': 'v1.0-6-gf0c2ac3', 'calculation_serial_number': 'voro_v1.0-6-gf0c2ac3_serial_20171207092915', 'compile_options': 'serial-O2 -r8 -traceback -i8-mkl -Wl,-stack_size,0x40000000,-stack_addr,0xf0000000'}, 'fpradius_atoms_unit': 'alat', 'alat': 5.423514, 'parser_warnings': ['Error parsing output of voronoi: radii.dat Info'], 'start_from_jellium_potentials': True, 'emin_units': 'Ry', 'fpradius_atoms': [0.4696902, 0.4696902, 0.4696902, 0.4696902, 0.4696902, 0.4696902], 'cluster_info_group': {'cluster_info_atoms': [{'rmt_ref': 2.3166, 'refpot': 1, 'iatom': 1, 'tb_cluster_id': 1, 'sites': 27}, {'rmt_ref': 2.3166, 'refpot': 1, 'iatom': 2, 'tb_cluster_id': 1, 'sites': 27}, {'rmt_ref': 2.3166, 'refpot': 1, 'iatom': 3, 'tb_cluster_id': 1, 'sites': 27}, {'rmt_ref': 2.3166, 'refpot': 1, 'iatom': 4, 'tb_cluster_id': 1, 'sites': 27}, {'rmt_ref': 2.3166, 'refpot': 1, 'iatom': 5, 'tb_cluster_id': 1, 'sites': 27}, {'rmt_ref': 2.3166, 'refpot': 1, 'iatom': 6, 'tb_cluster_id': 1, 'sites': 27}, {'rmt_ref': 2.3166, 'refpot': 1, 'iatom': 7, 'tb_cluster_id': 1, 'sites': 27}, {'rmt_ref': 2.3166, 'refpot': 1, 'iatom': 8, 'tb_cluster_id': 1, 'sites': 27}], 'number_of_clusters': 1},
                 'emin_minus_efermi': -12.370853917196168, 'emin_minus_efermi_Ry': -0.90924099999999997, 'emin_minus_efermi_Ry_units': 'Ry', 'emin_minus_efermi_units': 'eV',
                 'core_states_group': {'descr_highest_lying_core_state_per_atom': ['no core states','no core states','no core states','no core states','3p','3p','3p','3p','no core states','no core states','no core states','no core states'],
                                       'energy_highest_lying_core_state_per_atom': [None,None,None,None,-3.3287908000000002,-3.3287908000000002,-3.3287908000000002,-3.3287908000000002,None,None,None,None],
                                       'energy_highest_lying_core_state_per_atom_unit': 'Rydberg',
                                       'number_of_core_states_per_atom': [0,0,0,0,5,5,5,5,0,0,0,0]},
                'radial_meshpoints': [484. for i in range(12)]}
        assert not success
        assert out_dict == dref2
        assert msg_list == ['Error parsing output of voronoi: radii.dat Info']
        return out_dict
    
    