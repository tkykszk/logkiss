"""Basic example of logkiss usage.

Copyright (c) 2025 Taka Suzuki
SPDX-License-Identifier: MIT
See LICENSE for details.
"""

import logkiss as logging

# Most basic example of logging
logging.warning('Watch out!')  # Will output message to console
logging.info('I told you so')  # Won't output due to default WARNING level
