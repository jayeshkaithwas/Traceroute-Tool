# Network Traceroute Tool

A Python-based network diagnostic tool that traces the path of packets across an IP network. This implementation provides detailed hop-by-hop analysis with hostname resolution, timing information, and result logging capabilities.

## Features

- **Customizable Traces**: Configure maximum hops and timeout values
- **Hostname Resolution**: Automatically resolves IP addresses to hostnames when possible
- **Response Timing**: Measures and displays round-trip time for each hop
- **Result Logging**: Save trace results to timestamped files
- **User-Friendly Interface**: Interactive command-line interface for easy usage
- **Detailed Output**: Displays IP addresses, hostnames, and response times for each hop

## Prerequisites

- Python 3.6 or higher
- Root/Administrator privileges (required for raw socket operations)
- Operating System: Linux, macOS, or Windows

## Installation

1. Clone the repository:
```bash
git clone https://github.com/jayeshkaithwas/Traceroute-Tool.git
cd Traceroute-Tool
```

2. No additional dependencies are required as the tool uses Python standard library modules only.

## Usage

### Running from Command Line

```bash
# On Unix-like systems (Linux, macOS)
sudo python3 traceroute.py

# On Windows (run Command Prompt as Administrator)
python traceroute.py
```

### Using as a Module

```python
from traceroute import Traceroute

# Basic usage
tracer = Traceroute("google.com")
tracer.run_trace()

# Custom configuration
tracer = Traceroute(
    destination="github.com",
    max_hops=15,
    timeout=1
)
tracer.run_trace()

# Save results to file
tracer.save_results("trace_results.txt")
```

## Example Output

```
Traceroute to google.com
Hop     IP              Hostname                Time
------------------------------------------------------------
1       192.168.1.1     router.local           1.23ms
2       10.0.0.1        isp-gateway.net        15.67ms
3       172.16.0.1      backbone-1.isp.net     22.89ms
...
```

## Class Reference

### `Traceroute` Class

#### Parameters

- `destination` (str): Target hostname or IP address
- `max_hops` (int, optional): Maximum number of hops to trace. Default: 30
- `timeout` (float, optional): Timeout in seconds for each probe. Default: 2

#### Methods

- `run_trace()`: Executes the traceroute and displays results
- `save_results(filename=None)`: Saves trace results to a file. If no filename is provided, generates a timestamped filename

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Security Considerations

- This tool requires root/administrator privileges to run
- Use caution when tracing to unknown hosts
- Be aware of your organization's security policies regarding network diagnostics

## Support

For support, please open an issue in the GitHub repository.
