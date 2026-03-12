---

# Automated Instance Management Using AWS Lambda and Boto3

## 📌 Objective
This project demonstrates how to automate the **starting and stopping of EC2 instances** using **AWS Lambda** and **Boto3** (Amazon’s Python SDK). The automation is based on instance tags, making it flexible and reusable for different environments.

---
 
## 🛠️ Prerequisites
- AWS account with access to **EC2**, **IAM**, and **Lambda**.
- Basic knowledge of Python and AWS services.
- Two EC2 instances (free-tier `t2.micro` recommended).

---

## ⚙️ Setup Steps

### 1. EC2 Instances
- Launch **two EC2 instances**.
- Tag them as follows:
  - Instance 1 → `Key: Action`, `Value: Auto-Stop`
  - Instance 2 → `Key: Action`, `Value: Auto-Start`

### 2. IAM Role for Lambda
- Navigate to **IAM → Roles → Create Role**.
- Select **Lambda** as the trusted entity.
- Attach the policy: **AmazonEC2FullAccess**  
  *(Note: For production, use least-privilege policies instead of full access.)*
- Name the role: `LambdaEC2ManagerRole`.

### 3. Lambda Function
- Go to **Lambda → Create Function**.
- Runtime: **Python 3.x**.
- Assign the IAM role created above.
- Add the following code:

```python
import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')

    # Stop instances tagged Auto-Stop
    stop_response = ec2.describe_instances(
        Filters=[{'Name': 'tag:Action', 'Values': ['Auto-Stop']}]
    )
    stop_ids = [i['InstanceId'] for r in stop_response['Reservations'] for i in r['Instances']]
    
    for i in stop_ids:
        state = ec2.describe_instances(InstanceIds=[i])['Reservations'][0]['Instances'][0]['State']['Name']
        if state != "stopped":
            ec2.stop_instances(InstanceIds=[i])
            print(f"Stopped instance: {i}")
        else:
            print(f"Instance {i} is already stopped.")

    # Start instances tagged Auto-Start
    start_response = ec2.describe_instances(
        Filters=[{'Name': 'tag:Action', 'Values': ['Auto-Start']}]
    )
    start_ids = [i['InstanceId'] for r in start_response['Reservations'] for i in r['Instances']]
    
    for i in start_ids:
        state = ec2.describe_instances(InstanceIds=[i])['Reservations'][0]['Instances'][0]['State']['Name']
        if state != "running":
            ec2.start_instances(InstanceIds=[i])
            print(f"Started instance: {i}")
        else:
            print(f"Instance {i} is already running.")
```

---

## 🧪 Testing
1. Save and **manually invoke** the Lambda function.
2. Check the **EC2 dashboard**:
   - The `Auto-Stop` instance should transition to **stopped**.
   - The `Auto-Start` instance should transition to **running** (if it was stopped).
3. Review **CloudWatch Logs** for confirmation of actions taken.

---

## 🔑 Notes
- By default, new EC2 instances start in the **running** state. To test the `Auto-Start` logic, manually stop the instance before invoking Lambda.
- For production:
  - Use **least-privilege IAM policies**.
  - Consider scheduling Lambda with **CloudWatch Events** (e.g., stop at night, start in morning).
  - Extend tagging logic for additional actions (e.g., `Auto-Reboot`, `Auto-Terminate`).

---

## 📖 Workflow Diagram (Conceptual)

```
EC2 Instances (Tagged) ---> Lambda Function ---> Boto3 EC2 Client ---> Start/Stop Actions
                               |
                               v
                          CloudWatch Logs
```

---

## ✅ Deliverables
- Two EC2 instances with tags (`Auto-Stop`, `Auto-Start`).
- Lambda function with IAM role.
- Verified automation via manual invocation and CloudWatch logs.

---

Would you like me to also add a **“Troubleshooting” section** to the README (covering common issues like IAM permission errors, region mismatches, or Lambda timeout)? That would make it even more robust for onboarding new team members.
