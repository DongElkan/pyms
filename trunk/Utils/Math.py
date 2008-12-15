"""
Provides mathematical functions
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

import copy, math

from pyms.Utils.Error import error
from pyms.Utils.Utils import is_list, is_number

def median(v):

    """
    @summary: Returns a median of a list or numpy array

    @param v: Input list or array
    @type v: ListType or numpy.core.ndarray
    @return: The median of the input list
    @rtype: FloatType

    @author: Vladimir Likic
    """

    if not is_list(v):
        error("argument neither list nor array")

    local_data = copy.deepcopy(v)
    local_data.sort()
    N = len(local_data)

    if (N % 2) == 0:
        # even number of points
        K = N/2 - 1 
        median = (local_data[K] + local_data[K+1])/2.0
    else:
	    # odd number of points
        K = (N - 1)/2 - 1
        median = local_data[K+1]

    return median

def vector_by_step(vstart,vstop,vstep):

    """
    @summary: generates a list by using start, stop, and step values

    @param vstart: Initial value 
    @type vstart: A number
    @param vstop: Max value
    @type vstop: A number
    @param vstep: Step
    @type vstep: A number
   
    @return: A list generated
    @rtype: ListType

    @author: Vladimir Likic
    """

    if not is_number(vstart) or not is_number(vstop) or not is_number(vstep):
        error("parameters start, stop, step must be numbers")

    v = []

    p = vstart 
    while p < vstop:
        v.append(p)
        p = p + vstep

    return v

def MAD(v):

    """
    @summary: median absolute deviation

    @param v: A list or array
    @type v: ListType, TupleType, or numpy.core.ndarray

    @return: median absolute deviation
    @rtype: FloatType

    @author: Vladimir Likic
    """

    if not is_list(v):
        error("argument neither list nor array")

    m = median(v)
    m_list = []

    for xi in v:
        d = math.fabs(xi - m)
        m_list.append(d)

    mad = median(m_list)/0.6745

    return mad


