# Licensed to the StackStorm, Inc ('StackStorm') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import socket
import operator


def status_code_to_text(status):
    """
    Takes an Solarwinds Orion status code and translates it to
    human text and also a colour that can be used in Slack.
    """

    if status == 0:
        return ("Unknown", None)  # aka slack 'grey'
    elif status == 1:
        return ("Up", "#00ad52")  # aka slack 'good'
    elif status == 2:
        return ("Down", "#eb0000")  # aka slack 'danger'
    elif status == 3:
        return ("Warning", "#e89e0e")  # aka slack 'warning'
    elif status == 14:
        return ("Critical", "#eb0000")  # aka slack 'danger'


def send_user_error(message):
    """
    Prints an user error message.
    """
    print(message)


def discovery_status_to_text(status):
    """
    Convert a Discovery Status code into meaningful text.

    Args:
       status: Staus code from Orion.

    Returns:
       String: Human text for status code.
    """
    discovery_statuses = {"0": 'Unknown',
                          "1": 'InProgress',
                          "2": 'Finished',
                          "3": 'Error',
                          "4": "NotScheduled",
                          "5": "Scheduled",
                          "6": "NotCompleted",
                          "7": "Canceling",
                          "8": "ReadyForImport"}
    return discovery_statuses[status]


def is_ip(ip_address):
    """
    Check if an valid IP address using socket.inet_pton.

    Args:
       ip_address: a string to check

    Returns:
       bool: True if an IP address, False if not.
    """
    if "." in ip_address:
        family = socket.AF_INET
    elif ":" in ip_address:
        family = socket.AF_INET6
    else:
        return False

    try:
        socket.inet_pton(family, ip_address)
    except socket.error:
        return False
    else:
        return True


def only_one(*args):
    """
    Only return True, if only one arg is evaluates to True.
    """

    bools = [bool(v) for v in args]
    if all(bools):
        return False

    return reduce(operator.xor, bools, False)
