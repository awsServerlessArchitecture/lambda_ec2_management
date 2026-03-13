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
<img width="1898" height="497" alt="ec2_status_before_lambda_invoke" src="https://github.com/user-attachments/assets/8610dbe0-0742-4935-ae1d-6c3d2ac137c7" />

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
<img width="1895" height="770" alt="image" src="https://github.com/user-attachments/assets/c3f7e119-020d-48cf-b0ac-10259f40cc24" />

```python
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
```

---

## 🧪 Testing
1. Save and **manually invoke** the Lambda function.
  - Test from the Lambda Console
  - In the Lambda function page, click Test.
  - Create a new test event:
  - Event name: ManualInvoke
  - Leave the JSON as default (you don’t need to pass anything for this assignment).
  - Click Save and Test.
  - Check the Execution results and Logs section:
  - You’ll see your print() outputs (e.g., current state, started/stopped IDs).
  - If EC2 actions were triggered, they’ll show here.
2. Check the **EC2 dashboard**:
   - The `Auto-Stop` instance should transition to **stopped**.
   - The `Auto-Start` instance should transition to **running** (if it was stopped).

This is ec2 status taken before lambda run.
<img width="1712" height="396" alt="image" src="https://github.com/user-attachments/assets/c0095d4c-3828-4f26-9cce-29ccc33275ff" />


This is test logs on lambda invoke.
<img width="1900" height="612" alt="image" src="https://github.com/user-attachments/assets/656e5439-3b1e-412e-b52d-34f1cf7917f6" />


This ec2 status taken after lambda run.
<img width="1901" height="392" alt="image" src="https://github.com/user-attachments/assets/c3eb080b-0e48-4d11-843f-f8a734224532" />

3. you can configure cloudwatch log group and Review **CloudWatch Logs** for confirmation of actions taken.
   <img width="1901" height="740" alt="image" src="https://github.com/user-attachments/assets/1ff7a3d2-9c6d-47f0-9441-98c5613a02cb" />

---
You have two options:

1. **Attach AWS Managed Policy**  
   - Add **`AWSLambdaBasicExecutionRole`** to your Lambda role.  
   - This automatically includes the correct CloudWatch Logs permissions.

2. **Add Custom Logs Block**  
   If you want to extend your JSON, add this statement:

   ```json
   {
     "Effect": "Allow",
     "Action": [
       "logs:CreateLogGroup",
       "logs:CreateLogStream",
       "logs:PutLogEvents"
     ],
     "Resource": "arn:aws:logs:*:*:*"
   }
   ```

---

### 📌 Next Steps
1. Edit your Lambda role in IAM.
2. Attach either `AWSLambdaBasicExecutionRole` or add the custom block above.
3. Re-run your Lambda.  
   - CloudWatch will now automatically create the log group `/aws/lambda/<FunctionName>`.  
   - You’ll see your `print()` outputs in the log stream.

---


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
- Verified automation via manual invocation.

---
