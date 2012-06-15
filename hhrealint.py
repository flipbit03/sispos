# -*- coding: cp1252 -*-
import os
import re

# derive this from HHReal instead of BaseSISPOS
from hhreal import HHReal



class HHRealInt(HHReal):
    # ----------------------------------
    # Initalization parameters
    # ----------------------------------

    # Internal file name has to be Class name in UPPERCASE --> HHREALINT
    # because of HHReal's process() method file access method --> f[sel.f__class__.__name__.upper()]
    # This way we can reuse HHReal's methods without having to recode everything because of the file name
    findfiles = ( ("HHREALINT","hhrealint"), )
                                                    

if __name__ == "__main__":
    a = HHRealInt()
    r = a.run()
