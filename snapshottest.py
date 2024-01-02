import boto3

def check_snapshots_availability():
    # Create an EC2 client
    ec2 = boto3.client('ec2')

    # Get information about all EBS volumes
    response = ec2.describe_volumes()

    # Iterate through each volume
    for volume in response['Volumes']:
        volume_id = volume['VolumeId']

        # Check if there are snapshots for the volume
        snapshots = ec2.describe_snapshots(Filters=[{'Name': 'volume-id', 'Values': [volume_id]}])['Snapshots']

        if snapshots:
            print(f"Snapshots are available for EBS volume {volume_id}:")
            for snapshot in snapshots:
                print(f"  Snapshot ID: {snapshot['SnapshotId']}, Status: {snapshot['State']}")
        else:
            print(f"No snapshots available for EBS volume {volume_id}")

if __name__ == "__main__":
    check_snapshots_availability()
