import miniupnpc
import nopasaran.utils as utils
from nopasaran.decorators import parsing_decorator

class UPnPCPrimitives:
    """
    Class containing UPnP action primitives for the state machine.
    """

    @staticmethod
    @parsing_decorator(input_args=0, output_args=0)
    def discover(inputs, outputs, state_machine):
        """
        Discover UPnP devices on the network and print the discovery results.
        
        Number of input arguments: 0
        
        Number of output arguments: 0
        
        This primitive performs the following steps:
          - Creates a UPnP object.
          - Sets a discovery delay (in milliseconds).
          - Discovers UPnP-enabled devices (such as routers).
          - If devices are found, selects the Internet Gateway Device (IGD) and prints its LAN and external IP addresses.
          - If no devices are found, prints an error message.
        """
        # Create a UPnP object and set the discovery delay
        upnp = miniupnpc.UPnP()
        upnp.discoverdelay = 200  # Discovery delay in milliseconds

        # Discover UPnP devices on the network
        num_devices = upnp.discover()
        print("Devices discovered:", num_devices)

        # If devices are discovered, select the appropriate device (IGD)
        if num_devices > 0:
            upnp.selectigd()
            print("Selected UPnP device:")
            print("  LAN IP address:", upnp.lanaddr)
            print("  External IP address:", upnp.externalipaddress())
        else:
            print("No UPnP devices found.")

    @staticmethod
    @parsing_decorator(input_args=3, output_args=0)
    def add_port_mapping(inputs, outputs, state_machine):
        """
        Add a port mapping using UPnP, mimicking the 'upnpc -a' command.
        
        Number of input arguments: 3
            - The external port to open.
            - The internal port on the local machine.
            - The protocol (e.g., 'TCP' or 'UDP').
        
        Number of output arguments: 0
        
        This primitive performs the following steps:
          - Retrieves the external port, internal port, and protocol values from the state machine.
          - Creates a UPnP object and performs a discovery.
          - If an IGD is found, it selects the device and retrieves the local (LAN) address.
          - Attempts to add a port mapping with the given parameters.
          - Prints whether the port mapping was successfully added or if it failed.
        """
        # Retrieve values from the state machine
        external_port = state_machine.get_variable_value(inputs[0])
        internal_port = state_machine.get_variable_value(inputs[1])
        protocol = state_machine.get_variable_value(inputs[2])

        # Create a UPnP object and set discovery delay
        upnp = miniupnpc.UPnP()
        upnp.discoverdelay = 200

        # Discover UPnP devices
        num_devices = upnp.discover()
        if num_devices > 0:
            upnp.selectigd()
            lan_addr = upnp.lanaddr

            # Add port mapping: arguments are external port, protocol, internal host, internal port,
            # description, and remote host (empty string indicates any remote host).
            result = upnp.addportmapping(int(external_port), protocol, lan_addr, int(internal_port), 'Nopasaran mapping', '')
            if result:
                print(f"Port mapping added: external port {external_port} -> {lan_addr}:{internal_port} [{protocol}]")
            else:
                print("Failed to add port mapping.")
        else:
            print("No UPnP devices found. Cannot add port mapping.")