"""
Data Loader for Solomon VRPTW Instances

Loads customer and instance data from Solomon benchmark CSV format.
Validates 100 customers + 1 depot structure and all parameters.
"""

import os
from typing import Optional, List, Tuple
from pathlib import Path
from .models import Customer, Instance


class SolomonLoader:
    """
    Loader for Solomon VRPTW benchmark instances.
    
    Format (CSV, space-separated):
    - First line: Instance name, number of vehicles, capacity
    - Next 101 lines: Customer data
      Line format: customer_id x y demand ready_time due_date service_time
    """
    
    SOLOMON_FAMILIES = {
        'C1': ('Clustered, short horizon', 25),
        'C2': ('Clustered, long horizon', 25),
        'R1': ('Random, short horizon', 25),
        'R2': ('Random, long horizon', 25),
        'RC1': ('Mixed, short horizon', 25),
        'RC2': ('Mixed, long horizon', 25),
    }
    
    @staticmethod
    def parse_family(instance_name: str) -> str:
        """
        Extract Solomon family from instance name.
        
        Args:
            instance_name: Instance identifier (e.g., "C101")
            
        Returns:
            Family code (C1, C2, R1, R2, RC1, or RC2)
        """
        name = instance_name.upper().strip()
        for family in ['RC1', 'RC2', 'C1', 'C2', 'R1', 'R2']:
            if name.startswith(family):
                return family
        return "UNKNOWN"
    
    @staticmethod
    def load_instance(filepath: str) -> Instance:
        """
        Load a single Solomon instance from CSV file.
        
        Args:
            filepath: Path to instance file
            
        Returns:
            Loaded Instance object
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is invalid or data is corrupted
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Instance file not found: {filepath}")
        
        instance_name = Path(filepath).stem
        family = SolomonLoader.parse_family(instance_name)
        
        with open(filepath, 'r') as f:
            lines = f.readlines()
        
        if len(lines) < 2:
            raise ValueError(f"Invalid file format: expected at least 2 lines in {filepath}")
        
        # Parse header (first line)
        header = lines[0].split()
        try:
            # Try to extract vehicle count and capacity
            if len(header) >= 2:
                try:
                    k_vehicles = int(header[0])
                    q_capacity = float(header[1])
                except (ValueError, IndexError):
                    # Alternative format: instance name in header
                    k_vehicles = int(header[-2])
                    q_capacity = float(header[-1])
            else:
                raise ValueError("Header must contain at least vehicle count and capacity")
        except (ValueError, IndexError) as e:
            raise ValueError(f"Cannot parse header: {header}. Error: {e}")
        
        # Parse customers (remaining lines)
        customers = []
        for line_no, line in enumerate(lines[1:], start=2):
            parts = line.split()
            if not parts:  # Skip empty lines
                continue
            
            if len(parts) < 7:
                raise ValueError(
                    f"Invalid customer data at line {line_no}: expected 7 fields, got {len(parts)}"
                )
            
            try:
                customer_id = int(parts[0])
                x = float(parts[1])
                y = float(parts[2])
                demand = float(parts[3])
                ready_time = float(parts[4])
                due_date = float(parts[5])
                service_time = float(parts[6])
                
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
                
            except ValueError as e:
                raise ValueError(
                    f"Cannot parse customer at line {line_no}: {parts}. Error: {e}"
                )
        
        # Create instance
        n_customers = len(customers) - 1  # Excluding depot
        
        if n_customers != 100:
            raise ValueError(
                f"Expected 100 customers (101 including depot), got {n_customers}"
            )
        
        instance = Instance(
            name=instance_name,
            n_customers=n_customers,
            K_vehicles=k_vehicles,
            Q_capacity=q_capacity,
            customers=customers,
            family=family
        )
        
        # Validate
        is_valid, errors = instance.validate()
        if not is_valid:
            raise ValueError(
                f"Instance validation failed for {instance_name}:\n" +
                "\n".join(errors)
            )
        
        return instance
    
    @staticmethod
    def load_all_instances(dataset_path: str) -> dict:
        """
        Load all Solomon instances from a directory.
        
        Args:
            dataset_path: Path to dataset directory with subdirectories C1, C2, R1, R2, RC1, RC2
            
        Returns:
            Dictionary: {family: {instance_name: Instance}}
            
        Raises:
            FileNotFoundError: If directory or family subdirectories don't exist
        """
        if not os.path.isdir(dataset_path):
            raise FileNotFoundError(f"Dataset directory not found: {dataset_path}")
        
        instances = {family: {} for family in SolomonLoader.SOLOMON_FAMILIES}
        
        for family in SolomonLoader.SOLOMON_FAMILIES:
            family_path = os.path.join(dataset_path, family)
            
            if not os.path.isdir(family_path):
                print(f"⚠️  Family directory not found: {family_path}")
                continue
            
            # Find all instance files in family directory
            for filename in sorted(os.listdir(family_path)):
                if filename.startswith('.'):  # Skip hidden files
                    continue
                
                filepath = os.path.join(family_path, filename)
                if os.path.isfile(filepath):
                    try:
                        instance = SolomonLoader.load_instance(filepath)
                        instances[family][instance.name] = instance
                    except Exception as e:
                        print(f"⚠️  Failed to load {filepath}: {e}")
                        continue
        
        return instances
    
    @staticmethod
    def get_instance_by_id(all_instances: dict, instance_id: str) -> Optional[Instance]:
        """
        Get a specific instance by ID from loaded instances.
        
        Args:
            all_instances: Dictionary returned by load_all_instances()
            instance_id: Instance identifier (e.g., "C101")
            
        Returns:
            Instance object or None if not found
        """
        family = SolomonLoader.parse_family(instance_id)
        if family in all_instances:
            return all_instances[family].get(instance_id.upper())
        return None
    
    @staticmethod
    def get_family_instances(all_instances: dict, family: str) -> dict:
        """
        Get all instances in a specific family.
        
        Args:
            all_instances: Dictionary returned by load_all_instances()
            family: Family code (C1, C2, R1, R2, RC1, or RC2)
            
        Returns:
            Dictionary of instances in that family
        """
        return all_instances.get(family, {})
    
    @staticmethod
    def summary(all_instances: dict) -> dict:
        """
        Generate summary statistics for loaded instances.
        
        Args:
            all_instances: Dictionary returned by load_all_instances()
            
        Returns:
            Dictionary with statistics by family and global
        """
        summary_data = {}
        total_instances = 0
        total_customers = 0
        
        for family in SolomonLoader.SOLOMON_FAMILIES:
            family_instances = all_instances[family]
            count = len(family_instances)
            total_instances += count
            
            if count > 0:
                total_customers += count * 100  # Each instance has 100 customers
                avg_vehicles = sum(inst.K_vehicles for inst in family_instances.values()) / count
                avg_capacity = sum(inst.Q_capacity for inst in family_instances.values()) / count
                
                summary_data[family] = {
                    'count': count,
                    'avg_vehicles': avg_vehicles,
                    'avg_capacity': avg_capacity,
                    'instances': sorted(family_instances.keys())
                }
        
        return {
            'total_families': len(SolomonLoader.SOLOMON_FAMILIES),
            'total_instances': total_instances,
            'families': summary_data
        }
