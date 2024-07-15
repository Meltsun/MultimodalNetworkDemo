#!/bin/bash

# Check if IP address and port are provided as arguments
if [ $# -ne 2 ]; then
    echo "Usage: $0 <server_ip> <port>"
    exit 1
fi

# iPerf server IP address and port from arguments
SERVER_IP=$1
PORT=$2

# Function to run iPerf client
run_iperf() {
    iperf -c "$SERVER_IP" -i 1 -p "$PORT" -u -b 8M -e -t 100
}

# Main loop
while true; do
    # Try to run iPerf client and capture its exit status
    run_iperf
    EXIT_STATUS=$?

    # Check if iPerf client exited successfully
    if [ $EXIT_STATUS -eq 0 ]; then
        echo "iPerf client completed successfully."
    else
        echo "iPerf client failed or server is down. Retrying in 1 second..."
    fi

    # Wait for 1 second before retrying
    sleep 1
done
