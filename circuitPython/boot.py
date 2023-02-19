# SPDX-FileCopyrightText: 2017 Limor Fried for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""CircuitPython Essentials Storage logging boot.py file"""
import storage

# comment -> you can edit or delete temperature.txt
# uncomment -> you can write temperature.txt for logging purpose.
storage.remount("/", readonly=False)