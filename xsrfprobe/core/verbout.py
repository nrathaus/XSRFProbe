#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -:-:-:-:-:-:-::-:-:#
#    XSRF Probe     #
# -:-:-:-:-:-:-::-:-:#

# Author: 0xInfection
# This module requires XSRFProbe
# https://github.com/0xInfection/XSRFProbe

from xsrfprobe.files.config import DEBUG as verbose


def verbout(stat, content_info):
    """
    This module is for giving a verbose
                output.
    """
    # If debug mode is chosen as True
    if verbose:
        # Concatenate the stat type and string value and print out
        print(stat + content_info)
