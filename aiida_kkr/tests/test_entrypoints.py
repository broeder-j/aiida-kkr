#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

@pytest.mark.usefixtures("aiida_env")
class TestAiida_kkr_entrypoints:
    """
    tests all the entry points of the Kkr plugin. Therefore if the plugin is reconized by AiiDA 
    and installed right. 
    """
    
    # Calculation

    def test_kkrcalculation_entry_point(aiida_env):
        from aiida.orm import CalculationFactory
        from aiida_kkr.calculations.kkr import KkrCalculation

        kkr_calculation = CalculationFactory('kkr.kkr')
        assert kkr_calculation == KkrCalculation

    def test_kkrimportercalculation_entry_point(aiida_env):
        from aiida.orm import CalculationFactory
        from aiida_kkr.calculations.kkrimporter import KkrImporterCalculation

        kkrimporter_calculation = CalculationFactory('kkr.kkrimporter')
        assert kkrimporter_calculation == KkrImporterCalculation

    def test_kkrimpcalculation_entry_point(aiida_env):
        from aiida.orm import CalculationFactory
        from aiida_kkr.calculations.kkrimp import KkrimpCalculation

        kkrimp_calculation = CalculationFactory('kkr.kkrimp')
        assert kkrimp_calculation == KkrimpCalculation


    def test_voronoicalculation_entry_point(aiida_env):
        from aiida.orm import CalculationFactory
        from aiida_kkr.calculations.voro import VoronoiCalculation

        voro_calculation = CalculationFactory('kkr.voro')
        assert voro_calculation == VoronoiCalculation

    
    # Data

    def test_kkrstructuredata_entry_point(aiida_env):
        from aiida.orm import DataFactory, Data
        from aiida_kkr.data.kkrstructure import KkrstructureData
        
        StructureData = DataFactory('structure')
        kkrstruc = DataFactory('kkr.kkrstructure')
        assert kkrstruc == KkrstructureData
        assert isinstance(kkrstruc(), Data)
        assert isinstance(kkrstruc(), StructureData)


    # Parsers

    def test_kkr_parser_entry_point(aiida_env):
        from aiida.parsers import ParserFactory
        from aiida_kkr.parsers.kkr import KkrParser

        parser = ParserFactory('kkr.kkrparser')
        assert parser == KkrParser

    def test_kkrimporter_parser_entry_point(aiida_env):
        from aiida.parsers import ParserFactory
        from aiida_kkr.parsers.kkrimporter import KkrImporterParser

        parser = ParserFactory('kkr.kkrimporterparser')
        assert parser == KkrImporterParser


    def test_voronoi_parser_entry_point(aiida_env):
        from aiida.parsers import ParserFactory
        from aiida_kkr.parsers.voro import VoronoiParser

        parser = ParserFactory('kkr.voroparser')
        assert parser == VoronoiParser


    # Workchains

    def test_scf_workchain_entry_point(aiida_env):
        from aiida_kkr.workflows.kkr_scf import kkr_scf_wc
        from aiida.orm import WorkflowFactory
        
        wf = WorkflowFactory('kkr.scf')
        assert wf == kkr_scf_wc


    def test_dos_workchain_entry_point(aiida_env):
        from aiida_kkr.workflows.dos import kkr_dos_wc
        from aiida.orm import WorkflowFactory
        
        wf = WorkflowFactory('kkr.dos')
        assert wf == kkr_dos_wc


    def test_eos_workchain_entry_point(aiida_env):
        from aiida_kkr.workflows.eos import kkr_eos_wc
        from aiida.orm import WorkflowFactory
        
        wf = WorkflowFactory('kkr.eos')
        assert wf == kkr_eos_wc


    def test_startpot_workchain_entry_point(aiida_env):
        from aiida_kkr.workflows.voro_start import kkr_startpot_wc
        from aiida.orm import WorkflowFactory
        
        wf = WorkflowFactory('kkr.startpot')
        assert wf == kkr_startpot_wc


    def test_maginit_workchain_entry_point(aiida_env):
        from aiida_kkr.workflows.check_magnetic_state import kkr_check_mag_wc
        from aiida.orm import WorkflowFactory
        
        wf = WorkflowFactory('kkr.check_mag')
        assert wf == kkr_check_mag_wc


    def test_conv_workchain_entry_point(aiida_env):
        from aiida_kkr.workflows.check_para_convergence import kkr_check_para_wc
        from aiida.orm import WorkflowFactory
        
        wf = WorkflowFactory('kkr.convergence_check')
        assert wf == kkr_check_para_wc
        
        
