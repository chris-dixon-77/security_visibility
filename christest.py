import boto3

# Initialize AWS clients
cloudtrail_client = boto3.client('cloudtrail')
organizations_client = boto3.client('organizations')

def get_cloudtrail_log_name(account_id):
    response = cloudtrail_client.describe_trails()
    for trail in response.get('trailList', []):
        if trail['IsMultiRegionTrail'] and trail['IncludeGlobalServiceEvents']:
            if account_id in trail['TrailARN']:
                return trail['Name']
    return None

def is_organizational_trail(trail_name):
    response = cloudtrail_client.get_trail_status(Name=trail_name)
    if 'IsOrganizationTrail' in response:
        return response['IsOrganizationTrail']
    return False

def is_account_in_organization(account_id):
    try:
        # Create a boto3 client for the Organizations service
        organizations_client = boto3.client('organizations')
        
        # Use the describe_account API to check if the account is part of an organization
        response = organizations_client.describe_organization(AccountId=account_id)
        
        # If the account is part of an organization, it will return information about the organization
        organization_info = response['Organization']
        return True
    except organizations_client.exceptions.AWSOrganizationsNotInUseException:
        return False
    except Exception as e:
        print(f"An error occurred while checking AWS Organization status: {str(e)}")
        return False

if __name__ == "__main__":
    account_id = input("Enter the AWS account ID: ")
    account_in_organization = is_account_in_organization(account_id)
    
    log_name = get_cloudtrail_log_name(account_id)
    if log_name:
        print(f"CloudTrail log name: {log_name}")
        
        is_org_trail = is_organizational_trail(log_name)
        if is_org_trail:
            print("This CloudTrail log is part of an organizational trail.")
        else:
            print("This CloudTrail log is standalone.")
    else:
        print("CloudTrail log not found for the provided account ID.")
    
    if account_in_organization:
        print(f"The AWS account {account_id} is part of an organization.")
    else:
        print(f"The AWS account {account_id} is not part of an organization.")

