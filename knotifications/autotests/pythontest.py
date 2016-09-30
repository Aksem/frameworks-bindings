#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import print_function

import sys

sys.path.append(sys.argv[1])

from PyQt5 import QtCore
from PyQt5 import QtWidgets

from PyKF5 import KNotifications

def main():
    app = QtWidgets.QApplication(sys.argv)


if __name__ == '__main__':
    sys.exit(main())
