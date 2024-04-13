import ipaddress
from validator import get_class_based_cidr


class SubnetCalculator:
    def __init__(self, ip, cidr=None):
        self.ip = ip
        self.cidr = cidr if cidr is not None else get_class_based_cidr(self.ip)
        self.network = ipaddress.IPv4Network(f"{self.ip}/{self.cidr}", strict=False)

    def calculate_subnets(self, partition_type, number):
        """Calculate subnets based on partition type and number of partitions required."""
        number = int(number)
        if partition_type == "hosts":
            new_prefix = 32 - (number.bit_length() + 1)
        else:  # subnets
            new_prefix = self.cidr + (number - 1).bit_length()
            if new_prefix > 32:
                raise ValueError("Requested number of subnets is too high for the given IP block.")

        subnets = list(self.network.subnets(new_prefix=new_prefix))
        return {
            "Subnet Mask": str(self.network.netmask),
            "CIDR": f"/{self.network.prefixlen}",
            "Number of Hosts": self.network.num_addresses - 2,
            "Number of Subnets": len(subnets),
            "First Two Subnets": [(str(sub.network_address), str(sub.broadcast_address)) for sub in subnets[:2]],
            "Last Two Subnets": [(str(sub.network_address), str(sub.broadcast_address)) for sub in subnets[-2:]]
        }
