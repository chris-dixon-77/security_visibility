import boto3

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
    cloudtrail_logs = get_cloudtrail_logs()
    
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

