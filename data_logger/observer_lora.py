from LoRaRF import SX126x, LoRaSpi, LoRaGpio
import time
from datetime import datetime

# Begin LoRa radio with connected SPI bus and IO pins (cs and reset) on GPIO
# SPI is defined by bus ID and cs ID and IO pins defined by chip and offset number
spi = LoRaSpi(3, 0)
cs = LoRaGpio(4, 6)
reset = LoRaGpio(4, 1)
busy = LoRaGpio(4, 3)
LoRa = SX126x(spi, cs, reset, busy)
print("Begin LoRa radio")
if not LoRa.begin() :
    raise Exception("Something wrong, can't begin LoRa radio")

# Configure LoRa to use TCXO with DIO3 as control
print("Set RF module to use TCXO as clock reference")
LoRa.setDio3TcxoCtrl(LoRa.DIO3_OUTPUT_1_8, LoRa.TCXO_DELAY_10)

# Set frequency to 915 Mhz
print("Set frequency to 915 Mhz")
LoRa.setFrequency(915000000)

# Set RX gain. RX gain option are power saving gain or boosted gain
print("Set RX gain to power saving gain")
LoRa.setRxGain(LoRa.RX_GAIN_POWER_SAVING)                       # Power saving gain

LoRa.setTxPower(22)

# Configure modulation parameter including spreading factor (SF), bandwidth (BW), and coding rate (CR)
# Receiver must have same SF and BW setting with transmitter to be able to receive LoRa packet
print("Set modulation parameters:\n\tSpreading factor = 8\n\tBandwidth = 125 kHz\n\tCoding rate = 4/5")
sf = 8                                                          # LoRa spreading factor: 8
bw = 125000                                                     # Bandwidth: 125 kHz
cr = 5                                                          # Coding rate: 4/5
LoRa.setLoRaModulation(sf, bw, cr)

# Configure packet parameter including header type, preamble length, payload length, and CRC type
# The explicit packet includes header contain CR, number of byte, and CRC type
# Receiver can receive packet with different CR and packet parameters in explicit header mode
print("Set packet parameters:\n\tExplicit header type\n\tPreamble length = 12\n\tPayload Length = 15\n\tCRC on")
headerType = LoRa.HEADER_EXPLICIT                               # Explicit header mode
preambleLength = 12                                             # Set preamble length to 12
payloadLength = 15                                              # Initialize payloadLength to 15
crcType = True                                                  # Set CRC enable
LoRa.setLoRaPacket(headerType, preambleLength, payloadLength, crcType)

# Set syncronize word for public network (0x3444)
print("Set syncronize word to 0x3444")
LoRa.setSyncWord(0x3444)

print("\n-- LoRa Receiver --\n")

# Receive message continuously
while True :

    # Request for receiving new LoRa packet and wait for incoming LoRa packet
    LoRa.request()
    LoRa.wait()

    if LoRa.available():

        # Get received message from incoming LoRa packet
        t = round(time.time())
        time_str = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
        data = LoRa.read(LoRa.available())

        # Transmit timestamp to synchronize time
        # if (t % 60) != 2:
        LoRa.beginPacket()
        LoRa.write(data[0])     # gateway id
        LoRa.write(data[1])     # node id
        LoRa.write(1)           # time synchronize code
        LoRa.write((t >> 24) % 256)
        LoRa.write((t >> 16) % 256)
        LoRa.write((t >> 8) % 256)
        LoRa.write(t % 256)
        LoRa.endPacket()
        LoRa.wait()

        # Print time, received message, and packet/signal status
        message = "("
        for i, d in enumerate(data):
            message += "{:3d}".format(d)
            if i < (len(data) - 1): message += ","
        message += ")"
        print("{}    {}    RSSI: {} | SNR: {}".format(time_str, message, LoRa.packetRssi(), LoRa.snr()))

        # Show received status in case CRC or header error occur
        status = LoRa.status()
        if status == LoRa.STATUS_CRC_ERR : print("CRC error")
        elif status == LoRa.STATUS_HEADER_ERR : print("Packet header error")
