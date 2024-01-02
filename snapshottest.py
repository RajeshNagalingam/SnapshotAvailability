import boto3

def check_snapshots_availability(region_name='your-region', tag_key='Scheduler', tag_value='your-tag-value'):
    # Create an EC2 client for the specified region
    ec2 = boto3.client('ec2', region_name=region_name)

    # Get information about all EBS volumes with the specified tag
    response = ec2.describe_volumes(Filters=[{'Name': f'tag:{tag_key}', 'Values': [tag_value]}])

    # Iterate through each volume
    for volume in response['Volumes']:
        volume_id = volume['VolumeId']

        # Check if there are snapshots for the volume
        snapshots = ec2.describe_snapshots(Filters=[{'Name': 'volume-id', 'Values': [volume_id]}])['Snapshots']

        if snapshots:
            print(f"Snapshots are available for EBS volume {volume_id} in region {region_name}:")
            for snapshot in snapshots:
                print(f"  Snapshot ID: {snapshot['SnapshotId']}, Status: {snapshot['State']}")
        else:
            print(f"No snapshots available for EBS volume {volume_id} in region {region_name}")

if __name__ == "__main__":
    # Replace 'your-region' and 'your-tag-value' with your actual AWS region and tag value
    check_snapshots_availability(region_name='your-region', tag_value='your-tag-value')
