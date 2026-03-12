import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')

    # Find instances tagged Auto-Stop
    stop_response = ec2.describe_instances(
        Filters=[{'Name': 'tag:Action', 'Values': ['Auto-Stop']}]
    )
    stop_ids = [i['InstanceId'] for r in stop_response['Reservations'] for i in r['Instances']]
    
    # Log current state of Auto-Stop instances
    for i in stop_ids:
        state = ec2.describe_instances(InstanceIds=[i])['Reservations'][0]['Instances'][0]['State']['Name']
        print(f"Instance {i} is currently {state}")

    if stop_ids:
        ec2.stop_instances(InstanceIds=stop_ids)
        print(f"Stopped instances: {stop_ids}")
    else:
        print("No Auto-Stop instances found.")

    # Find instances tagged Auto-Start
    start_response = ec2.describe_instances(
        Filters=[{'Name': 'tag:Action', 'Values': ['Auto-Start']}]
    )
    start_ids = [i['InstanceId'] for r in start_response['Reservations'] for i in r['Instances']]
    
    # Log current state of Auto-Start instances
    for i in start_ids:
        state = ec2.describe_instances(InstanceIds=[i])['Reservations'][0]['Instances'][0]['State']['Name']
        print(f"Instance {i} is currently {state}")
        
    if start_ids:
        ec2.start_instances(InstanceIds=start_ids)
        print(f"Started instances: {start_ids}")
    else:
        print("No Auto-Start instances found.")