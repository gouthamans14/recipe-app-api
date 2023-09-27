"""
Test custom Django management commands.

"""

from unittest.mock import patch  # to mock the behaiour of database

from psycopg2 import OperationalError as Psycopg2Error  #  Possibilities of error when we connect to datase before it connects

from django.core.management import call_command  #  helper function to simulate to call the command
from django.db.utils import OperationalError  # another exception thrown by the database
from django.test import SimpleTestCase  #  to test 

  #  we are providing the path of the wait_for_db method.
@patch("core.management.commands.wait_for_db.Command.check")#Mocking the behaviour of all the check so we are passing the entire test class there.
class CommandTests(SimpleTestCase):
    """
    Django command to wait for database.

    """

  #  patched_check is argument from decorator.

    def test_wait_for_db_read(self, patched_check):

        """
        Test waiting for database if database is ready.
        """
        patched_check.return_value =True  
        # When we call check, we want to return True value

        call_command("wait_for_db")

        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):  
        # the decorator argument will be the first argument

        """
        Test is waiting for database when getting Operational Error.
        """

        patched_check.side_effect = [Psycopg2Error] * 2 + \
              [OperationalError] * 3 + [True]

        call_command("wait_for_db")

        self.assertEqual(patched_check.call_count,6)

        patched_check.assert_called_with(databases=['default'])  
        # checks calling the default database
