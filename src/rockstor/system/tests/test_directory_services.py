"""
Copyright (c) 2012-2021 RockStor, Inc. <http://rockstor.com>
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
import unittest
from mock import patch

from system.exceptions import CommandException
from system.directory_services import domain_workgroup


class SystemDirectoryServicesTests(unittest.TestCase):
    """
    The tests in this suite can be run via the following command:
    cd <root dir of rockstor ie /opt/rockstor>
    ./bin/test --settings=test-settings -v 3 -p test_directory_services*
    """

    def setUp(self):
        self.patch_run_command = patch("system.directory_services.run_command")
        self.mock_run_command = self.patch_run_command.start()

    def tearDown(self):
        patch.stopall()

    def test_domain_workgroup(self):
        """
        This tests for the correct return of WORKGROUP from the AD server
        as fetched by NET
        """
        domain = "samdom.example.com"
        o = ["Workgroup: SAMDOM", ""]
        e = [""]
        r = 0
        self.mock_run_command.return_value = (o, e, r)
        expected = "SAMDOM"

        returned = domain_workgroup(domain)
        self.assertEqual(
            returned,
            expected,
            msg="Un-expected domain_workgroup() result:\n "
            "returned = ({}).\n "
            "expected = ({}).".format(returned, expected),
        )

    def test_domain_workgroup_invalid(self):
        """
        Test domain_workgroup() if AD domain can't be reached.
        It should raise a CommandException.
        """
        domain = "bogusad.bogusdomain.com"
        self.mock_run_command.side_effect = CommandException(
            err=["Didn't find the cldap server!", ""],
            cmd=["/usr/bin/net", "ads", "workgroup", "-S", domain],
            out=[""],
            rc=255,
        )
        with self.assertRaises(CommandException):
            domain_workgroup(domain)

    def test_domain_workgroup_missing(self):
        """
        Test domain_workgroup() if AD domain can be reached but does
        not return the Workgroup information.
        It should raise an Exception
        """
        domain = "samdom.example.com"
        o = [""]
        e = [""]
        r = 0
        self.mock_run_command.return_value = (o, e, r)

        with self.assertRaises(Exception):
            domain_workgroup(domain)
