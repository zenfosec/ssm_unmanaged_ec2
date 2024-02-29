#!/usr/bin/env python3

import boto3
import csv
import datetime

def get_ec2_instances_without_ssm(keypairs={}):
    # Initialize Boto3 clients for EC2 and SSM
    ec2_client = boto3.client('ec2')
    ssm_client = boto3.client('ssm')
    # Retrieve a list of all EC2 instances
    ec2_instances = ec2_client.describe_instances()
    # Initialize an empty list to store instances without SSM associations
    instances_without_ssm = []
    # Iterate through the EC2 instances
    for reservation in ec2_instances['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            private_ip = instance.get('PrivateIpAddress', 'N/A')
            key_name = instance.get('KeyName', 'N/A')
            description = instance.get('Description', 'N/A')
            # Check if the instance has SSM associations
            ssm_associations = ssm_client.list_associations(
                AssociationFilterList=[
                    {
                        'key': 'InstanceId',
                        'value': instance_id
                    },
                    {
                        'key': 'AssociationName',
                        'value': 'AWS-RunShellScript'
                    }
                ]
            )
            # If the instance has no SSM associations, add it to the list
            if not ssm_associations['Associations']:
                # Enumerate keypairs to find the fingerprint for the key name
                for key_pair in keypairs['KeyPairs']:
                    if key_name == key_pair['KeyName']:
                        key_fingerprint = key_pair['KeyFingerprint']
                instances_without_ssm.append({
                    'InstanceID': instance_id,
                    'PrivateIpAddress': private_ip,
                    'Description': description,
                    'KeyName': key_name,
                    'KeyFingerprint': key_fingerprint,
                })
    return instances_without_ssm

def get_ec2_keypairs():
    # Initialize Boto3 clients for EC2 and SSM
    ec2_client = boto3.client('ec2')
    ec2_keys = ec2_client.describe_key_pairs()
    return ec2_keys

if __name__ == "__main__":
    keys = get_ec2_keypairs()
    instances_without_ssm = get_ec2_instances_without_ssm(keys)
    
    # Write the instances to a CSV file
    now = datetime.datetime.now()
    date_string = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"instances_without_ssm_{date_string}.csv"
    with open(filename, mode='w') as csv_file:
        fieldnames = ['InstanceID', 'PrivateIpAddress', 'Description', 'KeyName', 'KeyFingerprint']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for instance in instances_without_ssm:
            writer.writerow(instance)