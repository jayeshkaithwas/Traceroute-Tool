import socket
import struct
import time
import sys
from datetime import datetime

class Traceroute:
    def __init__(self, destination, max_hops=30, timeout=2):
        self.destination = destination
        self.max_hops = max_hops
        self.timeout = timeout
        self.port = 33434  # Starting port for UDP packets
    
    def create_socket(self, ttl):
        """Create and configure the ICMP socket with specified TTL"""
        icmp = socket.getprotobyname('icmp')
        udp = socket.getprotobyname('udp')
        
        # Create the sockets we'll use for tracerouting
        recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)
        
        # Set the time to live
        send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
        
        return recv_socket, send_socket
    
    def run_trace(self):
        """Execute the traceroute and print results"""
        print(f"\nTraceroute to {self.destination}")
        print("Hop\tIP\t\t\tHostname\t\tTime")
        print("-" * 60)
        
        dest_addr = socket.gethostbyname(self.destination)
        
        for ttl in range(1, self.max_hops + 1):
            try:
                recv_socket, send_socket = self.create_socket(ttl)
            except socket.error as e:
                print(f"Error creating socket: {e}")
                continue
            
            recv_socket.settimeout(self.timeout)
            recv_socket.bind(("", 0))
            
            send_time = time.time()
            try:
                # Send an empty UDP packet to an unlikely port
                send_socket.sendto(b"", (dest_addr, self.port))
                
                # Wait for the response
                packet, curr_addr = recv_socket.recvfrom(512)
                receive_time = time.time()
                
                # Parse the IP header
                ip_header = packet[20:28]
                type, code, checksum, p_id, sequence = struct.unpack("bbHHh", ip_header)
                
                try:
                    curr_name = socket.gethostbyaddr(curr_addr[0])[0]
                except socket.error:
                    curr_name = curr_addr[0]
                
                # Calculate round-trip time
                rtt = (receive_time - send_time) * 1000  # Convert to milliseconds
                
                # Print the results
                print(f"{ttl}\t{curr_addr[0]}\t{curr_name}\t\t{rtt:.2f}ms")
                
                if curr_addr[0] == dest_addr:
                    break
                
            except socket.error as e:
                print(f"{ttl}\t*\t\tRequest timed out")
            
            finally:
                send_socket.close()
                recv_socket.close()
    
    def save_results(self, filename=None):
        """Save traceroute results to a file"""
        if filename is None:
            filename = f"traceroute_{self.destination}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(filename, 'w') as f:
            f.write(f"Traceroute to {self.destination}\n")
            f.write(f"Maximum hops: {self.max_hops}\n")
            f.write(f"Timeout: {self.timeout} seconds\n")
            f.write("-" * 60 + "\n")
            
            # Redirect stdout temporarily to capture the trace
            old_stdout = sys.stdout
            sys.stdout = f
            self.run_trace()
            sys.stdout = old_stdout
            
        print(f"\nResults saved to {filename}")

def main():
    # Example usage
    destination = input("Enter destination host/IP: ")
    max_hops = int(input("Enter maximum hops (default 30): ") or "30")
    timeout = float(input("Enter timeout in seconds (default 2): ") or "2")
    
    tracer = Traceroute(destination, max_hops, timeout)
    tracer.run_trace()
    
    save = input("\nSave results to file? (y/n): ").lower()
    if save == 'y':
        filename = input("Enter filename (leave blank for auto-generated): ")
        tracer.save_results(filename if filename else None)

if __name__ == "__main__":
    main()
