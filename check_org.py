import boto3

def check_aws_organization(account_id):
    try:
        # Create a boto3 client for the Organizations service
        organizations_client = boto3.client('organizations')
        
        # Use the describe_organization API to check if the account is part of an organization
        response = organizations_client.describe_organization()
        
        # If the account is part of an organization, it will return information about the organization
        organization_info = response['Organization']
        return f"Account {account_id} is part of an AWS Organization."
    except organizations_client.exceptions.AWSOrganizationsNotInUseException:
        return f"Account {account_id} is not part of an AWS Organization and is a single account."
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == "__main__":
    account_id = input("Enter the AWS Account ID: ")
    result = check_aws_organization(account_id)
    print(result)

def check_cloudtrail_logs():
    try:
        # Create a boto3 client for the CloudTrail service
        cloudtrail_client = boto3.client('cloudtrail')
        
        # Use the describe_trails API to get information about CloudTrail trails
        response = cloudtrail_client.describe_trails()
        trails = response['trailList']
        cloudtrail_logs = get_cloudtrail_logs()
        if len(trails) == 1:
            return "The customer is using a single CloudTrail log."
        elif len(trails) > 1:
            return "The customer is using multiple CloudTrail logs."
        else:
            return "No CloudTrail logs found for the customer."
    except Exception as e:
        return f"An error occurred: {str(e)}"
          
        if not cloudtrail_logs:
            print("No CloudTrail logs found for the customer.")
        else:
            for trail in cloudtrail_logs:
                trail_name = trail['Name']
                is_organization_trail = trail.get('IsOrganizationTrail', False)
 
            print(f"Trail: {trail_name}")
            if is_organization_trail:
                print("This trail is an organization trail.")
            else:
                print("This trail is not an organization trail.")
 
            print("-----")

if not cloudtrail_logs:
        print("No CloudTrail logs found for the customer.")
else:
        for trail in cloudtrail_logs:
            trail_name = trail['Name']
            is_organization_trail = trail.get('IsOrganizationTrail', False)
            
            print(f"Trail: {trail_name}")
            if is_organization_trail:
                print("This trail is an organization trail.")
            else:
                print("This trail is not an organization trail.")
            
            print("-----")
