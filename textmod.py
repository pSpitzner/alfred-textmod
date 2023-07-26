#!python3
# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------ #
# all main functions return the manipulated text `ret`,
# or a tuple of (top, sub, ret, ok) for json output as required by alfred,
# if the function is called with `json=True`.
# ------------------------------------------------------------------------------ #


import sys
import re

# import json

# from datetime import datetime
# import dateutil.parser
# import textwrap

# configurable default values


def shorten(text, max_chars=75):
    # shorten and remove newline for alfred preview
    return (text[:max_chars] + "...") if len(text) > max_chars else text.rstrip("\n")


def alfred_json(title, sub, arg, valid, uid, icon="icon.png"):
    # creates the dicts needed for `print(json.dumps(result))`
    # result = {"items": []} then append the dicts from here
    return {
        "title": title,
        "subtitle": sub,
        "valid": valid,
        "uid": uid,
        "icon": {"path": icon},
        "arg": arg,
    }

# ------------------------------------------------------------------------------ #
# Main formatting functions
# ------------------------------------------------------------------------------ #


def underline(text, json=False, char="-"):
    sub = f"Underline with {char}"
    arg = ""
    title = char * 4 + " " + shorten(text, 75 - 10) + " " + char * 4
    valid = True
    lines = text.splitlines(False)
    for l in lines:
        # count leading white spaces for indent
        num_chars = len(l.lstrip(" "))
        num_white = len(l) - num_chars
        underline = " " * num_white + char * num_chars
        arg = arg + l + "\n" + underline + "\n"
    if json:
        # get the current function name from the stack
        uid = sys._getframe().f_code.co_name
        return alfred_json(title, sub, arg, valid, uid)
    else:
        return arg


def remove_newlines(text, json=False):
    sub = "Replace all newlines with a space"
    try:
        arg = text.replace("\n", " ")
        title = shorten(arg)
        valid = True
    except:
        arg = ""
        title = "Remove all newlines"
        valid = False
    if json:
        uid = sys._getframe().f_code.co_name
        return alfred_json(title, sub, arg, valid, uid)
    else:
        return arg


def remove_redundant_space(text, json=False, keep_indent=True):
    sub = "Remove all recurrent spaces and tabs except at the start of a line"
    try:
        if keep_indent:
            # use a regexp to replace all spaces that occur more than once with a single space
            # except at the beginning of each line
            arg = re.sub(r"(?<=\S) +", " ", text, flags=re.MULTILINE)
        else:
            # boil down multiple spaces into one
            arg = re.sub(r"(?<!^) +", " ", text, flags=re.MULTILINE)
            # remove whatever remains as leading space in each line
            arg = re.sub(r"^[ \t]+", "", arg, flags=re.MULTILINE)


        title = shorten(arg)
        valid = True
    except:
        arg = ""
        title = "Remove redundant spaces but keep indentation"
        valid = False
    if json:
        uid = sys._getframe().f_code.co_name
        return alfred_json(title, sub, arg, valid, uid)
    else:
        return arg


def limit_newlines_to_sentences(text, json=False, remove_redunant_space=True):
    sub = "Insert newline after sentences, remove all others"
    try:
        arg = text.replace("\n", " ")
        for delim in [". ", ": ", "; "]:
            arg = arg.replace(f"{delim} ", f"{delim}\n")
        if remove_redunant_space:
            arg = remove_redundant_space(arg, keep_indent=False)
        title = shorten(arg)
        valid = True
    except:
        arg = ""
        title = "Newlines after .:; only"
        valid = False
    if json:
        uid = sys._getframe().f_code.co_name
        return alfred_json(title, sub, arg, valid, uid)
    else:
        return arg

def one_liner(text, json=False):
    sub = "Remove all newlines and redundant spaces"
    try:
        arg = text.replace("\n", " ")
        arg = remove_redundant_space(arg, keep_indent=False)
        title = shorten(arg)
        valid = True
    except:
        arg = ""
        title = "Clean one-liner, no redundant spaces"
        valid = False
    if json:
        uid = sys._getframe().f_code.co_name
        return alfred_json(title, sub, arg, valid, uid)
    else:
        return arg
