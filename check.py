import boto3

def is_account_in_organization():
    try:
        # Create a boto3 client for the Organizations service
        organizations_client = boto3.client('organizations')
        
        # Use the describe_account API to check if the account is part of an organization
        response = organizations_client.describe_account()
        
        # If the account is part of an organization, it will return information about the organization
        organization_info = response['Account']
        return True
    except organizations_client.exceptions.AWSOrganizationsNotInUseException:
        return False
    except Exception as e:
        print(f"An error occurred while checking AWS Organization status: {str(e)}")
        return False

def get_cloudtrail_logs():
    try:
        # Create a boto3 client for the CloudTrail service
        cloudtrail_client = boto3.client('cloudtrail')
        
        # Use the describe_trails API to get information about CloudTrail trails
        response = cloudtrail_client.describe_trails()
        trails = response['trailList']
        
        return trails
    except Exception as e:
        print(f"An error occurred while fetching CloudTrail logs: {str(e)}")
        return []

if __name__ == "__main__":
    is_in_organization = is_account_in_organization()
    cloudtrail_logs = get_cloudtrail_logs()
    
    if is_in_organization:
        print("The customer is part of an AWS Organization.")
    else:
        print("The customer is not part of an AWS Organization.")

    if len(cloudtrail_logs) == 1:
        print("The customer is using a single CloudTrail log.")
    elif len(cloudtrail_logs) > 1:
        print("The customer is using multiple CloudTrail logs.")
    else:
        print("No CloudTrail logs found for the customer.")

