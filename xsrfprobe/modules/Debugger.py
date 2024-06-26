#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -:-:-:-:-:-:-:-:-:#
#    XSRFProbe     #
# -:-:-:-:-:-:-:-:-:#

# Author: 0xInfection
# This module requires XSRFProbe
# https://github.com/0xInfection/XSRFProbe

import re
import string
from random import Random

import xsrfprobe.core.colors

colors = xsrfprobe.core.colors.color()

from xsrfprobe.files.config import EMAIL_VALUE, TEXT_VALUE, TOKEN_GENERATION_LENGTH
from xsrfprobe.core.verbout import verbout


class Form_Debugger:
    def prepareFormInputs(self, form):
        """
        This method parses form types and generates strings based
                        on their input types.
        """
        verbout(colors.O, "Crafting inputs as form type...")
        cr_input = {}
        totcr = []

        verbout(colors.GR, f"Processing {colors.BOLD}<input type='text' name='...")
        # get name type inputs

        for m in form.findAll("input", {"name": True, "type": "text"}):
            # Empty is the default value
            value = ""
            try:
                if m["value"]:  # Ignore case while searching for a match
                    value = m["value"].encode(
                        "utf8"
                    )  # make sure no encoding errors there
            except KeyError:
                value = TEXT_VALUE
            cr_input[m["name"]] = value  # assign passed on value
            cr0 = {}
            cr0["type"] = "text"
            cr0["name"] = m["name"]
            cr0["label"] = m["name"].title()
            cr0["value"] = ""
            totcr.append(cr0)

        verbout(colors.GR, f"Processing {colors.BOLD}<input type='email' name='...")
        # get password inputs

        for m in form.findAll("input", {"name": True, "type": "email"}):
            value = EMAIL_VALUE
            if m["value"]:  # Ignore case while searching for a match
                value = m["value"].encode("utf8")  # make sure no encoding errors there
            cr_input[m["name"]] = value  # assign passed on value
            cr1 = {}
            cr1["type"] = "email"
            cr1["name"] = m["name"]
            cr1["label"] = "Email"
            cr1["value"] = ""
            totcr.append(cr1)

        verbout(colors.GR, f"Processing {colors.BOLD}<input type='password' name='...")
        # get password inputs

        for m in form.findAll("input", {"name": True, "type": "password"}):
            # Empty is the default value
            value = ""
            try:  # Ignore case while searching for a match
                if m["value"]:
                    value = m["value"].encode(
                        "utf8"
                    )  # make sure no encoding errors there
            except KeyError:
                value = randString()

            cr_input[m["name"]] = value  # assign passed on value
            cr2 = {}
            cr2["type"] = "password"
            cr2["name"] = m["name"]
            cr2["label"] = "Password"
            cr2["value"] = ""
            totcr.append(cr2)

        try:
            verbout(
                colors.GR,
                f"Processing {colors.BOLD}<input type='hidden' name='...",
            )
            # get hidden input types

            for m in form.findAll("input", {"name": True, "type": "hidden"}):
                # Empty is the default value
                value = ""
                if re.search(
                    "value=", m.__str__(), re.IGNORECASE
                ):  # Ignore case while searching for a match
                    value = m["value"]  # make sure no encoding errors there
                else:
                    value = TEXT_VALUE

                cr_input[m["name"]] = value  # assign passed on value
                cr3 = {}
                cr3["type"] = "hidden"
                cr3["name"] = m["name"]
                cr3["label"] = ""  # Nothing since its a hidden field
                cr3["value"] = value
                totcr.append(cr3)
        except KeyError:
            cr3["value"] = ""

        verbout(colors.GR, f"Processing {colors.BOLD}<input type='submit' name='...")
        # get submit buttons :D

        for m in form.findAll("input", {"name": True, "type": "submit"}):
            # Empty is the default value
            value = ""
            if re.search(
                "value=", str(m).strip(), re.IGNORECASE
            ):  # Ignore case while searching for a match
                value = m["value"].encode("utf8")  # make sure no encoding errors there
            else:
                value = "Submit"

            cr_input[m["name"]] = value  # assign passed on value

        verbout(colors.GR, f"Processing {colors.BOLD}<input type='checkbox' name='...")
        # get checkbox type inputs

        for m in form.findAll("input", {"name": True, "type": "checkbox"}):
            # Empty is the default value
            value = ""
            if re.search(
                "value=", m.__str__(), re.IGNORECASE
            ):  # Ignore case while searching for a match
                value = m["value"].encode("utf8")  # make sure no encoding errors there
            else:
                value = randString()  # assign passed on value

            cr_input[m["name"]] = value  # assign discovered value
            cr4 = {}
            cr4["type"] = "checkbox"
            cr4["name"] = m["name"]
            cr4["label"] = m["name"].title()
            cr4["value"] = ""
            totcr.append(cr4)

        verbout(colors.GR, f"Processing {colors.BOLD}<input type='radio' name='...")
        # get radio buttons :D

        listRadio = []
        for m in form.findAll("input", {"name": True, "type": "radio"}):
            # Empty is the default value
            value = ""
            if (not m["name"] in listRadio) and re.search(
                "value=", str(m).strip(), re.IGNORECASE
            ):  # Ignore case while searching for a match
                listRadio.append(m["name"])
                cr_input[m["name"]] = value.encode(
                    "utf8"
                )  # make sure no encoding errors there
                cr5 = {}
                cr5["type"] = "radio"
                cr5["name"] = m["name"]
                cr5["label"] = m["name"].title()
                cr5["value"] = ""
                totcr.append(cr5)

        verbout(colors.GR, f"Processing {colors.BOLD} <textarea name='...")
        # get textarea input types

        for m in form.findAll("textarea", {"name": True}):
            # m.contents is an array of lines
            if len(m.contents) == 0:
                m.contents.append(randString())  # get random strings

            cr_input[m["name"]] = m.contents[0].encode(
                "utf8"
            )  # make sure no encoding errors there

            cr6 = {}
            cr6["type"] = "text"
            cr6["name"] = m["name"]
            cr6["label"] = m["name"].title()
            cr6["value"] = ""
            totcr.append(cr6)

        verbout(colors.GR, f"Processing {colors.BOLD}<select name='...")
        # selection type inputs

        for m in form.findAll("select", {"name": True}):
            if m.findAll("option", value=True):
                name = m["name"]  # assign passed on value
                cr_input[name] = m.findAll("option", value=True)[0]["value"].encode(
                    "utf8"
                )  # find forms fields based on value

        verbout(colors.GR, "Parsing final inputs...")
        return (cr_input, totcr)  # Return the form input types


def randString():  # generate random strings
    verbout(colors.GR, "Compiling strings...")
    return "".join(
        Random().sample(string.ascii_letters, TOKEN_GENERATION_LENGTH)
    )  # any chars to be generated as form field inputs


def getAllForms(soup):  # get all forms
    return soup.findAll(
        "form", method=re.compile("post", re.IGNORECASE)
    )  # get forms with post method only
