import boto3

def is_guardduty_enabled(account_id, region):
    try:
        # Create a Boto3 session for AWS services
        session = boto3.Session(region_name=region)

        # Create a GuardDuty client
        guardduty_client = session.client('guardduty')

        # Get the list of detectors (should be one in most cases)
        detectors = guardduty_client.list_detectors()

        # Check if any detectors are returned
        if 'DetectorIds' in detectors and len(detectors['DetectorIds']) > 0:
            return True
        else:
            return False

    except Exception as e:
        print("An error occurred:", e)
        return False

if __name__ == "__main__":
    aws_account_id = input("Enter AWS Account ID: ")
    aws_region = input("Enter AWS Region: ")

    enabled = is_guardduty_enabled(aws_account_id, aws_region)
    if enabled:
        print("GuardDuty is enabled for AWS Account", aws_account_id)
    else:
        print("GuardDuty is not enabled for AWS Account", aws_account_id)

