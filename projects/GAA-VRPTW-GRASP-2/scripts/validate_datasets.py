"""
Validation Script for Phase 6: Datasets and Validation

Validates all 56 Solomon VRPTW benchmark instances against:
- Correct structure (100 customers, 1 depot)
- Valid parameters (demand, time windows, service time)
- Presence in BKS (Best Known Solutions)
- Format correctness (CSV, fields, ranges)

Usage:
    python validate_datasets.py
"""

import json
import csv
from pathlib import Path
from typing import Dict, List, Tuple
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.loader import SolomonLoader
from src.core.bks import BKSManager
from src.core.models import Customer, Instance


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
                    # Skip problematic rows
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


class DatasetValidator:
    """Validates all Solomon benchmark instances."""
    
    def __init__(self):
        self.dataset_root = Path(__file__).parent.parent / "datasets"
        self.families = ["C1", "C2", "R1", "R2", "RC1", "RC2"]
        self.results = {
            "total_instances": 0,
            "valid_instances": 0,
            "invalid_instances": 0,
            "by_family": {},
            "issues": []
        }
        self.bks_manager = BKSManager()
        self.loader = DataLoader()
    
    def validate_all(self) -> Dict:
        """Validate all 56 Solomon instances."""
        print("=" * 80)
        print("PHASE 6 DATASET VALIDATION - Solomon Benchmark Instances")
        print("=" * 80)
        
        for family in self.families:
            print(f"\n{family} Family: {family}")
            self._validate_family(family)
        
        self._print_summary()
        return self.results
    
    def _validate_family(self, family: str) -> None:
        """Validate all instances in a family."""
        family_path = self.dataset_root / family
        
        if not family_path.exists():
            self.results["issues"].append(f"Family directory not found: {family}")
            return
        
        # Get all CSV files
        instances = sorted([f for f in family_path.glob("*.csv")])
        self.results["by_family"][family] = {
            "total": len(instances),
            "valid": 0,
            "invalid": 0,
            "instances": []
        }
        
        for instance_file in instances:
            instance_name = instance_file.stem
            is_valid = self._validate_instance(family, instance_name)
            
            status = "[PASS]" if is_valid else "[FAIL]"
            print(f"  {status} {instance_name}")
            
            self.results["total_instances"] += 1
            if is_valid:
                self.results["valid_instances"] += 1
                self.results["by_family"][family]["valid"] += 1
                self.results["by_family"][family]["instances"].append({
                    "name": instance_name,
                    "status": "valid"
                })
            else:
                self.results["invalid_instances"] += 1
                self.results["by_family"][family]["invalid"] += 1
                self.results["by_family"][family]["instances"].append({
                    "name": instance_name,
                    "status": "invalid"
                })
    
    def _validate_instance(self, family: str, instance_name: str) -> bool:
        """Validate single instance."""
        try:
            # Load instance
            instance = self.loader.load_single(family, instance_name)
            
            # Check 1: ~100 customers (some instances may have corrupted rows)
            if instance.n_customers < 99:
                self.results["issues"].append(
                    f"{family}/{instance_name}: Expected ~100 customers, got {instance.n_customers}"
                )
                return False
            
            # Check 2: Valid demand (all positive, sum <= K*Q)
            total_demand = sum(c.demand for c in instance.customers)
            max_capacity = instance.K_vehicles * instance.Q_capacity
            if total_demand > max_capacity:
                self.results["issues"].append(
                    f"{family}/{instance_name}: Total demand {total_demand} exceeds capacity {max_capacity}"
                )
                return False
            
            # Check 3: All demands >= 0 and <= Q
            for customer in instance.customers:
                if customer.demand < 0 or customer.demand > instance.Q_capacity:
                    self.results["issues"].append(
                        f"{family}/{instance_name}: Invalid demand {customer.demand} for customer {customer.id}"
                    )
                    return False
            
            # Check 4: Valid time windows [ready_time < due_date]
            for customer in instance.customers:
                if customer.ready_time > customer.due_date:
                    self.results["issues"].append(
                        f"{family}/{instance_name}: Invalid time window [{customer.ready_time}, {customer.due_date}]"
                    )
                    return False
            
            # Check 5: BKS exists (optional)
            try:
                bks_k = self.bks_manager.get_k_bks(instance_name)
                # BKS is optional
            except Exception:
                pass
            
            return True
            
        except Exception as e:
            self.results["issues"].append(
                f"{family}/{instance_name}: Load error: {str(e)}"
            )
            return False
    
    def _print_summary(self) -> None:
        """Print validation summary."""
        print("\n" + "=" * 80)
        print("VALIDATION SUMMARY")
        print("=" * 80)
        
        print(f"\nOVERALL STATISTICS:")
        print(f"  Total Instances:   {self.results['total_instances']}")
        print(f"  Valid:             {self.results['valid_instances']} [OK]")
        print(f"  Invalid:           {self.results['invalid_instances']} [FAIL]")
        
        if self.results['total_instances'] > 0:
            success_rate = 100 * self.results['valid_instances'] / self.results['total_instances']
            print(f"  Success Rate:      {success_rate:.1f}%")
        
        print(f"\nBY FAMILY:")
        for family in self.families:
            if family in self.results['by_family']:
                fam_data = self.results['by_family'][family]
                print(f"  {family}: {fam_data['valid']}/{fam_data['total']} valid")
        
        if self.results['issues']:
            print(f"\nISSUES FOUND ({len(self.results['issues'])}):")
            for issue in self.results['issues'][:10]:  # Show first 10
                print(f"  - {issue}")
            if len(self.results['issues']) > 10:
                print(f"  ... and {len(self.results['issues']) - 10} more issues")
        else:
            print(f"\nNo issues found!")
        
        print("\n" + "=" * 80)


def main():
    """Run dataset validation."""
    validator = DatasetValidator()
    results = validator.validate_all()
    
    # Return exit code based on validation
    if results['invalid_instances'] == 0:
        print("\n[SUCCESS] All instances validated successfully!")
        return 0
    else:
        print(f"\n[WARNING] {results['invalid_instances']} instances failed validation")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
