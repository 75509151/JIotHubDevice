import pytest

class TestDevice:
    def test_upload_data(self, device):
        device.upload_data("test_upload_data")


