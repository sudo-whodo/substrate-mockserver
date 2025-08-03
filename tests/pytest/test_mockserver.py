import pytest
import requests
import time
from pathlib import Path
from testcontainers.generic import GenericContainer


class TestSubstrateMockserver:
    @pytest.fixture(scope="class")
    def mockserver_container(self):
        """Start MockServer container with the JSON expectations file."""
        # Get the path to the JSON file (relative to project root)
        json_file = Path(__file__).parent.parent.parent / "mocks" / "polkadot-full-mock.json"

        # Create and start the container
        container = GenericContainer("mockserver/mockserver:latest") \
            .with_exposed_ports(1080) \
            .with_volume_mapping(str(json_file), "/mockserver/expectations.json")

        container.start()

        # Wait for the container to be ready
        time.sleep(5)

        # Get the mapped port
        port = container.get_exposed_port(1080)
        base_url = f"http://localhost:{port}"

        yield base_url

        # Cleanup
        container.stop()

    def test_system_name_rpc(self, mockserver_container):
        """Test the system_name RPC method."""
        payload = {
            "jsonrpc": "2.0",
            "method": "system_name",
            "params": [],
            "id": 1
        }

        response = requests.post(mockserver_container, json=payload)
        assert response.status_code == 200

        data = response.json()
        assert data["jsonrpc"] == "2.0"
        assert data["result"] == "mockClient"
        assert data["id"] == 1
