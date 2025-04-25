"""Test cases for logkiss core functionality.

Copyright (c) 2025 Taka Suzuki
SPDX-License-Identifier: MIT
See LICENSE for details.
"""

import unittest
from logkiss import getLogger


class TestKissLog(unittest.TestCase):
    def setUp(self):
        self.logger_name = "test_logger"

    def test_logger_initialization(self):
        log = getLogger(self.logger_name)
        self.assertIsNotNone(log)
        self.assertEqual(log.name, self.logger_name)


if __name__ == "__main__":
    unittest.main()
