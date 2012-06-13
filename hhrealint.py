# -*- coding: cp1252 -*-
import os
import re

# derive this from HHReal instead of BaseSISPOS
from hhreal import HHReal

class HHRealInt(HHReal):
    # ----------------------------------
    # Initalization parameters
    # ----------------------------------
    findfiles = ( ("HHREALINT","hhrealint"), )

if __name__ == "__main__":
    a = HHRealInt()
    r = a.run()
