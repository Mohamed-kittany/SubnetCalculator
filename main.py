from validator import validate_ip, validate_cidr, get_class_based_cidr
from subnet_calculator import SubnetCalculator


def main():
    ip = input("Enter an IP address: ")
    if not validate_ip(ip):
        print("Invalid IP address format.")
        return

    try:
        # Validate and set CIDR early to prevent processing invalid or inappropriate IP addresses.
        cidr = get_class_based_cidr(ip)
    except ValueError as e:
        print(e)  # Print the specific error message (for Class D, E, or loopback)
        return

    cidr_input = input("Enter a CIDR (optional): ")
    if cidr_input and validate_cidr(cidr_input):
        cidr = int(cidr_input)  # Only override the determined CIDR if input is valid

    calculator = SubnetCalculator(ip, cidr)

    partition_type = input("Partition by number of hosts or subnets? (hosts/subnets): ")
    if partition_type not in ["hosts", "subnets"]:
        print("Invalid partition type.")
        return

    number_input = input(f"Enter number of {partition_type}: ")
    if not number_input.isdigit():
        print("Invalid number.")
        return

    try:
        subnet_info = calculator.calculate_subnets(partition_type, number_input)
        print("Subnet Information:")
        for key, value in subnet_info.items():
            if isinstance(value, list):
                print(f"{key}: ")
                for item in value:
                    print(f"  Network: {item[0]}, Broadcast: {item[1]}")
            else:
                print(f"{key}: {value}")
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
