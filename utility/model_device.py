from typing import Union, List
from dataclasses import dataclass
from rmcs_api_client.resource import DataType

@dataclass
class ModelConfig:
    name: str
    value: Union[int, float, str, None]
    category: str

@dataclass
class Model:
    category: str
    name: str
    description: str
    data_type: List[DataType]
    configs: List[List[ModelConfig]]

@dataclass
class Type:
    name: str
    description: str
    models: List[str]

@dataclass
class DeviceConfig:
    name: str
    value: Union[int, float, str]
    category: str

@dataclass
class Device:
    serial_number: str
    name: str
    description: str
    type: str
    configs: List[DeviceConfig]

@dataclass
class Group:
    category: str
    name: str
    description: str
    members: List[str]
