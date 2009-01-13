#
# partition.py
# Python bindings for libparted (built on top of the _ped Python module).
#
# Copyright (C) 2009 Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.  Any Red Hat trademarks that are incorporated in the
# source code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission of
# Red Hat, Inc.
#
# Red Hat Author(s): Chris Lumens <clumens@redhat.com>
#

import _ped

class Partition(object):
    def __init__(self, disk, type, fs, geom):
        self._disk = disk
        self._fileSystem = fs
        self._geometry = geom

        self.__partition = _ped.Partition(disk, type, fs.type, geom.start, geom.end)

    def _readOnly(self, prop):
        raise parted.ReadOnlyProperty, "%s is a read-only property"

    active = property(lambda s: s.__partition.is_active(), lambda s, v: s._readOnly("active"))
    busy = property(lambda s: s.__partition.is_busy(), lambda s, v: s._readOnly("busy"))
    disk = property(lambda s: s._disk, lambda s, v: s._readOnly("disk"))
    filesystem = property(lambda s: s._fileSystem, lambda s, v: setattr(s, "_fileSystem", v))
    geometry = property(lambda s: s._geometry, lambda s, v: setattr(s, "_geometry", v))
    number = property(lambda s: s.__partition.num, lambda s, v: setattr(s.__partition, "num", v))
    path = property(lambda s: s.__partition.get_path(), lambda s, v: s._readOnly("path"))
    system = property(, lambda s, v: s.__partition.set_system(v))
    type = property(lambda s: s.__partition.type, lambda s, v: setattr(s.__partition, "type", v))

    def getFlag(self, flag):
        """Get the value of a particular flag on the partition.  Valid flags
           are the _ped.PARTITION_* constants.  See _ped.flag_get_name() and
           _ped.flag_get_by_name() for more help working with partition flags.
        """
        return self.__partition.get_flag(flag)

    def getMaxGeometry(self, constraint):
        """Given a constraint, return the maximum Geometry that self can be
           grown to.  Raises Partitionexception on error."""
        return self.disk.get_max_partition_geometry(self.__partition, constraint)

    def setFlag(self, flag, value):
        """Set the flag on a partition to the provided value.  On error, a
           PartitionException will be raised.  See getFlag() for more help on
           working with partition flags."""
        return self.__partition.set_flag(flag, value)