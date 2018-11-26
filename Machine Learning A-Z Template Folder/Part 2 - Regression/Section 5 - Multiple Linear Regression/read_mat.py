#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 14:36:46 2018

@author: xueqianlong
"""

import scipy.io
mat = scipy.io.loadmat('Sample 1.mat')
X = mat['input']
y = mat['target']