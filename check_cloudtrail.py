import boto3

def check_cloudtrail_logs():
    try:
        # Create a boto3 client for the CloudTrail service
        cloudtrail_client = boto3.client('cloudtrail')
        
        # Use the describe_trails API to get information about CloudTrail trails
        response = cloudtrail_client.describe_trails()
        trails = response['trailList']
        
        if len(trails) == 1:
            return "The customer is using a single CloudTrail log."
        elif len(trails) > 1:
            return "The customer is using multiple CloudTrail logs."
        else:
            return "No CloudTrail logs found for the customer."
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == "__main__":
    result = check_cloudtrail_logs()
    print(result)

