import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from rmcs_api_client.resource import DataType
from utility.model_device import Model, ModelConfig, Type, Device, DeviceConfig, Group


MODELS = {
    "accelerometer": Model(
        "RAW", 
        "3-axis 16-bit accelerometer", 
        "3 16-bit integer accelerometer output value", 
        [DataType.U16, DataType.U16, DataType.U16],
        []
    ),
    "soil_inclinometer": Model(
        "DATA",
        "XZ-axis soil inclinometer",
        "XZ-axis inclination and displacement, Y-axis parallel with gravity",
        [DataType.F64, DataType.F64, DataType.F64, DataType.F64, DataType.F64, DataType.F64, DataType.F64],
        [
            [
                ModelConfig("scale", "acceleration-X", "SCALE"),
                ModelConfig("unit", "gravity", "UNIT"),
                ModelConfig("symbol", "g", "SYMBOL")
            ],
            [
                ModelConfig("scale", "acceleration-Y", "SCALE"),
                ModelConfig("unit", "gravity", "UNIT"),
                ModelConfig("symbol", "g", "SYMBOL")
            ],
            [
                ModelConfig("scale", "acceleration-Z", "SCALE"),
                ModelConfig("unit", "gravity", "UNIT"),
                ModelConfig("symbol", "g", "SYMBOL")
            ],
            [
                ModelConfig("scale", "inclination-X", "SCALE"),
                ModelConfig("unit", "degree", "UNIT"),
                ModelConfig("symbol", "°", "SYMBOL")
            ],
            [
                ModelConfig("scale", "inclination-Y", "SCALE"),
                ModelConfig("unit", "degree", "UNIT"),
                ModelConfig("symbol", "°", "SYMBOL")
            ],
            [
                ModelConfig("scale", "displacement-X", "SCALE"),
                ModelConfig("unit", "millimeter", "UNIT"),
                ModelConfig("symbol", "mm", "SYMBOL")
            ],
            [
                ModelConfig("scale", "displacement-Y", "SCALE"),
                ModelConfig("unit", "millimeter", "UNIT"),
                ModelConfig("symbol", "mm", "SYMBOL")
            ]
        ]
    ),
    "piezometer_raw": Model(
        "RAW", 
        "piezometer raw data", 
        "16-bit integer pressure and depth value", 
        [DataType.U16, DataType.U16, DataType.U16, DataType.U16],
        []
    ),
    "piezometer_data": Model(
        "DATA",
        "piezometer data",
        "pressure and depth value",
        [DataType.F64, DataType.F64],
        [
            [
                ModelConfig("scale", "pressure", "SCALE"),
                ModelConfig("unit", "pascal", "UNIT"),
                ModelConfig("symbol", "pa", "SYMBOL")
            ],
            [
                ModelConfig("scale", "depth", "SCALE"),
                ModelConfig("unit", "millimeter", "UNIT"),
                ModelConfig("symbol", "mm", "SYMBOL")
            ]
        ]
    ),
    "rain_gauge_raw": Model(
        "RAW", 
        "rain gauge raw data", 
        "16-bit integer rain fall value", 
        [DataType.U16, DataType.U16, DataType.U16, DataType.U16],
        []
    ),
    "rain_gauge_data": Model(
        "DATA",
        "rain gauge data",
        "rain gauge yesterday, daily, last hour, and hourly data",
        [DataType.F64, DataType.F64, DataType.F64, DataType.F64],
        [
            [
                ModelConfig("scale", "rain yesterday", "SCALE"),
                ModelConfig("unit", "millimeter", "UNIT"),
                ModelConfig("symbol", "mm", "SYMBOL")
            ],
            [
                ModelConfig("scale", "rain daily", "SCALE"),
                ModelConfig("unit", "millimeter", "UNIT"),
                ModelConfig("symbol", "mm", "SYMBOL")
            ],
            [
                ModelConfig("scale", "rain last hour", "SCALE"),
                ModelConfig("unit", "millimeter", "UNIT"),
                ModelConfig("symbol", "mm", "SYMBOL")
            ],
            [
                ModelConfig("scale", "rain hourly", "SCALE"),
                ModelConfig("unit", "millimeter", "UNIT"),
                ModelConfig("symbol", "mm", "SYMBOL")
            ]
        ]
    ),
    "environment_raw": Model(
        "RAW", 
        "environment sensor raw data", 
        "16-bit integer temperature, humidity, and pressure value", 
        [DataType.U16, DataType.U16, DataType.U16],
        []
    ),
    "environment_data": Model(
        "DATA",
        "environment sensor data",
        "air temperature, relative humidity, and pressure data",
        [DataType.F64, DataType.F64, DataType.F64],
        [
            [
                ModelConfig("scale", "temperature", "SCALE"),
                ModelConfig("unit", "celcius", "UNIT"),
                ModelConfig("symbol", "°C", "SYMBOL")
            ],
            [
                ModelConfig("scale", "humidity", "SCALE"),
                ModelConfig("unit", "percent", "UNIT"),
                ModelConfig("symbol", "%", "SYMBOL")
            ],
            [
                ModelConfig("scale", "pressure", "SCALE"),
                ModelConfig("unit", "kilo pascal", "UNIT"),
                ModelConfig("symbol", "kPa", "SYMBOL")
            ]
        ]
    )
}

TYPES = {
    "gateway": Type(
        "gateway blank",
        "gateway with no model",
        []
    ),
    "soil_inclinometer": Type(
        "soil inclinometer",
        "3-axis accelerometer and soil inclinometer",
        ["accelerometer", "soil_inclinometer"]
    ),
    "piezometer": Type(
        "piezometer",
        "piezometer with fluid pressure and depth output",
        ["piezometer_raw", "piezometer_data"]
    ),
    "rain_gauge": Type(
        "rain gauge",
        "tipping bucket rain gauge with daily and hourly rain fall output",
        ["rain_gauge_raw", "rain_gauge_data"]
    ),
    "environment": Type(
        "environment sensor",
        "environment sensor with air temperature, relative humidity, and  output",
        ["environment_raw", "environment_data"]
    )
}

GATEWAY = Device(
    "GATE01",
    "Gateway_1",
    "",
    "gateway",
    []
)

DEVICES = [
    Device(
        "TESTACC01",
        "Accelerometer_1",
        "soil inclinometer 1 testing",
        "soil_inclinometer",
        [
            DeviceConfig("slave_id", 0x01, "COMMUNICATION"),
            DeviceConfig("offset-X", 0, "OFFSET"),
            DeviceConfig("offset-Y", 0, "OFFSET"),
            DeviceConfig("offset-Z", 0, "OFFSET"),
            DeviceConfig("space", 1000, "ANALYSIS"),
            DeviceConfig("position", 1, "ANALYSIS")
        ]
    ),
    Device(
        "TESTACC02",
        "Accelerometer_2",
        "soil inclinometer 2 testing",
        "soil_inclinometer",
        [
            DeviceConfig("slave_id", 0x02, "COMMUNICATION"),
            DeviceConfig("offset-X", 0, "OFFSET"),
            DeviceConfig("offset-Y", 0, "OFFSET"),
            DeviceConfig("offset-Z", 0, "OFFSET"),
            DeviceConfig("space", 1000, "ANALYSIS"),
            DeviceConfig("position", 2, "ANALYSIS")
        ]
    ),
    Device(
        "TESTACC03",
        "Accelerometer_3",
        "soil inclinometer 3 testing",
        "soil_inclinometer",
        [
            DeviceConfig("slave_id", 0x03, "COMMUNICATION"),
            DeviceConfig("offset-X", 0, "OFFSET"),
            DeviceConfig("offset-Y", 0, "OFFSET"),
            DeviceConfig("offset-Z", 0, "OFFSET"),
            DeviceConfig("space", 1000, "ANALYSIS"),
            DeviceConfig("position", 3, "ANALYSIS")
        ]
    ),
    Device(
        "TESTACC04",
        "Accelerometer_4",
        "soil inclinometer 4 testing",
        "soil_inclinometer",
        [
            DeviceConfig("slave_id", 0x04, "COMMUNICATION"),
            DeviceConfig("offset-X", 0, "OFFSET"),
            DeviceConfig("offset-Y", 0, "OFFSET"),
            DeviceConfig("offset-Z", 0, "OFFSET"),
            DeviceConfig("space", 1000, "ANALYSIS"),
            DeviceConfig("position", 4, "ANALYSIS")
        ]
    ),
    Device(
        "TESTACC05",
        "Accelerometer_5",
        "soil inclinometer 5 testing",
        "soil_inclinometer",
        [
            DeviceConfig("slave_id", 0x05, "COMMUNICATION"),
            DeviceConfig("offset-X", 0, "OFFSET"),
            DeviceConfig("offset-Y", 0, "OFFSET"),
            DeviceConfig("offset-Z", 0, "OFFSET"),
            DeviceConfig("space", 1000, "ANALYSIS"),
            DeviceConfig("position", 5, "ANALYSIS")
        ]
    ),
    Device(
        "TESTPIE01",
        "Piezometer_1",
        "piezometer testing",
        "piezometer",
        [
            DeviceConfig("slave_id", 0x80, "COMMUNICATION"),
            DeviceConfig("offset-pressure", 0, "OFFSET"),
            DeviceConfig("offset-depth", 0, "OFFSET")
        ]
    ),
    Device(
        "TESTRAG01",
        "Rain_Gauge_1",
        "rain gauge testing",
        "rain_gauge",
        [
            DeviceConfig("slave_id", 0x90, "COMMUNICATION"),
            DeviceConfig("coefficient", 0.1, "COMMUNICATION")
        ]
    ),
    Device(
        "TESTENV01",
        "Environment_Sensor_1",
        "environment sensor testing",
        "environment",
        [
            DeviceConfig("slave_id", 0xA0, "COMMUNICATION")
        ]
    )
]

GROUPS = [
    Group(
        "ANALYSIS",
        "soil inclinometer",
        "soil inclinometer testing",
        [
            "TESTACC01",
            "TESTACC02",
            "TESTACC03",
            "TESTACC04",
            "TESTACC05"
        ]
    )
]
