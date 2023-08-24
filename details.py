import boto3

def get_guardduty_configuration(account_id, region):
    try:
        # Create a Boto3 session for AWS services
        session = boto3.Session(region_name=region)

        # Create a GuardDuty client
        guardduty_client = session.client('guardduty')

        # Get the publishing frequency of findings
        publishing_frequency = guardduty_client.get_findings_publishing_frequency()

        return publishing_frequency

    except Exception as e:
        print("An error occurred:", e)
        return None

if __name__ == "__main__":
    aws_account_id = input("Enter AWS Account ID: ")
    aws_region = input("Enter AWS Region: ")

    publishing_frequency = get_guardduty_configuration(aws_account_id, aws_region)
    if publishing_frequency:
        print("GuardDuty Configuration for AWS Account", aws_account_id)
        print("Findings Publishing Frequency:", publishing_frequency['FindingPublishingFrequency'])
    else:
        print("Failed to retrieve GuardDuty configuration for AWS Account", aws_account_id)

