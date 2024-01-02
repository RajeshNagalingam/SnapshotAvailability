import boto3
from datetime import datetime

def check_snapshots_after_date(region_name='your-region', tag_key='SchedulerID', tag_value='your-tag-value', user_date='2023-01-01'):
    # Convert user input date string to a datetime object
    user_date_datetime = datetime.strptime(user_date, '%Y-%m-%d')

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
            print(f"Snapshots created after {user_date} for EBS volume {volume_id} in region {region_name}:")
            for snapshot in snapshots:
                snapshot_date = snapshot['StartTime'].replace(tzinfo=None)
                if snapshot_date > user_date_datetime:
                    print(f"  Snapshot ID: {snapshot['SnapshotId']}, Created at: {snapshot_date}")
        else:
            print(f"No snapshots available for EBS volume {volume_id} in region {region_name}")

if __name__ == "__main__":
    # Replace 'your-region', 'your-tag-value', and '2023-01-01' with your actual AWS region, tag value, and user date
    check_snapshots_after_date(region_name='your-region', tag_value='your-tag-value', user_date='2023-01-01')
