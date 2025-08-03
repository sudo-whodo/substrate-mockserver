import os
# Set environment variables before importing testcontainers
os.environ["TESTCONTAINERS_RYUK_DISABLED"] = "true"
os.environ["TESTCONTAINERS_CHECKS_DISABLE"] = "true"

import pytest
import requests
import time
from pathlib import Path
from testcontainers.core.container import DockerContainer


class TestSubstrateMockserver:
    @pytest.fixture(scope="class")
    def mockserver_container(self):
        """Start MockServer container with the JSON expectations file."""
        # Get the path to the JSON file (relative to project root)
        json_file = Path(__file__).parent.parent.parent / "mocks" / "polkadot-full-mock.json"

        # Create and start the container with explicit configuration
        container = DockerContainer("mockserver/mockserver:latest") \
            .with_exposed_ports(1080) \
            .with_volume_mapping(str(json_file), "/mockserver/expectations.json") \
            .with_kwargs(platform="linux/amd64")

        # Start container with proper MockServer configuration
        container._container = container._docker.client.containers.run(
            container.image,
            detach=True,
            ports={1080: None},
            volumes={str(json_file): {"bind": "/mockserver/expectations.json", "mode": "ro"}},
            platform="linux/amd64",
            environment={
                "MOCKSERVER_INITIALIZATION_JSON_PATH": "/mockserver/expectations.json",
                "MOCKSERVER_LOG_LEVEL": "INFO"
            }
        )

        # Wait for the container to be ready and check if it's running
        time.sleep(10)
        container._container.reload()
        if container._container.status != "running":
            logs = container._container.logs().decode()
            raise RuntimeError(f"Container failed to start. Status: {container._container.status}. Logs: {logs}")

        # Additional wait for MockServer to initialize
        time.sleep(5)

        # Get the mapped port
        port_info = container._container.attrs['NetworkSettings']['Ports']['1080/tcp']
        if port_info and len(port_info) > 0:
            port = port_info[0]['HostPort']
        else:
            raise RuntimeError("Could not get mapped port for container")

        base_url = f"http://localhost:{port}"

        # Debug: Print container info
        print(f"Container started on port {port}")
        print(f"Base URL: {base_url}")

        # Load expectations via API
        try:
            with open(json_file, 'r') as f:
                expectations = f.read()

            # Load expectations via MockServer API
            expectations_response = requests.put(
                f"{base_url}/mockserver/expectation",
                data=expectations,
                headers={"Content-Type": "application/json"}
            )
            print(f"✅ Substrate RPC expectations loaded into MockServer ({expectations_response.status_code})")

            # Verify MockServer is working with a test RPC call
            test_payload = {
                "jsonrpc": "2.0",
                "method": "system_name",
                "params": [],
                "id": 1
            }
            test_response = requests.post(base_url, json=test_payload)
            print(f"✅ MockServer health check - system_name RPC call: {test_response.status_code}")
            if test_response.status_code == 200:
                result = test_response.json()
                print(f"✅ system_name response: '{result.get('result', 'N/A')}' (status: {test_response.status_code})")
            else:
                print(f"❌ Error response: {test_response.text}")
                raise RuntimeError(f"MockServer health check failed: {test_response.status_code}")

        except Exception as e:
            print(f"❌ Could not initialize MockServer: {e}")
            raise

        yield base_url

        # Cleanup
        try:
            container._container.stop()
            container._container.remove()
        except Exception as e:
            print(f"Warning: Error stopping container: {e}")

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
