import sACNTools
import sys
sACNTools.init("239.255.0.1")
print "Running sACN Capture"
while(1):
    ACN = sACNTools.capturesACN()
    sys.stdout.write("%s\r" % str(ACN["DMP"]["propertyValues"][0:10]))
    sys.stdout.flush()