"""
Phase 7 Tests: Output Manager, Metrics Calculation, CSV Schemas, Logging

19 comprehensive tests covering:
- OutputManager structure creation
- CSV schema integrity
- Metrics calculation (hierarchical K/D)
- Logging system
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
import pandas as pd
import json
import logging

from output_manager import (
    OutputManager, ExecutionResult, ConvergencePoint, 
    MetricsCalculator, TimestampFormat
)


@pytest.fixture
def temp_output_dir():
    """Crear directorio temporal para outputs"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    # Close all logger handlers before cleanup
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
        handler.close()
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def manager(temp_output_dir):
    """Crear OutputManager con directorio temporal"""
    return OutputManager(output_root=temp_output_dir)


@pytest.fixture
def sample_results():
    """Crear conjunto de resultados de prueba"""
    results = []
    
    # Escenario 1: Instancia C101 con 3 ejecuciones (algoritmo GAA_1)
    for run in range(3):
        result = ExecutionResult(
            algorithm_id="GAA_Algorithm_1",
            instance_id="C101",
            family="C1",
            run_id=run,
            random_seed=42 + run,
            K_final=10,  # Alcanza BKS
            D_final=828.94,
            K_BKS=10,
            D_BKS=828.94,
            total_time_sec=5.2,
            iterations_executed=150
        )
        results.append(result)
    
    # Escenario 2: Instancia R101 con 3 ejecuciones (algoritmo GAA_1) - NO alcanza K_BKS
    for run in range(3):
        result = ExecutionResult(
            algorithm_id="GAA_Algorithm_1",
            instance_id="R101",
            family="R1",
            run_id=run,
            random_seed=100 + run,
            K_final=12,  # NO alcanza BKS (11)
            D_final=1635.47,
            K_BKS=11,
            D_BKS=1635.47,
            total_time_sec=7.8,
            iterations_executed=250
        )
        results.append(result)
    
    # Escenario 3: Instancia C101 con algoritmo GAA_2 (mejor)
    for run in range(3):
        result = ExecutionResult(
            algorithm_id="GAA_Algorithm_2",
            instance_id="C101",
            family="C1",
            run_id=run,
            random_seed=200 + run,
            K_final=10,
            D_final=820.00,  # Mejor distancia
            K_BKS=10,
            D_BKS=828.94,
            total_time_sec=4.9,
            iterations_executed=140
        )
        results.append(result)
    
    return results


# ============================================================================
# TESTS: OUTPUT MANAGER STRUCTURE (5 tests)
# ============================================================================

class TestOutputManagerStructure:
    """Validar creación de estructura de directorios"""
    
    def test_output_manager_creates_root_directory(self, manager):
        """Verificar que se crea directorio raíz"""
        assert manager.output_root.exists()
    
    def test_output_manager_creates_execution_directory_with_timestamp(self, manager):
        """Verificar que se crea directorio de ejecución con timestamp DD-MM-YY_HH-MM-SS"""
        assert manager.execution_dir.exists()
        # Validar formato timestamp
        timestamp_str = manager.execution_dir.name
        # Debe coincidir con patrón DD-MM-YY_HH-MM-SS (ej: 02-01-26_10-30-45)
        parts = timestamp_str.split('_')
        assert len(parts) == 2
        date_parts = parts[0].split('-')
        time_parts = parts[1].split('-')
        assert len(date_parts) == 3 and len(time_parts) == 3
    
    def test_output_manager_creates_subdirectories(self, manager):
        """Verificar creación de todas las subdirectorios: results/, solutions/, plots/, gaa/, logs/"""
        assert manager.results_dir.exists()
        assert manager.solutions_dir.exists()
        assert manager.plots_dir.exists()
        assert manager.gaa_dir.exists()
        assert manager.logs_dir.exists()
    
    def test_output_manager_multiple_executions_have_different_timestamps(self, temp_output_dir):
        """Verificar que cada ejecución obtiene un timestamp único"""
        mgr1 = OutputManager(output_root=temp_output_dir)
        # Pequeña pausa para asegurar diferentes timestamps (1 segundo)
        import time
        time.sleep(1.1)
        mgr2 = OutputManager(output_root=temp_output_dir)
        
        assert mgr1.execution_timestamp != mgr2.execution_timestamp
        assert mgr1.execution_dir != mgr2.execution_dir
    
    def test_output_manager_initializes_logger(self, manager):
        """Verificar que logger está inicializado y tiene handlers"""
        assert manager.logger is not None
        assert len(manager.logger.handlers) > 0


# ============================================================================
# TESTS: EXECUTION RESULT MODEL (3 tests)
# ============================================================================

class TestExecutionResultModel:
    """Validar modelo ExecutionResult y cálculos automáticos"""
    
    def test_execution_result_calculates_delta_k(self):
        """Verificar cálculo automático de delta_K = K_final - K_BKS"""
        result = ExecutionResult(
            algorithm_id="GAA", instance_id="C101", family="C1",
            run_id=0, random_seed=42,
            K_final=11, D_final=830.0,
            K_BKS=10, D_BKS=828.0,
            total_time_sec=5.0, iterations_executed=100
        )
        assert result.delta_K == 1
    
    def test_execution_result_sets_reached_k_bks_true(self):
        """Verificar que reached_K_BKS=True cuando K_final==K_BKS"""
        result = ExecutionResult(
            algorithm_id="GAA", instance_id="C101", family="C1",
            run_id=0, random_seed=42,
            K_final=10, D_final=828.0,
            K_BKS=10, D_BKS=828.0,
            total_time_sec=5.0, iterations_executed=100
        )
        assert result.reached_K_BKS is True
        assert result.gap_distance == 0.0
        assert result.gap_percent == 0.0
    
    def test_execution_result_gap_metrics_na_when_k_not_bks(self):
        """Verificar que gap_distance y gap_percent=NA cuando K_final != K_BKS"""
        result = ExecutionResult(
            algorithm_id="GAA", instance_id="C101", family="C1",
            run_id=0, random_seed=42,
            K_final=11, D_final=830.0,
            K_BKS=10, D_BKS=828.0,
            total_time_sec=5.0, iterations_executed=100
        )
        assert result.reached_K_BKS is False
        assert result.gap_distance is None
        assert result.gap_percent is None


# ============================================================================
# TESTS: RESULTS STORAGE & CSV OUTPUT (4 tests)
# ============================================================================

class TestResultsStorageAndCSV:
    """Validar almacenamiento y exportación CSV"""
    
    def test_add_result_stores_in_memory(self, manager, sample_results):
        """Verificar que add_result() almacena en lista interna"""
        manager.add_result(sample_results[0])
        assert len(manager.raw_results) == 1
        assert manager.raw_results[0].instance_id == "C101"
    
    def test_save_raw_results_creates_csv_with_correct_schema(self, manager, sample_results):
        """Verificar save_raw_results() crea CSV con 15 columnas exactas"""
        for result in sample_results:
            manager.add_result(result)
        
        manager.save_raw_results()
        
        csv_path = manager.results_dir / "raw_results.csv"
        assert csv_path.exists()
        
        df = pd.read_csv(csv_path)
        
        # Validar columnas exactas
        expected_columns = [
            'algorithm_id', 'instance_id', 'family', 'run_id', 'random_seed',
            'K_final', 'D_final', 'K_BKS', 'D_BKS', 'delta_K',
            'gap_distance', 'gap_percent', 'total_time_sec', 'iterations_executed',
            'reached_K_BKS'
        ]
        assert list(df.columns) == expected_columns
        assert len(df) == len(sample_results)
    
    def test_save_convergence_trace_creates_csv(self, manager):
        """Verificar save_convergence_trace() crea CSV con esquema correcto"""
        # Agregar puntos de convergencia
        for iter in range(5):
            point = ConvergencePoint(
                algorithm_id="GAA_1", instance_id="C101", family="C1",
                run_id=0, iteration=iter, elapsed_time_sec=float(iter),
                K_best_so_far=11 - min(iter, 1), D_best_so_far=900.0 - iter*10,
                is_K_BKS=(iter >= 1)
            )
            manager.add_convergence_point(point)
        
        manager.save_convergence_trace()
        
        csv_path = manager.results_dir / "convergence_trace.csv"
        assert csv_path.exists()
        
        df = pd.read_csv(csv_path)
        expected_columns = [
            'algorithm_id', 'instance_id', 'family', 'run_id', 'iteration',
            'elapsed_time_sec', 'K_best_so_far', 'D_best_so_far', 'is_K_BKS'
        ]
        assert list(df.columns) == expected_columns
        assert len(df) == 5
    
    def test_save_raw_results_handles_empty_results(self, manager):
        """Verificar que save_raw_results() maneja lista vacía correctamente"""
        manager.save_raw_results()  # No debería fallar
        csv_path = manager.results_dir / "raw_results.csv"
        assert not csv_path.exists()  # No debe crear archivo


# ============================================================================
# TESTS: METRICS CALCULATION - HIERARCHICAL K/D (5 tests)
# ============================================================================

class TestMetricsCalculation:
    """Validar cálculo de métricas jerárquicas según especificación canónica"""
    
    def test_metrics_calculator_initializes_from_results(self, sample_results):
        """Verificar que MetricsCalculator se inicializa correctamente"""
        calc = MetricsCalculator(sample_results)
        assert calc.df is not None
        assert len(calc.df) == len(sample_results)
    
    def test_calculate_k_metrics_for_instance_reaching_bks(self, sample_results):
        """Verificar cálculo de K_metrics cuando instancia alcanza K_BKS"""
        calc = MetricsCalculator(sample_results)
        
        # C101 con GAA_Algorithm_1: todas 3 ejecuciones alcanzan K_BKS=10
        k_metrics = calc.calculate_k_metrics("GAA_Algorithm_1", "C101")
        
        assert k_metrics['K_best'] == 10
        assert k_metrics['K_mean'] == 10.0
        assert k_metrics['K_std'] == 0.0
        assert k_metrics['percent_runs_K_min'] == 100.0
        assert k_metrics['reached_K_BKS'] == True  # Use == instead of is
    
    def test_calculate_k_metrics_for_instance_not_reaching_bks(self, sample_results):
        """Verificar cálculo de K_metrics cuando instancia NO alcanza K_BKS"""
        calc = MetricsCalculator(sample_results)
        
        # R101 con GAA_Algorithm_1: todas 3 ejecuciones alcanzan K_final=12, K_BKS=11
        k_metrics = calc.calculate_k_metrics("GAA_Algorithm_1", "R101")
        
        assert k_metrics['K_best'] == 12
        assert k_metrics['K_BKS'] == 11
        assert k_metrics['reached_K_BKS'] == False  # Use == instead of is
    
    def test_calculate_d_metrics_only_when_k_equals_bks(self, sample_results):
        """Verificar que D_metrics solo se calculan cuando K == K_BKS"""
        calc = MetricsCalculator(sample_results)
        
        # C101/GAA_1: alcanza K_BKS, debe tener D_metrics
        d_metrics_c101 = calc.calculate_d_metrics("GAA_Algorithm_1", "C101")
        assert d_metrics_c101['D_mean_at_K_min'] is not None
        assert d_metrics_c101['gap_percent_mean'] == 0.0
        
        # R101/GAA_1: NO alcanza K_BKS, D_metrics debe ser NA
        d_metrics_r101 = calc.calculate_d_metrics("GAA_Algorithm_1", "R101")
        assert d_metrics_r101['D_mean_at_K_min'] is None
        assert d_metrics_r101['gap_percent_mean'] is None
    
    def test_calculate_summary_by_instance(self, sample_results):
        """Verificar generación de summary_by_instance.csv"""
        calc = MetricsCalculator(sample_results)
        df_summary = calc.calculate_summary_by_instance()
        
        # Debe haber 3 filas: (GAA_1 x C101), (GAA_1 x R101), (GAA_2 x C101)
        assert len(df_summary) == 3
        
        # Validar columnas
        assert 'algorithm_id' in df_summary.columns
        assert 'instance_id' in df_summary.columns
        assert 'K_mean' in df_summary.columns
        assert 'gap_percent_mean' in df_summary.columns


# ============================================================================
# TESTS: METRICS BY FAMILY (2 tests)
# ============================================================================

class TestMetricsByFamily:
    """Validar cálculo de métricas agregadas por familia"""
    
    def test_calculate_summary_by_family(self, sample_results):
        """Verificar generación de summary_by_family.csv"""
        calc = MetricsCalculator(sample_results)
        df_family = calc.calculate_summary_by_family()
        
        # Debe tener filas para (GAA_1 x C1), (GAA_1 x R1), (GAA_2 x C1)
        assert len(df_family) >= 2
        
        # Validar estructura
        assert 'algorithm_id' in df_family.columns
        assert 'family' in df_family.columns
        assert 'instances_count' in df_family.columns
        assert 'percent_instances_K_BKS' in df_family.columns
    
    def test_percent_instances_k_bks_calculation(self, sample_results):
        """Verificar cálculo correcto de %Instancias_K_BKS"""
        calc = MetricsCalculator(sample_results)
        df_family = calc.calculate_summary_by_family()
        
        # GAA_1 x C1: 1 instancia (C101), alcanza K_BKS -> 100%
        gaa1_c1 = df_family[(df_family['algorithm_id'] == 'GAA_Algorithm_1') & 
                            (df_family['family'] == 'C1')]
        if not gaa1_c1.empty:
            assert gaa1_c1['percent_instances_K_BKS'].iloc[0] == 100.0
        
        # GAA_1 x R1: 1 instancia (R101), NO alcanza K_BKS -> 0%
        gaa1_r1 = df_family[(df_family['algorithm_id'] == 'GAA_Algorithm_1') & 
                            (df_family['family'] == 'R1')]
        if not gaa1_r1.empty:
            assert gaa1_r1['percent_instances_K_BKS'].iloc[0] == 0.0


# ============================================================================
# TESTS: LOGGING SYSTEM (3 tests)
# ============================================================================

class TestLoggingSystem:
    """Validar sistema centralizado de logging"""
    
    def test_execution_log_file_created(self, manager):
        """Verificar que execution.log se crea"""
        manager.logger.info("Test message")
        
        log_path = manager.logs_dir / "execution.log"
        assert log_path.exists()
        
        content = log_path.read_text()
        assert "Test message" in content
    
    def test_errors_log_file_created(self, manager):
        """Verificar que errors.log se crea y solo contiene errores"""
        manager.logger.info("Info message")
        manager.logger.error("Error message")
        manager.logger.warning("Warning message")
        
        error_log_path = manager.logs_dir / "errors.log"
        assert error_log_path.exists()
        
        content = error_log_path.read_text()
        assert "Error message" in content
        # info y warning NO deben estar en errors.log
        assert content.count("Info message") == 0
        assert content.count("Warning message") == 0
    
    def test_add_result_logs_correctly(self, manager):
        """Verificar que add_result() registra en log con detalles"""
        result = ExecutionResult(
            algorithm_id="GAA_1", instance_id="C101", family="C1",
            run_id=0, random_seed=42,
            K_final=10, D_final=828.94,
            K_BKS=10, D_BKS=828.94,
            total_time_sec=5.2, iterations_executed=150
        )
        
        manager.add_result(result)
        
        log_path = manager.logs_dir / "execution.log"
        content = log_path.read_text()
        
        assert "C101" in content
        assert "K=10" in content
        assert "BKS=10" in content


# ============================================================================
# TESTS: SESSION SUMMARY (1 test)
# ============================================================================

class TestSessionSummary:
    """Validar generación de session_summary.txt"""
    
    def test_save_session_summary(self, manager):
        """Verificar que save_session_summary() crea archivo formateado"""
        summary_data = {
            'Total Executions': 9,
            'Algorithms': 2,
            'Instances': 2,
            'Families': {'C1': 1, 'R1': 1}
        }
        
        manager.save_session_summary(summary_data)
        
        summary_path = manager.logs_dir / "session_summary.txt"
        assert summary_path.exists()
        
        content = summary_path.read_text()
        assert "SESSION SUMMARY" in content
        assert "Total Executions" in content
        assert "Families" in content


# ============================================================================
# INTEGRATION TESTS (1 test)
# ============================================================================

class TestPhase7Integration:
    """Tests de integración end-to-end"""
    
    def test_full_workflow_create_results_calculate_metrics_save_csv(
        self, manager, sample_results
    ):
        """Test end-to-end: agregar resultados -> calcular métricas -> guardar CSV"""
        # 1. Agregar resultados
        for result in sample_results:
            manager.add_result(result)
        
        # 2. Calcular métricas
        calc = MetricsCalculator(manager.raw_results)
        
        # 3. Guardar CSV
        manager.save_raw_results()
        manager.save_convergence_trace()  # Aunque vacío, no debe fallar
        
        # 4. Verificar archivos creados
        assert (manager.results_dir / "raw_results.csv").exists()
        
        # 5. Verificar contenido
        df_results = pd.read_csv(manager.results_dir / "raw_results.csv")
        assert len(df_results) == len(sample_results)
        assert df_results['algorithm_id'].nunique() == 2  # GAA_1, GAA_2
        assert df_results['instance_id'].nunique() == 2  # C101, R101


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
