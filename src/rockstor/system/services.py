"""
Copyright (c) 2012-2013 RockStor, Inc. <http://rockstor.com>
This file is part of RockStor.

RockStor is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published
by the Free Software Foundation; either version 2 of the License,
or (at your option) any later version.

RockStor is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""


import re
import subprocess

from osi import run_command

SERVICE_BIN = '/sbin/service'

def init_service_op(service_name, command):
    service = None
    if (service_name == 'nfs'):
        service = 'nfs'
    elif (service_name == 'samba'):
        service = 'smb'
    elif (service_name == 'sftp'):
        service = 'sshd'
    else:
        raise Exception('unknown service: %s' % service_name)

    cmd = [SERVICE_BIN, service, command]
    out, err, rc = run_command(cmd)
    return out, err, rc
