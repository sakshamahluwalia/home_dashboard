import requests
import base64
import os
from datetime import datetime, timedelta

def fetch_emails(headers, subject_filter=None, sender_filter=None):

    # Calculate the date one month ago
    today = datetime.utcnow()
    last_month_date = today - timedelta(days=30)
    last_month_iso = last_month_date.isoformat() + 'Z'  # ISO 8601 format

    endpoint = 'https://graph.microsoft.com/v1.0/me/messages'
    params = {
        '$select': 'id,subject,from,hasAttachments',
        '$top': 2,  # Adjust as needed
    }
    
    # Build filter query
    filter_queries = [f"receivedDateTime ge {last_month_iso}"]
    if subject_filter:
        filter_queries.append(f"subject eq '{subject_filter}'")
    if sender_filter:
        filter_queries.append(f"from/emailAddress/address eq '{sender_filter}'")
    if filter_queries:
        params['$filter'] = ' and '.join(filter_queries)

    response = requests.get(endpoint, headers=headers, params=params)
    if response.status_code == 200:
        emails = response.json().get('value', [])
        return emails
    else:
        print(f"Failed to fetch emails: {response.status_code}")
        print(response.text)
        return []


def download_attachments(message_id, headers, save_directory):
    endpoint = f'https://graph.microsoft.com/v1.0/me/messages/{message_id}/attachments'
    response = requests.get(endpoint, headers=headers)
    if response.status_code == 200:
        attachments = response.json().get('value', [])
        for attachment in attachments:
            if attachment['@odata.type'] == '#microsoft.graph.fileAttachment':
                file_name = attachment['name']
                if file_name.endswith('.pdf'):
                    content_bytes = attachment['contentBytes']
                    attachment_content = base64.b64decode(content_bytes)
                    file_path = os.path.join(save_directory, file_name)
                    with open(file_path, 'wb') as file:
                        file.write(attachment_content)
                    print(f"Attachment saved to {file_path}")
                    return file_path
    else:
        print(f"Failed to fetch attachments: {response.status_code}")
        print(response.text)
    return None


def fetch_brampton_water_email_from_junk(headers, subject_filter, sender_filter):

    # Calculate the date 5 minutes ago
    now = datetime.utcnow()
    five_minutes_ago = now - timedelta(minutes=2)
    five_minutes_ago_iso = five_minutes_ago.isoformat() + 'Z'  # ISO 8601 format

    endpoint = 'https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messages'
    params = {
        '$select': 'id,subject,from,receivedDateTime,bodyPreview',
        '$top': 1,  # Adjust as needed
    }
    
    # Build filter query
    filter_queries = [f"receivedDateTime ge {five_minutes_ago_iso}"]
    if subject_filter:
        filter_queries.append(f"contains(subject, '{subject_filter}')")
    if sender_filter:
        filter_queries.append(f"from/emailAddress/address eq '{sender_filter}'")
    if filter_queries:
        params['$filter'] = ' and '.join(filter_queries)

    # Fetch emails from the inbox
    response = requests.get(endpoint, headers=headers, params=params)
    inbox_emails = []
    if response.status_code == 200:
        inbox_emails = response.json().get('value', [])
    else:
        print(f"Failed to fetch emails from inbox: {response.status_code}")
        print(response.text)

    # Fetch emails from the Junk folder
    junk_endpoint = 'https://graph.microsoft.com/v1.0/me/mailFolders/junkemail/messages'
    junk_response = requests.get(junk_endpoint, headers=headers, params=params)
    junk_emails = []
    if junk_response.status_code == 200:
        junk_emails = junk_response.json().get('value', [])
    else:
        print(f"Failed to fetch emails from junk folder: {junk_response.status_code}")
        print(junk_response.text)

    # Combine both inbox and junk emails
    all_emails = inbox_emails + junk_emails
    
    return all_emails


def fetch_email_body(headers, email_id):
    """
    This function fetches the full email body for the given email ID.
    """
    endpoint = f'https://graph.microsoft.com/v1.0/me/messages/{email_id}'
    params = {
        '$select': 'body'
    }
    
    response = requests.get(endpoint, headers=headers, params=params)
    if response.status_code == 200:
        email_body = response.json().get('body', {}).get('content', '')
        return email_body
    else:
        print(f"Failed to fetch email body: {response.status_code}")
        print(response.text)
        return None
