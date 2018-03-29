import mss
import numpy as np
import win32api
def getScreenPixels(pxx, pxy):
    with mss.mss() as sct:
        # Get a screenshot of the 1st monitor
       # print sct.monitors
        x,y = win32api.GetCursorPos()
        monitor = {'top':y, 'left':x, 'width':pxx, 'height':pxy}
        sct_img = sct.grab(monitor)

        # Create an Image
      # img = Image.new('RGB', sct_img.size)
        pixels = []
        # Best solution: create a list(tuple(R, G, B), ...) for putdata()


        #aa = [a << 24 for a in sct_img.raw[3::4]]
        bb = [b<<16 for b in sct_img.raw[2::4]]
        gg = [g<<8 for g in sct_img.raw[1::4]]
        rr = [r<<0 for r in sct_img.raw[0::4]]
        for i,b in enumerate(bb):
            pixels.append(rr[i]|gg[i]|bb[i]|0x00)
           # pixels.append(rr[i]|0|0)

       # print pixels[1:16]
        pixels = np.array(pixels)
        #pixels = np.array(zip(
         #                   sct_img.raw[3::4],
          #                  sct_img.raw[2::4],
           #                 sct_img.raw[1::4],
            #                sct_img.raw[0::4],))
        #print pixels.shape
        return pixels
