import smbus

bus = smbus.SMBus(1)
adr = 0x33
setupCmd = [0x83]
configCmd = [0x3]
cmd = 2

# bus.write_i2c_block_data(adr, cmd, setupCmd)
# bAck = bus.read_byte(adr)
# print(bAck)


def concat_val(v1, v2):
    init_str = v1 + v2
    # print(init_str) #Debug
    str_len = len(init_str)
    new_str = init_str[6:str_len]
    # print(newStr) #Debug
    print(int(new_str, 2))
    
while True:
    bus.write_i2c_block_data(adr, cmd, configCmd)
    bData = bus.read_i2c_block_data(adr, cmd)
    # bWord = bus.read_word_data(adr, cmd)
    # bByte = bus.read_byte_data(adr, cmd)
    # for x in bData:
    #     if ((x < 50 or x > 60) and x < 250):
    #       print(x)
    b1 = '{0:b}'.format(bData[0])
    b2 = '{0:b}'.format(bData[1])
    concat_val(b1, b2)

    # print(b1) #Debug
    # print(b2) #Debug
    # print(bWord) #Debug
    # print(bByte) #Debug
    
# bus.close()
