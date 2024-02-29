# EC2 Instances Without SSM

This script, `ssm_unmanaged_ec2_with_keys.py`, is used to identify EC2 instances that are not managed by AWS Systems Manager (SSM). The script retrieves information about all EC2 instances and their associated key pairs, and writes this information to a CSV file.

## Functionality

The script performs the following steps:

1. Retrieves a list of all EC2 instances.
2. For each instance, it checks if the instance is managed by SSM.
3. If the instance is not managed by SSM, it retrieves the key name and key fingerprint associated with the instance.
4. It also retrieves the private IP address and description (if available) of the instance.
5. The information about each unmanaged instance (instance ID, private IP address, key name, key fingerprint, and description) is written to a CSV file.

## Usage

To run the script, use the following command:

python ssm_unmanaged_ec2_with_keys.py