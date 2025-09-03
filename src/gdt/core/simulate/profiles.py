# CONTAINS TECHNICAL DATA/COMPUTER SOFTWARE DELIVERED TO THE U.S. GOVERNMENT WITH UNLIMITED RIGHTS
#
# Contract No.: CA 80MSFC17M0022
# Contractor Name: Universities Space Research Association
# Contractor Address: 7178 Columbia Gateway Drive, Columbia, MD 21046
#
# Copyright 2017-2022 by Universities Space Research Association (USRA). All rights reserved.
#
# Developed by: William Cleveland and Adam Goldstein
#               Universities Space Research Association
#               Science and Technology Institute
#               https://sti.usra.edu
#
# Developed by: Daniel Kocevski
#               National Aeronautics and Space Administration (NASA)
#               Marshall Space Flight Center
#               Astrophysics Branch (ST-12)
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
# in compliance with the License. You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied. See the License for the specific language governing permissions and limitations under the
# License.
#
import numpy as np
from .generators import *

__all__ = ['norris', 'tophat', 'gaussian', 'triangular', 'constant', 'linear', 'quadratic']

# pulse shapes
def tophat(x, amp, tstart, tstop):
    """A tophat (rectangular) pulse function.
    
    Args:
        x (np.array): Array of times
        amp (float): The tophat amplitude
        tstart (float): The start time of the tophat
        tstop (float): The end time of the tophat
    
    Returns:
        (np.array)
    """
    mask = (x >= tstart) & (x <= tstop)
    fxn = np.zeros_like(x)
    fxn[mask] = amp
    return fxn


def norris(x, amp, tstart, t_rise, t_decay):
    r"""A Norris pulse-shape function:

    :math:`I(t) = A \lambda e^{-\tau_1/t - t/\tau_2} \text{ for } t > 0;\\ 
    \text{ where } \lambda = e^{2\sqrt(\tau_1/\tau_2)};`
    
    and where
    
    * :math:`A` is the pulse amplitude
    * :math:`\tau_1` is the rise time
    * :math:`\tau_2` is the decay time
    
    References:
        `Norris, J. P., et al. 2005 ApJ 627 324
        <https://iopscience.iop.org/article/10.1086/430294>`_
    
    Args:
        x (np.array): Array of times
        amp (float): The amplitude of the pulse
        tstart (float): The start time of the pulse
        t_rise (float): The rise timescal of the pulse
        t_decay (flaot): The decay timescale of the pulse
    
    Returns:
        (np.array)
    """
    x = np.asarray(x)
    fxn = np.zeros_like(x)
    mask = (x > tstart)
    lam = amp * np.exp(2.0 * np.sqrt(t_rise / t_decay))
    fxn[mask] = lam * np.exp(
        -t_rise / (x[mask] - tstart) - (x[mask] - tstart) / t_decay)
    return fxn

def gaussian(x, amp, center, sigma):
    r"""A Gaussian (normal) profile.
    
    The functional form is:
    
    :math:`f(x) = A e^{-\frac{(x - \mu)^2}{2\sigma^2}}`
    
    where:
    
    * :math:`A` is the pulse amplitude
    * :math:`\mu` is the center of the peak
    * :math:`\sigma` is the standard deviation (width)
    
    Args:
        x (np.array): Array of times.
        amp (float): The amplitude of the pulse, A.
        center (float): The center time of the pulse, :math:`\mu`.
        sigma (float): The standard deviation of the pulse, :math:`\sigma`.
    
    Returns:
        (np.array)
    """
    return amp * np.exp(-((x - center)**2) / (2 * sigma**2))


def triangular(x, amp, tstart, tpeak, tstop):
    r"""A triangular pulse function.
    
    The functional form is a piecewise linear function:
    
    :math:`f(x) = \begin{cases} 
    A \frac{x - t_{start}}{t_{peak} - t_{start}} & t_{start} \le x < t_{peak} \\ 
    A \frac{t_{stop} - x}{t_{stop} - t_{peak}} & t_{peak} \le x \le t_{stop} \\ 
    0 & \text{otherwise} 
    \end{cases}`
    
    where:
    
    * :math:`A` is the pulse amplitude
    * :math:`t_{start}` is the start time of the pulse
    * :math:`t_{peak}` is the time of the peak amplitude
    * :math:`t_{stop}` is the end time of the pulse
    
    Args:
        x (np.array): Array of times.
        amp (float): The amplitude of the peak, A.
        tstart (float): The start time of the pulse.
        tpeak (float): The time of the peak.
        tstop (float): The end time of the pulse.
        
    Returns:
        (np.array)
    """
    return np.interp(x, [tstart, tpeak, tstop], [0, amp, 0])

# ------------------------------------------------------------------------------

# background profiles
def constant(x, amp):
    """A constant background function.
    
    Args:
        x (np.array): Array of times
        amp (float): The background amplitude
    
    Returns:
        (np.array)
    """
    fxn = np.empty(x.size)
    fxn.fill(amp)
    return fxn


def linear(x, c0, c1):
    """A linear background function.
    
    Args:
        x (np.array): Array of times
        c0 (float): The constant coefficient
        c1 (float): The linear coefficient
    
    Returns:
        (np.array)
    """
    fxn = c0 + c1 * x
    return fxn


def quadratic(x, c0, c1, c2):
    """A quadratic background function.
    
    Args:
        x (np.array): Array of times
        c0 (float): The constant coefficient
        c1 (float): The linear coefficient
        c2 (float): The quadratic coefficient
    
    Returns:
        (np.array)
    """
    fxn = linear(x, c0, c1) + c2 * x ** 2
    return fxn
