import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from dataclasses import dataclass
import time
from datetime import datetime
from uuid import UUID
import grpc
from rmcs_api_client.auth import Auth
from rmcs_api_client.resource import Resource, DeviceSchema
import config
from LoRaRF import SX126x, LoRaSpi, LoRaGpio


@dataclass
class DeviceMap:
    id: UUID
    model: UUID
    type: str
    length: int
    period: int
    offset: int

@dataclass
class Id:
    gateway: int
    node: int
    def __hash__(self):
        return self.gateway * 256 + self.node

@dataclass
class Transmit:
    id: Id
    code: int
    data: int

@dataclass
class Receive:
    id: Id
    binary: tuple[int]


# Command code definition
CMD_CODE_END                          =  0x00
CMD_CODE_SYNCRONIZE_S                 =  0x01
CMD_CODE_RETRANSMIT_0                 =  0x0A
CMD_CODE_RETRANSMIT_1                 =  0x0B
CMD_CODE_RETRANSMIT_2                 =  0x0C
CMD_CODE_RETRANSMIT_3                 =  0x0D
CMD_CODE_RETRANSMIT_4                 =  0x0E

# Get gateway ID from input argument and corresponding configurations from config file
invalid = True
if len(sys.argv) > 1:
    gateway_id = sys.argv[1]
    if gateway_id in config.GATEWAY_LORA:
        GATEWAY = config.GATEWAY_LORA[gateway_id]
        if all(k in GATEWAY for k in ("spi", "cs", "reset", "busy")):
            if "frequency" not in GATEWAY: GATEWAY['frequency'] = 915000000
            if "sf" not in GATEWAY: GATEWAY['sf'] = 7
            if "bw" not in GATEWAY: GATEWAY['bw'] = 125000
            if "cr" not in GATEWAY: GATEWAY['cr'] = 5
            invalid = False
if invalid:
    raise Exception("Gateway ID input missing, invalid format, or invalid gateway configuration")

# Begin LoRa radio with connected SPI bus and IO pins (cs and reset) on GPIO
spi = LoRaSpi(GATEWAY['spi'][0], GATEWAY['spi'][1])
cs = LoRaGpio(GATEWAY['cs'][0], GATEWAY['cs'][1])
reset = LoRaGpio(GATEWAY['reset'][0], GATEWAY['reset'][1])
busy = LoRaGpio(GATEWAY['busy'][0], GATEWAY['busy'][1])
LoRa = SX126x(spi, cs, reset, busy)
print("Begin LoRa radio")
if not LoRa.begin() :
    raise Exception("Something wrong, can't begin LoRa radio")

# Setting LoRa modem configuration based on gateway setting in database
print("Set RF module to use TCXO as clock reference")
LoRa.setDio3TcxoCtrl(LoRa.DIO3_OUTPUT_1_8, LoRa.TCXO_DELAY_10)
print("Set frequency to {} Mhz".format(GATEWAY['frequency']/1000000.0))
LoRa.setFrequency(GATEWAY['frequency'])
print("Set TX power to +22 dBm")
LoRa.setTxPower(22)
print("Set RX gain to boosted gain")
LoRa.setRxGain(LoRa.RX_GAIN_BOOSTED)
print("Set modulation parameters:\n\tSpreading factor = {}\n\tBandwidth = {} kHz\n\tCoding rate = 4/{}".format(GATEWAY['sf'], GATEWAY['bw'], GATEWAY['cr']))
LoRa.setLoRaModulation(GATEWAY['sf'], GATEWAY['bw'], GATEWAY['cr'])
print("Set packet parameters:\n\tExplicit header type\n\tPreamble length = 12\n\tPayload Length = 15\n\tCRC on")
LoRa.setLoRaPacket(LoRa.HEADER_EXPLICIT, 12, 15, True)
print("Set syncronize word to 0x3444")
LoRa.setSyncWord(0x3444)


# User login
address_auth = config.SERVER_LOCAL['address_auth']
address_resource = config.SERVER_LOCAL['address_resource']
auth = Auth(address_auth)
login = auth.user_login(config.SERVER_LOCAL['admin_name'], config.SERVER_LOCAL['admin_password'])
resource = Resource(address_resource, login.access_tokens[0].access_token)

print("LOGIN:")
print("user_id       = {}".format(login.user_id))
print("auth_token    = {}".format(login.auth_token))
for token in login.access_tokens:
    print("api_id        = {}".format(token.api_id))
    print("access_token  = {}".format(token.access_token))
    print("refresh_token = {}".format(token.refresh_token))

# Read devices associated with configured gateway
device_map: dict[Id, DeviceMap] = {}
devices: list[DeviceSchema] = []
for gateway_id in config.GATEWAYS:
    device_list = resource.list_device_by_gateway(UUID(gateway_id))
    for index, device in enumerate(device_list):
        if device.id == device.gateway_id:
            device_list.pop(index)
    devices = devices + device_list
for device in devices:
    if device.id != device.gateway_id: # filter out gateway
        gateway_id = None
        node_id = None
        length = None
        period = None
        offset = None
        for conf in device.configs:
            if conf.name == "gateway_id":
                gateway_id = conf.value
            elif conf.name == "node_id":
                node_id = conf.value
            elif conf.name == "data_length":
                length = conf.value
            elif conf.name == "period_time":
                period = conf.value
            elif conf.name == "offset_time":
                offset = conf.value
        for model_id in device.type.models:
            model = resource.read_model(model_id)
            if model.category == "RAW" and gateway_id != None and node_id != None and length != None and period != None and offset != None:
                id = Id(gateway_id, node_id)
                device_map[id] = DeviceMap(device.id, model_id, device.type.name, length, period, offset)
for id, device in device_map.items():
    print("[{:3d},{:3d}]    {}".format(id.gateway, id.node, device))

def lora_transmit(transmit: Transmit, timeout: int = LoRa.TX_SINGLE):
    # Transmit a LoRa packet containing gatewayId, nodeId, deviceId, and data
    LoRa.beginPacket()
    LoRa.write(transmit.id.gateway)
    LoRa.write(transmit.id.node)
    LoRa.write(transmit.code)
    LoRa.write((transmit.data >> 24) & 0xFF)
    LoRa.write((transmit.data >> 16) & 0xFF)
    LoRa.write((transmit.data >> 8) & 0xFF)
    LoRa.write(transmit.data & 0xFF)
    LoRa.endPacket(timeout)
    # Wait modulation to finish
    LoRa.wait(timeout)

def lora_receive(timeout: int = LoRa.RX_SINGLE) -> Receive | None:
    # Request for a LoRa packet
    if LoRa.request(timeout):
        # Wait modulation to finish
        LoRa.wait(timeout)
        # Only continue when status is STATUS_RX_DONE
        if LoRa.status() != LoRa.STATUS_RX_DONE: return None
        # Filter LoRa packet by length
        if LoRa.available() <= 2: return None
        # Check gateway ID and get node ID
        id = Id(LoRa.read(), LoRa.read())
        # Get received message
        return Receive(id, LoRa.read(LoRa.available()))


while True:

    # Get received data from node
    receive = lora_receive()
    if receive:

        # Get current time
        timeNow = time.time()
        timeString = datetime.fromtimestamp(round(timeNow)).strftime('%Y-%m-%d %H:%M:%S')

        # Filter unrecocognized node and get device configurations
        if receive.id in device_map:
            device = device_map[receive.id]
            if len(receive.binary) != device.length:
                print("{}    [{:3d},{:3d}]    Invalid data length".format(timeString, receive.id.gateway, receive.id.node))
                continue
        else:
            print("{}    Received an unrecognized node LoRa packet".format(timeString))
            continue
        # Calculate measurement time and time drift
        timeData = timeNow - timeNow % device.period
        timeDrift = timeData + device.offset - timeNow

        # Check actual incoming data time
        if abs(timeDrift) > config.TIMING['max_drift']:
            # Send synchronize command when actual incoming data time drifted from incoming data time based on setting
            timeSync = round(timeNow)
            lora_transmit(Transmit(receive.id, CMD_CODE_SYNCRONIZE_S, timeSync))
            print("Node time has been synchronized. Time drift {}".format(timeDrift))
        else:
            # Send end period command
            lora_transmit(Transmit(receive.id, CMD_CODE_END, 0))

        try:
            message = "("
            for i, d in enumerate(receive.binary):
                message += "{:3d}".format(d)
                if i < (len(receive.binary) - 1): message += ","
            message += ")"
            print("{}    {}    [{:3d},{:3d}]    {}    RSSI: {} | SNR: {}".format(timeString, device.id, receive.id.gateway, receive.id.node, message, LoRa.packetRssi(), LoRa.snr()))
            # Create buffer data with configured status
            resource.create_buffer(device.id, device.model, datetime.fromtimestamp(timeData), receive.binary, "ANALYSIS_1")

        except grpc.RpcError as error:
            if error.code() == grpc.StatusCode.UNAUTHENTICATED:
                login = auth.user_login(config.SERVER_LOCAL['admin_name'], config.SERVER_LOCAL['admin_password'])
                resource = Resource(address_resource, login.access_tokens[0].access_token)
                print("RELOGIN LOCAL")
            else:
                print(error)
