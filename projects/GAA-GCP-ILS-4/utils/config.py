"""
utils/config.py
Utilidades para cargar y gestionar configuración del proyecto.
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional


class Config:
    """Gestor de configuración centralizado."""
    
    _instance: Optional["Config"] = None
    _config: Dict[str, Any] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def load(cls, config_file: str = "config/config.yaml") -> "Config":
        """
        Cargar configuración desde archivo YAML.
        
        Parametros:
            config_file (str): Ruta al archivo de configuración
        
        Retorna:
            Config: Instancia singleton
        """
        config_path = Path(config_file)
        
        if not config_path.exists():
            raise FileNotFoundError(f"Archivo de configuración no encontrado: {config_file}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            cls._config = yaml.safe_load(f) or {}
        
        return cls()
    
    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """
        Obtener valor de configuración con notación de punto.
        
        Ejemplo:
            Config.get("ils.max_iterations")  # Retorna 500
        
        Parametros:
            key (str): Clave con notación de punto (ej: "a.b.c")
            default (Any): Valor por defecto si no existe
        
        Retorna:
            Any: Valor de configuración
        """
        keys = key.split('.')
        value = cls._config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value
    
    @classmethod
    def set(cls, key: str, value: Any) -> None:
        """
        Establecer valor de configuración.
        
        Parametros:
            key (str): Clave con notación de punto
            value (Any): Nuevo valor
        """
        keys = key.split('.')
        config = cls._config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    @classmethod
    def get_all(cls) -> Dict[str, Any]:
        """Obtener toda la configuración."""
        return cls._config.copy()
    
    @classmethod
    def __getitem__(cls, key: str) -> Any:
        """Acceso directo con []."""
        return cls.get(key)


# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def load_config(config_file: str = "config/config.yaml") -> Config:
    """Cargar configuración global."""
    return Config.load(config_file)


def get_config(key: str, default: Any = None) -> Any:
    """Acceso rápido a configuración."""
    return Config.get(key, default)


def ensure_directories() -> None:
    """Crear directorios necesarios si no existen."""
    directories = [
        Config.get("problem.datasets_dir"),
        Config.get("problem.training_dir"),
        Config.get("problem.validation_dir"),
        Config.get("problem.test_dir"),
        Config.get("output.results_dir"),
        Config.get("output.solutions_dir"),
        Config.get("output.logs_dir"),
        Config.get("output.plots_dir"),
    ]
    
    for dir_path in directories:
        if dir_path:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
