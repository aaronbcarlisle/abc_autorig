#------------------------------------------------------------------------------#
#-------------------------------------------------------------------- HEADER --#

"""
:author:
    acarlisle

:description:
    json utility functions.
"""
#------------------------------------------------------------------------------#
#------------------------------------------------------------------- IMPORTS --#

# built-in
import json
import maya.cmds as cmds

#------------------------------------------------------------------------------#
#----------------------------------------------------------------- FUNCTIONS --#

def json(data=None, path=None):
    """Saves out given data into a json file."""
    # batch hack
    try:
        if not path:
            path = cmds.fileDialog2(fm=0, ds=2, ff="*.json", rf=True)
            if not path:
                return
            path = path[0]
    except:
        pass

    data = json.dumps(data, sort_keys=True, ensure_ascii=True, indent=2)
    fobj = open(path, 'wb')
    fobj.write(data)
    fobj.close()

    return path

def load(path=None):
    """This procedure loads and returns the content of a json file."""
    # batch hack
    try:
        if not path:
            path = cmds.fileDialog2(fm=1, ds=2, ff="*.json")
            if not path:
                return
            path = path[0]
    except:
        pass

    fobj = open(path, "rb")
    data = json.load(fobj)
    return data
