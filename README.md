# Substrate Mockserver

A lightweight mockserver implementation for testing Substrate RPC services. This provides a quick way to simulate basic Substrate node functionality for testing infrastructure-as-code (IaC) deployments and service integrations without requiring a full Substrate node.

## Overview

This mockserver responds to common Substrate RPC calls with predefined mock responses, making it ideal for:

- Testing deployment pipelines
- Infrastructure validation
- Service integration testing
- Development environments where a full node is not required

## Supported RPC Methods

The mockserver currently supports the following Substrate RPC methods:

| Method | Category | Description | Mock Response |
|--------|----------|-------------|---------------|
| `chain_getBlock` | Chain | Returns a mock block structure | `{"jsonrpc":"2.0","result":{"block":{"header":{"parentHash":"0x0000000000000000000000000000000000000000000000000000000000000000","number":"0x01","stateRoot":"0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef","extrinsicsRoot":"0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890"},"extrinsics":[]}},"id":1}` |
| `chain_getBlockHash` | Chain | Returns a mock block hash | `{"jsonrpc":"2.0","result":"0x1234000000000000000000000000000000000000000000000000000000000000","id":1}` |
| `chain_getFinalizedHead` | Chain | Returns a mock finalized head hash | `{"jsonrpc":"2.0","result":"0xabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdef","id":1}` |
| `chain_getHeader` | Chain | Returns a mock block header | `{"jsonrpc":"2.0","result":{"parentHash":"0x0000000000000000000000000000000000000000000000000000000000000000","number":"0x01","stateRoot":"0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef","extrinsicsRoot":"0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890"},"id":1}` |
| `state_getKeys` | State | Returns empty key list | `{"jsonrpc":"2.0","result":[],"id":1}` |
| `state_getKeysPaged` | State | Returns empty paginated key list | `{"jsonrpc":"2.0","result":[],"id":1}` |
| `state_getMetadata` | State | Returns mock metadata | `{"jsonrpc":"2.0","result":"0x6d65746164617461...","id":1}` |
| `state_getRuntimeVersion` | State | Returns mock runtime version | `{"jsonrpc":"2.0","result":{"specVersion":1010,"transactionVersion":6},"id":1}` |
| `state_getStorage` | State | Returns mock storage value | `{"jsonrpc":"2.0","result":"0x010203","id":1}` |
| `system_chain` | System | Returns mock chain name | `{"jsonrpc":"2.0","result":"mockChain","id":1}` |
| `system_health` | System | Returns mock health status | `{"jsonrpc":"2.0","result":{"peers":5,"isSyncing":false,"shouldHavePeers":true},"id":1}` |
| `system_name` | System | Returns mock client name | `{"jsonrpc":"2.0","result":"mockClient","id":1}` |
| `system_properties` | System | Returns mock chain properties | `{"jsonrpc":"2.0","result":{"ss58Format":42},"id":1}` |
| `system_upgradedToTripleRefCount` | System | Returns upgrade status | `{"jsonrpc":"2.0","result":true,"id":1}` |
| `system_version` | System | Returns mock version | `{"jsonrpc":"2.0","result":"9.8.7","id":1}` |
| `dev_echo` | Development | Echo method for testing | `{"jsonrpc":"2.0","result":["echoed_param"],"id":1}` |
| `rpc_methods` | RPC | Lists all available RPC methods | `{"jsonrpc":"2.0","result":{"methods":["chain_getBlock","chain_getBlockHash","chain_getHeader","system_chain","system_name","system_version"],"version":"1.0.0"},"id":1}` |

### Method Categories

#### Chain Methods
Methods for interacting with blockchain data and block information.

#### State Methods
Methods for querying blockchain state, storage, and runtime information.

#### System Methods
Methods for retrieving system information about the node and network.

#### Development Methods
Utility methods for testing and development purposes.

## Quick Start

### Using Docker

#### Static Mock Responses
```bash
# Pull and run MockServer with static mock responses
docker run -d \
  --name substrate-mockserver \
  -p 9933:1080 \
  -v $(pwd)/mocks/polkadot-static-responses.json:/mockserver/expectations.json \
  mockserver/mockserver:latest
```

#### Live Proxy to Polkadot Network
```bash
# Pull and run MockServer as a proxy to live Polkadot RPC
docker run -d \
  --name substrate-proxy \
  -p 9933:1080 \
  -v $(pwd)/mocks/polkadot-proxy-forwarding.json:/mockserver/expectations.json \
  mockserver/mockserver:latest
```

#### For Mac ARM Users
```bash
# Static mocks - Use platform flag for ARM-based Macs
docker run -d \
  --platform linux/amd64 \
  --name substrate-mockserver \
  -p 9933:1080 \
  -v $(pwd)/mocks/polkadot-static-responses.json:/mockserver/expectations.json \
  mockserver/mockserver:latest

# Live proxy - Use platform flag for ARM-based Macs
docker run -d \
  --platform linux/amd64 \
  --name substrate-proxy \
  -p 9933:1080 \
  -v $(pwd)/mocks/polkadot-proxy-forwarding.json:/mockserver/expectations.json \
  mockserver/mockserver:latest
```

### Using Podman

#### Static Mock Responses
```bash
# Pull and run MockServer with static mock responses
podman run -d \
  --name substrate-mockserver \
  -p 9933:1080 \
  -v $(pwd)/mocks/polkadot-static-responses.json:/mockserver/expectations.json \
  docker.io/mockserver/mockserver:latest
```

#### Live Proxy to Polkadot Network
```bash
# Pull and run MockServer as a proxy to live Polkadot RPC
podman run -d \
  --name substrate-proxy \
  -p 9933:1080 \
  -v $(pwd)/mocks/polkadot-proxy-forwarding.json:/mockserver/expectations.json \
  docker.io/mockserver/mockserver:latest
```

#### For Mac ARM Users
```bash
# Static mocks - Use platform flag for ARM-based Macs with Podman
podman run -d \
  --platform linux/amd64 \
  --name substrate-mockserver \
  -p 9933:1080 \
  -v $(pwd)/mocks/polkadot-static-responses.json:/mockserver/expectations.json \
  docker.io/mockserver/mockserver:latest

# Live proxy - Use platform flag for ARM-based Macs with Podman
podman run -d \
  --platform linux/amd64 \
  --name substrate-proxy \
  -p 9933:1080 \
  -v $(pwd)/mocks/polkadot-proxy-forwarding.json:/mockserver/expectations.json \
  docker.io/mockserver/mockserver:latest
```

## Testing the Mockserver

Once the container is running, you can test the mockserver by sending RPC requests:

```bash
# Test system_name method
curl -X POST http://localhost:9933 \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "system_name",
    "params": [],
    "id": 1
  }'

# Expected response:
# {"jsonrpc":"2.0","result":"mockClient","id":1}
```

```bash
# Test chain_getBlock method
curl -X POST http://localhost:9933 \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "chain_getBlock",
    "params": [],
    "id": 1
  }'
```

## Configuration

This repository includes two types of mock configurations:

### 1. Static Mock Responses (`mocks/polkadot-static-responses.json`)
Contains predefined mock responses for common Substrate RPC methods. This file defines:
- HTTP request patterns to match
- Corresponding HTTP responses to return
- Headers and status codes

### 2. Live Proxy Configuration (`mocks/polkadot-proxy-forwarding.json`)
Forwards all requests to a live Polkadot RPC endpoint at `rpc.ibp.network/polkadot`. This configuration:
- Proxies all JSON-RPC POST requests to the live endpoint
- Forwards GET requests for health checks or other endpoints
- Uses HTTPS on port 443 for secure communication

### Customizing Responses

To modify the mock responses:

1. Edit the `mocks/polkadot-full-mock.json` file
2. Restart the container to load the new configuration

Example expectation structure:
```json
{
  "httpRequest": {
    "method": "POST",
    "path": "/",
    "body": { "json": { "method": "system_name" } }
  },
  "httpResponse": {
    "statusCode": 200,
    "body": "{\"jsonrpc\":\"2.0\",\"result\":\"mockClient\",\"id\":1}",
    "headers": [{ "name": "Content-Type", "values": ["application/json"] }]
  }
}
```

## Environment Variables

You can customize the MockServer behavior using environment variables:

```bash
# Set log level
docker run -d \
  --name substrate-mockserver \
  -p 9933:1080 \
  -e MOCKSERVER_LOG_LEVEL=INFO \
  -v $(pwd)/mocks/polkadot-full-mock.json:/mockserver/expectations.json \
  mockserver/mockserver:latest
```

Common environment variables:
- `MOCKSERVER_LOG_LEVEL` - Set logging level (TRACE, DEBUG, INFO, WARN, ERROR)
- `MOCKSERVER_PORT` - Change the port (default: 1080)

## Docker Compose

For easier management, you can use Docker Compose:

```yaml
# docker-compose.yml
version: '3.8'
services:
  substrate-mockserver:
    image: mockserver/mockserver:latest
    platform: linux/amd64  # For ARM Macs
    ports:
      - "9933:1080"
    volumes:
      - ./mocks/polkadot-full-mock.json:/mockserver/expectations.json
    environment:
      - MOCKSERVER_LOG_LEVEL=INFO
```

Run with:
```bash
docker-compose up -d
```

## Use Cases

### Infrastructure Testing
Use this mockserver to test your infrastructure deployments without requiring a full Substrate node:

```bash
# Test your service connectivity
curl -X POST http://your-load-balancer:9933 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"system_health","params":[],"id":1}'
```

### CI/CD Pipeline Testing
This repository includes automated testing via GitHub Actions with separate workflows:

**Static Response Testing (`.github/workflows/test-static-responses.yml`):**
- Runs on every PR and push
- Tests static mock responses quickly and reliably
- No network dependencies

**Proxy Forwarding Testing (`.github/workflows/test-proxy-forwarding.yml`):**
- Runs on PR/push and daily schedule
- Tests live network connectivity
- May fail due to network issues

**Example integration in your own projects:**
```yaml
# Example GitHub Actions step
- name: Start Substrate Mockserver
  run: |
    docker run -d \
      --name substrate-mockserver \
      -p 9933:1080 \
      -v ${{ github.workspace }}/mocks/polkadot-static-responses.json:/mockserver/expectations.json \
      mockserver/mockserver:latest
```

## Development

### Local Testing with Act + Podman

You can test the GitHub Actions workflows locally using `act` with Podman:

```bash
# Install act (if not already installed)
brew install act  # on macOS

# Start podman
podman machine start  # if using podman machine

# Run the test script
./test-local.sh
```

**Manual Testing:**
```bash
# Test JSON lint workflow only
act -j lint --workflows .github/workflows/jsonlint.yml

# Test MockServer workflow only (with proper architecture)
act -j test-mockserver --workflows .github/workflows/test-mockserver.yml \
    --container-architecture linux/amd64
```

**Environment Variables for Podman:**
- `DOCKER_HOST` - Points to podman socket (auto-detected on macOS)
- `TESTCONTAINERS_RYUK_DISABLED=true` - Disables cleanup container
- `TESTCONTAINERS_CHECKS_DISABLE=true` - Disables environment checks

**Troubleshooting Act + Podman:**
- On macOS: Ensure `podman machine start` has been run
- Use `--container-architecture linux/amd64` flag for ARM Macs
- If socket issues persist, try running act without custom DOCKER_HOST

### JSON Validation
This repository includes automated JSON validation via GitHub Actions. All JSON files are automatically linted on push and pull requests.

### Contributing
1. Fork the repository
2. Make your changes to the mock configuration
3. Test locally with `./test-local.sh` (optional)
4. Ensure JSON files are valid
5. Submit a pull request

## Troubleshooting

### Container Won't Start
- Ensure the JSON file is valid and properly mounted
- Check that port 9933 is not already in use
- Verify the platform flag is set for ARM Macs

### Mock Responses Not Working
- Verify the JSON structure matches MockServer expectations format
- Check container logs: `docker logs substrate-mockserver`
- Ensure the request method and path match the expectations

### ARM Mac Issues
Always use the `--platform linux/amd64` flag when running on ARM-based Macs to ensure compatibility.

## License

This project is open source. Please check the repository for license details.

## Related Links

- [MockServer Documentation](https://www.mock-server.com/)
- [Substrate Documentation](https://docs.substrate.io/)
- [Polkadot RPC Documentation](https://polkadot.js.org/docs/substrate/rpc)
