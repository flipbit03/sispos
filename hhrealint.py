# -*- coding: cp1252 -*-
import os
import re

# derive this from HHReal instead of BaseSISPOS
from hhreal import HHReal



class HHRealInt(HHReal):
    # ----------------------------------
    # Initalization parameters
    # ----------------------------------

    # No  init needed because of HHReal's .dynfindfiles() method (Uses class name to find files)

    # "pass" needed as there are no instructions in this class
    pass 

if __name__ == "__main__":
    a = HHRealInt()
    r = a.run()
