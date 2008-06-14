"""
General I/O functions
"""

 #############################################################################
 #                                                                           #
 #    PyMS software for processing of metabolomic mass-spectrometry data     #
 #    Copyright (C) 2005-8 Vladimir Likic                                    #
 #                                                                           #
 #    This program is free software; you can redistribute it and/or modify   #
 #    it under the terms of the GNU General Public License version 2 as      #
 #    published by the Free Software Foundation.                             #
 #                                                                           #
 #    This program is distributed in the hope that it will be useful,        #
 #    but WITHOUT ANY WARRANTY; without even the implied warranty of         #
 #    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
 #    GNU General Public License for more details.                           #
 #                                                                           #
 #    You should have received a copy of the GNU General Public License      #
 #    along with this program; if not, write to the Free Software            #
 #    Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.              #
 #                                                                           #
 #############################################################################

import types, os, string

from Error import error
from Utils import is_number, is_str, is_list

def open_for_reading(file_name):

    """
    Opens file for reading, returns file pointer

    @param file_name: Name of the file to be opened for reading
    @type file_name: StringType
    @return: Pointer to the opened file
    @rtype: FileType
    @author: Vladimir Likic
    """

    if not is_str(file_name):
        error("'file_name' is not a string")
    try:
        fp = open(file_name)
    except IOError:
        error("'%s' does not exist" % (file_name))

    return fp

def open_for_writing(file_name):

    """
    Opens file for writing, returns file pointer

    @param file_name: Name of the file to be opened for writing
    @type file_name: StringType
    @return: Pointer to the opened file
    @rtype: FileType
    @author: Vladimir Likic
    """

    if not is_str(file_name):
        error("'file_name' is not a string")
    try:
        fp = open(file_name, "w")
    except IOError:
        error("Cannot open '%s' for writing" % (file_name))
    return fp

def close_for_reading(fp):

    """
    Closes file pointer open for reading

    @param fp: A file pointer, previously opened for reading
    @type fp: FileType
    @return: none
    @rtype: NoneType
    @author: Vladimir Likic
    """

    fp.close()

def close_for_writing(fp):

    """
    Closes file pointer open for writing

    @param fp: A file pointer, previously opened for writing
    @type fp: FileType
    @return: none
    @rtype: NoneType
    @author: Vladimir Likic
    """

    fp.close()

def file_lines(file_name):

    """
    Returns lines from a file, as a list

    @param file_name: Name of a file
    @type: StringType
    @return: A list of lines
    @rtype: ListType
    @author: Vladimir Likic
    """

    if not is_str(file_name):
        error("'file_name' is not a string")

    fp = open_for_reading(file_name)
    file_lines = fp.readlines()
    close_for_reading(fp)

    return file_lines

def save_data(file_name, data, format_str="%.6f", prepend="", sep=" ",
	compressed=False):

    """
    Saves a list of numbers or a list of lists of numbers to a file
    with specific formatting.

    @param file_name: Name of a file
    @type: StringType
    @param data: A list of numbers, or a list of lists
    @type: ListType
    @param format_str: A format string for individual entries
    @type: StringType
    @param prepend: A string, printed before each row
    @type: StringType
    @param sep: A string, printed after each number
    @type: StringType
    @param compressed: A boolean. If True, the output will be gzipped
    @type: BooleanType
    @return: none
    @rtype: NoneType
    @author: Vladimir Likic
    """

    if not is_str(file_name):
        error("'file_name' is not a string")

    if not is_list(data):
        error("'data' is not a list")

    if not is_str(prepend):
        error("'prepend' is not a string")

    if not is_str(sep):
        error("'sep' is not a string")

    fp = open_for_writing(file_name)

    # decide whether data is a vector or matrix
    if is_number(data[0]):
        for item in data:
            if not is_number(item):
                error("not all elements of the list are numbers")
        data_is_matrix = 0
    else:
        for item in data:
            if not is_list(item):
                error("not all elements of the list are lists")
        data_is_matrix = 1

    if data_is_matrix:
        for ii in range(len(data)):
            fp.write(prepend)
            for jj in range(len(data[ii])):
                if is_number(data[ii][jj]):
                    fp.write(format_str % (data[ii][jj]))
                    if (jj<(len(data[ii])-1)): fp.write(sep)
                else:
                    error("datum not a number")
            fp.write("\n")
    else:
        for ii in range(len(data)):
            fp.write(prepend)
            fp.write(format_str % (data[ii]))
            fp.write("\n")

    close_for_writing(fp)

    if compressed:
        status = os.system('gzip %s' % (file_name))
        if status != 0:
            error("gzip compress failed")

