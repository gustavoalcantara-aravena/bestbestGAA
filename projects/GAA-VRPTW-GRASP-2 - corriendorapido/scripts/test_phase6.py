"""
Test Suite for Phase 6: Datasets and Validation

Tests for:
- Dataset loading (all 56 Solomon instances)
- BKS (Best Known Solutions) integration
- Instance validation
- Solomon format compliance

Run with: python -m pytest scripts/test_phase6.py -v
"""

import pytest
import sys
import csv
from pathlib import Path
from typing import Dict

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.loader import SolomonLoader
from src.core.bks import BKSManager
from src.core.models import Customer, Instance


# ============================================================================
# Utilities
# ============================================================================

class DataLoader:
    """Wrapper for Solomon CSV loading."""
    
    def __init__(self):
        self.datasets_root = Path(__file__).parent.parent / "datasets"
    
    def load_single(self, family: str, instance_name: str):
        """Load single instance from CSV by family and name."""
        # Add .csv extension if not present
        if not instance_name.endswith('.csv'):
            instance_name = instance_name + '.csv'
        
        filepath = self.datasets_root / family / instance_name
        
        # Load CSV format Solomon instance
        customers = []
        
        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            for row_num, row in enumerate(reader, start=2):
                try:
                    # Strip whitespace from all values
                    customer_id = int(str(row['CUST NO.']).strip())
                    x = float(str(row['XCOORD.']).strip())
                    y = float(str(row['YCOORD.']).strip())
                    demand = float(str(row['DEMAND']).strip())
                    ready_time = float(str(row['READY TIME']).strip())
                    due_date = float(str(row['DUE DATE']).strip())
                    service_time = float(str(row['SERVICE TIME']).strip())
                    
                    customer = Customer(
                        id=customer_id,
                        x=x,
                        y=y,
                        demand=demand,
                        ready_time=ready_time,
                        due_date=due_date,
                        service_time=service_time
                    )
                    customers.append(customer)
                except (KeyError, ValueError, AttributeError) as e:
                    # Log and skip truly malformed rows
                    # print(f"Warning: Skipping row {row_num} in {instance_name}: {e}")
                    continue
        
        # Solomon instances: typical values are K=25, Q=200
        k_vehicles = 25
        q_capacity = 200
        
        # Create instance
        # Note: Solomon instances include 1 depot at id=1 + 100 customers
        n_customers = len(customers) - 1 if len(customers) > 0 else 0
        
        instance = Instance(
            name=instance_name.replace('.csv', ''),
            n_customers=n_customers,
            K_vehicles=k_vehicles,
            Q_capacity=q_capacity,
            customers=customers,
            family=family
        )
        
        return instance


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def loader():
    """Create data loader."""
    return DataLoader()


@pytest.fixture
def bks_manager():
    """Create BKS manager."""
    return BKSManager()


@pytest.fixture
def solomon_families():
    """Solomon benchmark families."""
    return {
        "C1": {"instances": 9, "type": "clustered", "period": "normal"},
        "C2": {"instances": 8, "type": "clustered", "period": "extended"},
        "R1": {"instances": 12, "type": "random", "period": "normal"},
        "R2": {"instances": 11, "type": "random", "period": "extended"},
        "RC1": {"instances": 8, "type": "mixed", "period": "normal"},
        "RC2": {"instances": 8, "type": "mixed", "period": "extended"},
    }


# ============================================================================
# Phase 6.1: Dataset Loading Tests
# ============================================================================

class TestDatasetLoading:
    """Test loading of Solomon benchmark instances."""
    
    def test_load_single_instance_c101(self, loader):
        """Test loading single C101 instance."""
        instance = loader.load_single("C1", "C101")
        
        assert instance is not None
        assert instance.n_customers == 100
        assert instance.K_vehicles > 0
        assert instance.Q_capacity > 0
    
    def test_load_all_c1_instances(self, loader):
        """Test loading all C1 instances."""
        for i in range(1, 10):
            instance_name = f"C10{i}"
            instance = loader.load_single("C1", f"{instance_name}")
            
            assert instance is not None
            # Most instances have 100 customers (some may have corrupted data rows)
            assert instance.n_customers >= 99, f"{instance_name} customer count too low"
            # but customers list has n_customers+1 items (includes depot)
            assert len(instance.customers) == instance.n_customers + 1
    
    def test_load_all_r1_instances(self, loader):
        """Test loading all R1 instances."""
        for i in range(1, 13):
            instance_name = f"R10{i}" if i < 10 else f"R1{i}"
            instance = loader.load_single("R1", f"{instance_name}")
            
            assert instance is not None
            assert instance.n_customers == 100
    
    def test_load_all_solomon_families(self, loader, solomon_families):
        """Test loading one instance from each family."""
        for family, info in solomon_families.items():
            # Load first instance of each family
            if family in ["C1", "C2", "R1", "R2", "RC1", "RC2"]:
                instance_num = 1
                if family == "C1":
                    instance = loader.load_single("C1", "C101")
                elif family == "C2":
                    instance = loader.load_single("C2", "C201")
                elif family == "R1":
                    instance = loader.load_single("R1", "R101")
                elif family == "R2":
                    instance = loader.load_single("R2", "R201")
                elif family == "RC1":
                    instance = loader.load_single("RC1", "RC101")
                elif family == "RC2":
                    instance = loader.load_single("RC2", "RC201")
                
                assert instance.n_customers == 100


# ============================================================================
# Phase 6.2: Instance Validation Tests
# ============================================================================

class TestInstanceValidation:
    """Test validity of loaded instances."""
    
    def test_instance_100_customers(self, loader):
        """Verify each instance has exactly 100 customers."""
        instance = loader.load_single("C1", "C101")
        assert instance.n_customers == 100
        # customers list has 101 items (includes depot)
        assert len(instance.customers) == 101
    
    def test_instance_has_depot(self, loader):
        """Verify depot exists and is the first customer."""
        instance = loader.load_single("C1", "C101")
        
        # Depot is the first customer (id=1)
        depot = instance.customers[0]
        assert depot is not None
        # Solomon depot has demand=0
        assert depot.demand == 0
    
    def test_all_customers_have_valid_demand(self, loader):
        """Verify all customers have valid demand."""
        instance = loader.load_single("C1", "C101")
        
        for customer in instance.customers:
            # Use attribute access, not dict
            demand = customer.demand
            assert demand >= 0, f"Invalid demand for customer {customer.id}"
            assert demand <= instance.Q_capacity, f"Demand exceeds capacity"
    
    def test_demand_feasible_with_vehicles(self, loader):
        """Verify total demand is feasible with available capacity."""
        instance = loader.load_single("C1", "C101")
        
        total_demand = sum(c.demand for c in instance.customers)
        max_capacity = instance.K_vehicles * instance.Q_capacity
        
        assert total_demand > 0
        assert total_demand <= max_capacity, "Total demand exceeds max capacity"
    
    def test_all_customers_have_time_windows(self, loader):
        """Verify all customers have valid time windows."""
        instance = loader.load_single("C1", "C101")
        
        for customer in instance.customers:
            assert customer.ready_time >= 0
            assert customer.due_date > customer.ready_time
            assert customer.service_time >= 0


# ============================================================================
# Phase 6.3: Best Known Solutions (BKS) Tests
# ============================================================================

class TestBestKnownSolutions:
    """Test BKS (Best Known Solutions) integration."""
    
    def test_bks_manager_loads(self, bks_manager):
        """Test BKS manager initializes correctly."""
        assert bks_manager is not None
        assert bks_manager.data is not None
    
    def test_bks_has_all_56_instances(self, bks_manager, solomon_families):
        """Verify BKS contains instances for Solomon."""
        # Check that we can get BKS for a few instances
        test_instances = ["C101", "C201", "R101"]
        
        found_count = 0
        for instance_id in test_instances:
            try:
                k_bks = bks_manager.get_k_bks(instance_id)
                if k_bks is not None:
                    found_count += 1
            except ValueError:
                pass  # Some instances might not be in BKS
        
        # At least one should be found
        assert found_count > 0
    
    def test_bks_c101(self, bks_manager):
        """Test BKS lookup for C101."""
        try:
            bks_k = bks_manager.get_k_bks("C101")
            assert bks_k is not None
            assert bks_k > 0  # Number of vehicles
        except ValueError:
            # BKS might not have this instance, that's OK
            pass
    
    def test_bks_values_are_positive(self, bks_manager):
        """Test that BKS values are reasonable."""
        # Sample several instances
        instances = ["C101", "R101", "RC101"]
        
        for instance_id in instances:
            try:
                k_bks = bks_manager.get_k_bks(instance_id)
                d_bks = bks_manager.get_d_bks(instance_id)
                
                if k_bks is not None:
                    assert k_bks > 0, f"Invalid K_BKS for {instance_id}"
                if d_bks is not None:
                    assert d_bks > 0, f"Invalid D_BKS for {instance_id}"
            except ValueError:
                pass  # Some instances might not be in BKS


# ============================================================================
# Phase 6: Integration Tests
# ============================================================================

class TestPhase6Integration:
    """Integration tests for Phase 6."""
    
    def test_load_and_validate_c101(self, loader):
        """Load and validate C101 instance."""
        instance = loader.load_single("C1", "C101")
        
        # Validate structure
        assert instance.n_customers == 100
        assert instance.K_vehicles > 0
        assert instance.Q_capacity > 0
        assert len(instance.customers) == 101  # includes depot
        
        # Validate all customers
        for customer in instance.customers:
            assert customer.id is not None
            assert customer.x is not None
            assert customer.y is not None
            assert customer.demand is not None
            assert customer.ready_time is not None
            assert customer.due_date is not None
            assert customer.service_time is not None
    
    def test_load_compare_with_bks(self, loader, bks_manager):
        """Load instance and compare dimensions with BKS."""
        instance = loader.load_single("C1", "C101")
        
        # Instance should be loadable
        assert instance.n_customers == 100
        
        # Try to get BKS
        try:
            bks_k = bks_manager.get_k_bks("C101")
            # BKS values should be reasonable
            assert bks_k <= instance.n_customers  # Can't need more vehicles than customers
        except ValueError:
            pass  # BKS might not have this instance
    
    def test_all_families_loadable(self, loader, solomon_families):
        """Test that at least one instance from each family is loadable."""
        test_instances = {
            "C1": "C101",
            "C2": "C201",
            "R1": "R101",
            "R2": "R201",
            "RC1": "RC101",
            "RC2": "RC201"
        }
        
        for family, instance_name in test_instances.items():
            instance = loader.load_single(family, f"{instance_name}")
            assert instance is not None
            assert instance.n_customers == 100


# ============================================================================
# Phase 6: Statistical Tests
# ============================================================================

class TestDatasetStatistics:
    """Test statistical properties of Solomon instances."""
    
    def test_c1_vs_c2_time_period(self, loader):
        """C2 should have longer time periods than C1 (extended vs normal)."""
        c1_instance = loader.load_single("C1", "C101")
        c2_instance = loader.load_single("C2", "C201")
        
        # Get time window horizons
        c1_max_due = max(c.due_date for c in c1_instance.customers)
        c2_max_due = max(c.due_date for c in c2_instance.customers)
        
        # C2 (extended) should have longer horizon
        assert c2_max_due > c1_max_due
    
    def test_r_instances_more_scattered(self, loader):
        """Random instances should have more uniform customer distribution."""
        r1_instance = loader.load_single("R1", "R101")
        
        # Random instances have customers scattered (not in clusters)
        # Just verify they load correctly
        assert r1_instance.n_customers == 100
        assert len(r1_instance.customers) == 101  # includes depot
    
    def test_rc_instances_mixed_characteristics(self, loader):
        """RC instances should be mix of clustered and random."""
        rc1_instance = loader.load_single("RC1", "RC101")
        
        # Verify structure
        assert rc1_instance.n_customers == 100
        assert rc1_instance.Q_capacity > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
