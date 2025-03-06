import boto3
from datetime import datetime

def check_snapshots_on_date(region_name='your-region', tag_key='CreatedBy', tag_value='your-tag-value', user_date='2025-03-04'):
    # Convert user input date string to a datetime object
    user_date_datetime = datetime.strptime(user_date, '%Y-%m-%d')

    # Create an EC2 client for the specified region
    ec2 = boto3.client('ec2', region_name=region_name)

    # Get information about all EBS volumes with the specified tag
    response = ec2.describe_volumes(Filters=[{'Name': f'tag:{tag_key}', 'Values': [tag_value]}])

    # Track volumes with and without snapshots on the given date
    volumes_with_snapshots = []
    volumes_without_snapshots = []

    # Iterate through each volume
    for volume in response['Volumes']:
        volume_id = volume['VolumeId']

        # Check if there are snapshots for the volume
        snapshots = ec2.describe_snapshots(Filters=[{'Name': 'volume-id', 'Values': [volume_id]}])['Snapshots']

        snapshot_found = False
        if snapshots:
            for snapshot in snapshots:
                snapshot_date = snapshot['StartTime'].replace(tzinfo=None)
                if snapshot_date.date() == user_date_datetime.date():
                    snapshot_found = True
                    print(f"Snapshots created on {user_date} for EBS volume {volume_id} in region {region_name}:")
                    print(f"  Snapshot ID: {snapshot['SnapshotId']}, Created at: {snapshot_date}")

        if not snapshot_found:
            volumes_without_snapshots.append(volume_id)

    # Print volumes without snapshots on the given date
    if volumes_without_snapshots:
        print(f"\nVolumes without snapshots on {user_date} in region {region_name}:")
        for volume_id in volumes_without_snapshots:
            print(f"  Volume ID: {volume_id}")

if __name__ == "__main__":
    # Replace 'your-region', 'your-tag-value', and '2025-03-04' with your actual AWS region, tag value, and user date
    check_snapshots_on_date(region_name='us-east-1', tag_value='Rajesh', user_date='2025-03-04')
