import sys
from INA3221_linux import INA3221
import time


ina = INA3221(address=0x40, bus="/dev/i2c-2")

if __name__ == "__main__":

    if not ina.begin():
        print("Could not connect. Fix and Reboot")
        sys.exit(1)
    else:
        print(f"Address: \t{hex(ina.get_address())}")

    print(f"Die ID: \t{hex(ina.get_die_id())}")
    print(f"Manufacture ID: \t{hex(ina.get_manufacturer_id())}")
    print(f"Configuration: \t{hex(ina.get_configuration())}")

    # Set custom shunt resistors
    ina.set_shunt_resistor(0, 0.005)
    ina.set_shunt_resistor(1, 0.005)
    ina.set_shunt_resistor(2, 0.005)

    print("CHAN\tCRITIC\tWARNING")
    for ch in range(3):
        crit = ina.get_critical_alert(ch)
        warn = ina.get_warning_alert(ch)
        print(f"{ch}\t{hex(crit)}\t{hex(warn)}")

    print("Shunt Voltage")
    print(f"  SVSUM:\t{hex(ina.get_shunt_voltage_sum())}")
    print(f"SVLIMIT:\t{hex(ina.get_shunt_voltage_sum_limit())}")

    print("Mask/ Enable")
    print(f"M/E:\t{hex(ina.get_mask_enable())}")

    print("Power Limit")
    print(f"UPPER:\t{hex(ina.get_power_upper_limit())}")
    print(f"LOWER:\t{hex(ina.get_power_lower_limit())}")


    while True:

        print("CHAN    BUS[V]       SHUNT[V]    CURRENT[A]  POWER[W]")
        for ch in range(3):
            bus = ina.get_bus_voltage(ch)
            shunt = ina.get_shunt_voltage(ch)
            current = ina.get_current(ch)
            power = ina.get_power(ch)
            print(f"{ch}       {bus:8.5f}    {shunt:8.5f}    {current:8.5f}    {power:8.5f}")
            time.sleep(1)
