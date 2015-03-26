import sys


# exit status values #
SUCCESS = 0
INVALID_ARGS = 1
FILE_NOT_FOUND = 2
# #### ###### ###### #

# printing functions #
def info(s, init_new_line=False):
    """
    """
    if s:
        nfo = '\n' if init_new_line else ''
        nfo += '[i] '
        sys.stdout.write(nfo + str(s) + '\n')
        sys.stdout.flush()


def error(s, init_new_line=False):
    """
    """
    if s:
        err = '\n' if init_new_line else ''
        err += '[e] '
        sys.stderr.write(err + str(s) + '\n')
        sys.stderr.flush()
# ######## ######### #
