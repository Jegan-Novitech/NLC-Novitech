import time
import smbus
import json
i2c_ch = 1

# TMP102 address on the I2C bus
i2c_address = 0x0a
D6T_CMD= 0x4C
f=open("/home/faren-t/share/config",'r')
test_string = f.read()
f.close()
res = json.loads(test_string)
host_ip=res['host_ip']
port_no=res['port_no']
calib_value=res['calib_value']
temp=res['temp_thresh']
# Calculate the 2's complement of a number
def twos_comp(val, bits):
    if (val & (1 << (bits - 1))) != 0:
        val = val - (1 << bits)
    return val

# Read temperature registers and calculate Celsius
def read_temp():
    try:
            # Read temperature registers
            val = bus.read_i2c_block_data(i2c_address, D6T_CMD,35)
##            bus.write_i2c_block_data(i2c_address, D6T_CMD, 35)
##            print(val)

            temp_c = (val[0] << 4) | (val[1] >> 4)
            temp_c = twos_comp(temp_c, 12)

            # Convert registers value to temperature (C)
            temp_c = temp_c * 0.0625

            tp = []
            tptat = 0
            data=[0,val]
##            print(data[1][33])
            tp.append((data[1][3] * 256 + data[1][2]) / 10.0)
            tp.append((data[1][5] * 256 + data[1][4]) / 10.0)
            tp.append((data[1][7] * 256 + data[1][6]) / 10.0)
            tp.append((data[1][9] * 256 + data[1][8]) / 10.0)
            tp.append((data[1][11] * 256 + data[1][10]) / 10.0)
            tp.append((data[1][13] * 256 + data[1][12]) / 10.0)
            tp.append((data[1][15] * 256 + data[1][14]) / 10.0)
            tp.append((data[1][17] * 256 + data[1][16]) / 10.0)
            tp.append((data[1][19] * 256 + data[1][18]) / 10.0)
            tp.append((data[1][21] * 256 + data[1][20]) / 10.0)
            tp.append((data[1][23] * 256 + data[1][22]) / 10.0)
            tp.append((data[1][25] * 256 + data[1][24]) / 10.0)
            tp.append((data[1][27] * 256 + data[1][26]) / 10.0)
            tp.append((data[1][29] * 256 + data[1][28]) / 10.0)
            tp.append((data[1][31] * 256 + data[1][30]) / 10.0)
            tp.append((data[1][33] * 256 + data[1][32]) / 10.0)

            tptat = (data[1][1] * 256 + data[1][0]) / 10.0
    except IndexError:
            print('got an incorrect index.')
            return None,None
    
    return tp, tptat

# Initialize I2C (SMBus)
bus = smbus.SMBus(i2c_ch)

# Read the CONFIG register (2 bytes)D6T_CMD
try:
    val = bus.read_i2c_block_data(i2c_address,D6T_CMD , 35)
##    print("Old CONFIG:", val)

    # Set to 4 Hz sampling (CR1, CR0 = 0b10)
    val[1] = val[1] & 0b00111111
    val[1] = val[1] | (0b10 << 6)
    bus.write_i2c_block_data(i2c_address, D6T_CMD, 35)
except:
    pass


# Print out temperature every second
def get_temp():
    while True:
        try:
            tpn, tptat = read_temp()
            print(tpn)
##            tpn1=tpn[0:4]+tpn[4:8]
            calib_temp=round((36.0+(36.3-33.5)*(max(tpn1)-41.3)/(50-41.3))/calib_value,1)
##            print(calib_temp,max(tpn1))
            temp=float(round((calib_temp* 9/5 + 32),1))
##            print(temp, "°F")
            return temp
        except:
            pass
##        time.sleep(1)

##get_temp()
