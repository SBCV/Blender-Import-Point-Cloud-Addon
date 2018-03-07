'''
Copyright (C) 2018 Sebastian Bullinger


Created by Sebastian Bullinger

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import time

class StopWatch(object):

    def __init__(self):
        self.last_t = time.time()

    def reset_time(self):
        self.last_t = time.time()

    def get_elapsed_time(self):
        current_t = time.time()
        elapsed_t = current_t - self.last_t
        self.last_t = current_t
        return elapsed_t