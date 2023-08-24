import boto3
import subprocess
import json

# Initialize AWS clients
cloudtrail_client = boto3.client('cloudtrail')
organizations_client = boto3.client('organizations')
guardduty_client = boto3.client('guardduty')
config_client = boto3.client('config')

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

def is_guardduty_enabled(account_id):
    try:
        detectors = guardduty_client.list_detectors()
        if 'DetectorIds' in detectors and len(detectors['DetectorIds']) > 0:
            return True
        else:
            return False

    except Exception as e:
        print("An error occurred:", e)
        return False

def get_detector_ids():
    try:
        command = "aws guardduty list-detectors"
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        detectors_data = json.loads(result.stdout)
        return [detector['DetectorId'] for detector in detectors_data.get('DetectorIds', [])]

    except Exception as e:
        print("An error occurred:", e)
        return []

def get_aggregated_accounts(detector_id):
    try:
        command = f"aws guardduty list-members --detector-id {detector_id}"
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        accounts_data = json.loads(result.stdout)
        return accounts_data.get('Members', [])

    except Exception as e:
        print("An error occurred:", e)
        return []

def is_config_enabled(account_id):
    try:
        response = config_client.describe_configuration_recorders()
        if len(response['ConfigurationRecorders']) > 0:
            return True
        return False
    except Exception as e:
        print(f"An error occurred while checking AWS Config status: {str(e)}")
        return False

if __name__ == "__main__":
    account_id = input("Enter the AWS account ID: ")
    account_in_organization = is_account_in_organization(account_id)
    guardduty_enabled = is_guardduty_enabled(account_id)
    config_enabled = is_config_enabled(account_id)
    detector_ids = get_detector_ids()
    
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
    
    if guardduty_enabled:
        print("AWS GuardDuty is enabled for the account.")
    else:
        print("AWS GuardDuty is not enabled for the account.")
    
    if config_enabled:
        print("AWS Config is enabled for the account.")
    else:
        print("AWS Config is not enabled for the account.")

    for detector_id in detector_ids:
        aggregated_accounts = get_aggregated_accounts(detector_id)
        print(f"Detector ID: {detector_id}")
        if aggregated_accounts:
            print("Aggregated Accounts:")
            for account in aggregated_accounts:
                print("  Account ID:", account['AccountId'], "Region:", account['Region'])
        else:
            print("No aggregated accounts.")
        print("-" * 40)
