import socket
import pprint
import struct
import traceback
import numpy as np
seqnum = 0
sock = 0


def bytesToInt(ba):
    result = 0
    i = 0
    for b in ba:
        result += ord(b) << ((len(b)-i)*8)
        i = i+1;
    return result

def ACNData(data):
    ACNDataPacket = {
        # ----------Root Layer-----------#
        "Root": {
            "preambleSize": bytesToInt(data[0:2]),
            "postamleSize": bytesToInt(data[2:4]),
            "id": data[4:16],
            "RLPPDULength": ((ord(data[16]) & 0x0F) << 8) + ord(data[17]),
            "vector": data[18:22],
            "cid": data[22:38]
        },
        # -----E1.31 Framing Layer-------#
        "Framing": {
            "flags": ord(data[38]) & 0xF0,
            "PDULength": ((ord(data[38]) & 0x0F) << 8) + ord(data[39]),
            "vector": data[40:44],
            "sourceName": "".join(data[44:108]),
            "priority": bytesToInt(data[108]),
            "syncAddress": data[109:111],
            "seqNum": ord(data[111]),
            "options": ord(data[112]),
            "universe": bytesToInt(data[113:115])
        },
        # ------------DMP Layer----------#
        "DMP": {
            "flags": ord(data[115]) & 0xF0,
            "PDULength": ((ord(data[115]) & 0x0F) << 8) + ord(data[116]),
            "vector": data[117],
            "addrAndDataType": data[118],  # Always contains 0xa1
            # Always contains 0x0000, indicates position of start code
            "firstPropertyAdress": bytesToInt(data[119:121]),
            "addressIncrement": data[121:123],  #
            "propertyValueCount": data[123:125],
            "propertyValues": [ord(d) for d in data[126:638]],
        }
    }
    return ACNDataPacket

def dump(packet):
    print "#############################################################"
    pp = pprint.PrettyPrinter(indent = 2)
    pp.pprint(packet)

def capturesACN():
    global sock
    #print "Running ACN capture..."

    # Receive with buffer size of 1024 bytes.
    # The ACN packets received will be <700 bytes
    # So 1024 is sufficient. This is a blocking call.
    data, addr = sock.recvfrom(1024)
   # print "received from:",addr
    if (data[4:16] == "ASC-E1.17\0\0\0"):
        ACN = ACNData(data)
        return ACN
        #dump(ACN)
        #print data
        #print ACN["DMP"]["propertyValues"]
    else:
        print id, "Not sACN"

def sendsACN(universe, startcode, dmxData):
    global seqnum
    global sock

    if not (type(dmxData) is list):
        return

    seqnum = seqnum+1
    data = [0]*638
    data[0:2] = [1,6]
    data[2:4] = [0,0]
    data[4:16] = [ord(c) for c in "ASC-E1.17"]
    data[16] = (622 & 0x0F00) # RLPPDU high
    data[17] = (622 & 0x00FF) # RLPPDU low
    data[18:22] = [0,0,0,4]
    #data[22:38] # cid
    data[38] = 112
    data[38] = (600 & 0x0F00) # PDU Length High
    data[39] = (600 & 0x00FF) # PDU Length Low
    data[40:44] = [0,0,0,2]
    data[44:108] = [ord(c) for c in "Noah Meltzer ACN LED Matrix"]
    data[108] = 256
    data[109:111] = [0,0] # Sync address
    data[111] = seqnum
    data[112] = 40
    data[113] = universe & 0xFF00 # universe high
    data[114] = universe & 0x00FF # universe low
    data[115] = 112 & 0xF0
    data[115] = (523 & 0x0F) # PDU Length High
    data[116] = (523 & 0x00FF) # PDU Length Low
    data[117] = 2 # vector
    data[118] = 161 # Address and data type
    data[119:121] = [0,0]
    data[121:123] = [0,1]
    data[123:125] = [2,1]
    rawdat = [startcode]
    rawdat.extend(dmxData)
    data[125:638] = rawdat




    # Receive with buffer size of 1024 bytes.
    # The ACN packets received will be <700 bytes
    # So 1024 is sufficient. This is a blocking call.
   # print "sending..."
   # print data
    data = [chr(b) if b<256 else chr(0) for b in data]
    try:
       sock.sendto("".join(data),
                ('239.255.0.1', 5568))
        #sock.send("".join(data))
    except:
       # print data
        traceback.print_exc()

  #  print "done sending..."
def init(ip):
    global sock
  # Create UDP socket
    sock = socket.socket(socket.AF_INET,  # Use internet protocol
                        socket.SOCK_DGRAM,
                        socket.IPPROTO_UDP)  # Receive UDP
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    # Bind our new socket to the IP address and port
    print "binding to port..."

    UDP_IP = ip  # Loopback IP
    UDP_PORT = 5568  # ACN-SDT
    #sock.bind((UDP_IP, UDP_PORT))
    #sock.listen(1)
    sock.bind(('', UDP_PORT))
    multicast_group = "239.255.0.1"
    group = socket.inet_aton(multicast_group)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    print "done binding."
    #sock.connect((UDP_IP, UDP_PORT))
    #sock.listen(1)
    #conn, addr = sock.accept()