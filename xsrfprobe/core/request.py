#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -:-:-:-:-:-:-::-:-:#
#    XSRF Probe     #
# -:-:-:-:-:-:-::-:-:#

# Author: 0xInfection
# This module requires XSRFProbe
# https://github.com/0xInfection/XSRFProbe

import time
from urllib.parse import urljoin

import requests

import xsrfprobe.core.colors

colors = xsrfprobe.core.colors.color()

from xsrfprobe.files.config import (
    HEADER_VALUES,
    COOKIE_VALUE,
    USER_AGENT_RANDOM,
    USER_AGENT,
    DELAY_VALUE,
    DISPLAY_HEADERS,
    TIMEOUT_VALUE,
    VERIFY_CERT,
    FILE_EXTENSIONS,
    EXECUTABLES,
)
from xsrfprobe.core.verbout import verbout
from xsrfprobe.core.randua import RandomAgent
from xsrfprobe.files.discovered import FILES_EXEC
from xsrfprobe.core.logger import presheaders, preqheaders, ErrorLogger  # import ends

headers = HEADER_VALUES  # set the headers

# Set Cookie
if COOKIE_VALUE:
    headers["Cookie"] = ",".join(cookie for cookie in COOKIE_VALUE)

# Set User-Agent
if USER_AGENT_RANDOM:
    headers["User-Agent"] = RandomAgent()
if USER_AGENT:
    headers["User-Agent"] = USER_AGENT


def Post(url, action, data):
    """
    The main use of this function is as a
           Form Requester [POST].
    """
    global headers, TIMEOUT_VALUE, VERIFY_CERT
    time.sleep(DELAY_VALUE)  # If delay param has been supplied
    verbout(colors.GR, "Preparing the request...")

    if DISPLAY_HEADERS:
        preqheaders(headers)

    verbout(colors.GR, f"Processing the {colors.GREY}POST{colors.END} Request...")
    main_url = urljoin(url, action)  # join url and action
    try:
        # Make the POST Request.
        response = requests.post(
            main_url,
            headers=headers,
            data=data,
            timeout=TIMEOUT_VALUE,
            verify=VERIFY_CERT,
        )
        if DISPLAY_HEADERS:
            presheaders(response.headers)
        return response  # read data content
    except requests.exceptions.HTTPError as e:  # if error
        verbout(colors.R, "HTTP Error : " + main_url)
        ErrorLogger(main_url, e.__str__())
        return None
    except requests.exceptions.ConnectionError as e:
        verbout(colors.R, "Connection Aborted : " + main_url)
        ErrorLogger(main_url, e.__str__())
        return None
    except requests.exceptions.ReadTimeout as e:
        verbout(colors.R, "Exception at: " + colors.GREY + url)
        verbout(
            colors.R,
            "Error: Read Timeout. Consider increasing the timeout value via --timeout.",
        )
        ErrorLogger(url, e.__str__())
        return None
    except ValueError as e:  # again if valuerror
        verbout(colors.R, "Value Error : " + main_url)
        ErrorLogger(main_url, e.__str__())
        return None
    except Exception as e:
        verbout(colors.R, "Exception Caught: " + e.__str__())
        ErrorLogger(main_url, e.__str__())
        return None  # if at all nothing happens :(


def Get(url, headers=headers):
    """
    The main use of this function is as a
            Url Requester [GET].
    """
    global TIMEOUT_VALUE, VERIFY_CERT
    # We do not verify the request while GET requests
    time.sleep(DELAY_VALUE)  # We make requests after the time delay
    # Making sure the url is not a file
    if url.split(".")[-1].lower() in (FILE_EXTENSIONS or EXECUTABLES):
        FILES_EXEC.append(url)
        verbout(colors.G, "Found File: " + colors.BLUE + url)
        return None
    try:
        verbout(colors.GR, "Preparing the request...")

        if DISPLAY_HEADERS:
            preqheaders(headers)

        verbout(
            colors.GR,
            f"Processing the {colors.GREY}GET{colors.END} Request...",
        )

        req = requests.get(
            url,
            headers=headers,
            timeout=TIMEOUT_VALUE,
            stream=False,
            verify=VERIFY_CERT,
        )

        if req is None:
            verbout(colors.RED, f" [!] Failed to get a response from: {url}")
            return None

        # Displaying headers if DISPLAY_HEADERS is 'True'
        if DISPLAY_HEADERS:
            presheaders(req.headers)

        # Return the object
        return req
    except requests.exceptions.MissingSchema as e:
        verbout(colors.R, "Exception at: " + colors.GREY + url)
        verbout(colors.R, "Error: Invalid URL Format")
        ErrorLogger(url, e.__str__())
        return None
    except requests.exceptions.ReadTimeout as e:
        verbout(colors.R, "Exception at: " + colors.GREY + url)
        verbout(
            colors.R,
            "Error: Read Timeout. Consider increasing the timeout value via --timeout.",
        )
        ErrorLogger(url, e.__str__())
        return None
    except requests.exceptions.HTTPError as e:  # if error
        verbout(colors.R, "HTTP Error Encountered : " + url)
        ErrorLogger(url, e.__str__())
        return None
    except requests.exceptions.ConnectionError as e:
        verbout(colors.R, "Connection Aborted : " + url)
        ErrorLogger(url, e.__str__())
        return None
    except Exception as e:
        verbout(colors.R, "Exception Caught: " + e.__str__())
        ErrorLogger(url, e.__str__())
        return None
