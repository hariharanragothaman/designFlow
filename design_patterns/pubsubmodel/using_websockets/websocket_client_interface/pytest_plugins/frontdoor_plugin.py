"""
:Organization:  BOSE CORPORATION

:Copyright:  COPYRIGHT 2018 BOSE CORPORATION ALL RIGHTS RESERVED.
             This program may not be reproduced, in whole or in part in any
             form or any means whatsoever without the written permission of:
                 BOSE CORPORATION
                 The Mountain,
                 Framingham, MA 01701-9168


This module can be used as a pytest plugin.
This contains the fixtures to create FrontDoor and FrontDoor utils object
"""

import pytest
from CastleTestUtils.FrontDoorAPI.FrontDoorAPI import FrontDoorAPI
from CastleTestUtils.FrontDoorAPI.FrontDoorHelper import FrontDoorUtilities


@pytest.fixture(scope="session")
def frontdoor(device_ip, oauth_info):
    """
    Get FrontDoorAPI instance.
    1. Fixture to get device_ip, install the RivieraUtil/pytest_plugin/product_plugin
    2. oauth_info fixture - OAuthUtils/pytest_plugin/oauth_plugin
    """
    front_door = FrontDoorAPI(device_ip, access_token=oauth_info['access_token'])

    yield front_door
    if front_door:
        front_door.close()


@pytest.fixture(scope="session")
def frontdoor_utils(frontdoor):
    """
    Fixture to get frontdoor_utils
    """
    return FrontDoorUtilities(frontdoor)
