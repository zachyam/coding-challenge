import unittest
from unittest.mock import Mock
from lightstep import Solution

class TestSum(unittest.TestCase):
    def setUp(self):
        self.json = Mock()
        self.data = Solution(self.json)

    def test_unique_error_highest_count(self):
        unique_error_count_test_data = unque_error_count_test_data = [{
                        "service": "loadbalancer",
                        "level": "INFO",
                        "timestamp": "2017-10-17 00:00:00.000000",
                        "operation": "POST",
                        "message": "START /login requested",
                        "transaction_id": "1"
                        },
                        {
                        "service": "webserver",
                        "level": "DEBUG",
                        "timestamp": "2017-10-17 00:00:00.207697",
                        "operation": "/login",
                        "message": "START Logging in user",
                        "transaction_id": "1"
                        },
                        {
                        "service": "authentication_service",
                        "level": "ERROR",
                        "timestamp": "2017-10-17 00:00:01.038673",
                        "operation": "AuthenticateUser",
                        "message": "START Authenticating user",
                        "transaction_id": "1"
                        },
                        {
                        "service": "webserver",
                        "level": "ERROR",
                        "timestamp": "2017-10-17 00:00:01.207697",
                        "operation": "AuthenticateUser",
                        "message": "END Authenticating user",
                        "transaction_id": "1"
                        }]
        data = Solution(unique_error_count_test_data)
        self.assertEqual(data.get_operation_with_highest_error_count(), ('AuthenticateUser', 2))

    def test_non_unique_error_highest_count(self):
        non_unique_error_count_test_data = [{
                        "service": "loadbalancer",
                        "level": "ERROR",
                        "timestamp": "2017-10-17 00:00:00.000000",
                        "operation": "/login",
                        "message": "START /login requested",
                        "transaction_id": "1"
                        },
                        {
                        "service": "webserver",
                        "level": "ERROR",
                        "timestamp": "2017-10-17 00:00:00.207697",
                        "operation": "/login",
                        "message": "START Logging in user",
                        "transaction_id": "1"
                        },
                        {
                        "service": "authentication_service",
                        "level": "ERROR",
                        "timestamp": "2017-10-17 00:00:01.038673",
                        "operation": "AuthenticateUser",
                        "message": "START Authenticating user",
                        "transaction_id": "1"
                        },
                        {
                        "service": "webserver",
                        "level": "ERROR",
                        "timestamp": "2017-10-17 00:00:01.207697",
                        "operation": "AuthenticateUser",
                        "message": "END Authenticating user",
                        "transaction_id": "1"
                        }]
        data = Solution(non_unique_error_count_test_data)
        self.assertEqual(data.get_operation_with_highest_error_count(), ('/login', 2))

    def test_longest_transaction_time(self):
        transaction_time_test_data = [{
                        "service": "loadbalancer",
                        "level": "ERROR",
                        "timestamp": "2017-10-17 00:00:02.000000",
                        "operation": "/login",
                        "message": "START /login requested",
                        "transaction_id": "1"
                        },
                        {
                        "service": "webserver",
                        "level": "INFO",
                        "timestamp": "2017-10-17 00:00:01.000000",
                        "operation": "/login",
                        "message": "START Logging in user",
                        "transaction_id": "1"
                        },
                        {
                        "service": "authentication_service",
                        "level": "ERROR",
                        "timestamp": "2017-10-17 00:00:03.000000",
                        "operation": "AuthenticateUser",
                        "message": "END Authenticating user",
                        "transaction_id": "1"
                        },
                        {
                        "service": "webserver",
                        "level": "ERROR",
                        "timestamp": "2017-10-17 00:00:01.000000",
                        "operation": "AuthenticateUser",
                        "message": "START Authenticating user",
                        "transaction_id": "2"
                        },
                        {
                        "service": "authentication_service",
                        "level": "INFO",
                        "timestamp": "2017-10-17 00:00:02.000000",
                        "operation": "AuthenticateUser",
                        "message": "END Authenticating user",
                        "transaction_id": "2"
                        }]
        data = Solution(transaction_time_test_data)
        self.assertEqual(data.get_longest_transaction_process(), ('1', 2.0))

    def test_parseTimestamp(self):
        self.assertEqual(self.data.parse_timestamp('2017-10-17 00:00:01.038673'), 1508223601.038673)
        self.assertNotEqual(self.data.parse_timestamp('2017-10-17 00:00:01.038673'), 1508223601)


if __name__ == '__main__':
    unittest.main()
