import boto3

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

def is_cloudtrail_organization_trail(trail_name):
    try:
        # Create a boto3 client for the CloudTrail service
        cloudtrail_client = boto3.client('cloudtrail')
        
        # Use the describe_trails API to get information about CloudTrail trails
        response = cloudtrail_client.describe_trails()
        trails = response['trailList']
        
        for trail in trails:
            if trail['Name'] == trail_name:
                return trail.get('IsOrganizationTrail', False)
        
        return False
    except Exception as e:
        print(f"An error occurred while fetching CloudTrail log information: {str(e)}")
        return False

if __name__ == "__main__":
    aws_account_id = input("Enter the AWS Account ID: ")
    account_in_organization = is_account_in_organization(aws_account_id)
    
    if account_in_organization:
        print(f"The AWS account {aws_account_id} is part of an organization.")
    else:
        print(f"The AWS account {aws_account_id} is not part of an organization.")
    
  #  trail_name = input(trail)
    is_org_trail = is_cloudtrail_organization_trail(trail_name)
    
    if is_org_trail:
        print(f"The CloudTrail log '{trail_name}' is an organization trail.")
    else:
        print(f"The CloudTrail log '{trail_name}' is not an organization trail.")

