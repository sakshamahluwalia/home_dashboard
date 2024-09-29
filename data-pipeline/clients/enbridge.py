# import os
import re
from bs4 import BeautifulSoup

from gen_helper.config import CONFIG
from msft_helper.auth import generate_token
from msft_helper.outlook_client import fetch_emails, download_attachments, fetch_email_body

# from pdf_helper.parse_pdf import parse_pdf


def extract_total_charges_from_email_attachment(text):
    
    # Define a regular expression pattern to match "Total Charges for Natural Gas" followed by an amount
    pattern = r'T otal Char ges f or Na tur al Gas \$([0-9]+\.[0-9]{2})'
    
    # Search for the pattern in the normalized text
    match = re.search(pattern, text)
    
    if match:
        return match.group(1)  # Return the extracted amount
    else:
        return None
    
def extract_total_charges_from_email_body(html_content):

    balance_amount = None
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the div that contains the balance, using a unique attribute like style or class
    balance_div = soup.find('div', style=re.compile(r'font-size:40px'))

    # Extract the balance using regex to capture the number with decimal points
    if balance_div:
        balance_text = balance_div.get_text(strip=True)
        balance_match = re.search(r'\$\d+\.\d{2}', balance_text)
        if balance_match:
            balance_amount = balance_match.group(0).replace("$", "")
            print(f"Extracted Balance: {balance_amount}")
        else:
            print("Balance not found in the text.")
    else:
        print("Balance div not found.")
    
    return balance_amount


'''
    Main function to login to outlook main and extract the total charge for enbridge
    @return: total_charge: float or None
'''
def main(headers):
    sender_filter = CONFIG.enbridge_sender_filter
    subject_filter = CONFIG.enbridge_subject_filter

    emails = fetch_emails(headers, subject_filter, sender_filter)

    total_charge = None
    # read email body
    if not emails:
        print("No emails found matching the criteria.")
    else:
        for email in emails:
            # download_attachments(email['id'], headers, dir_to_save_emails)
            body = fetch_email_body(headers, email["id"])
            total_charge = extract_total_charges_from_email_body(body)
    
    return float(total_charge) if total_charge else None


if __name__ == "__main__":

    # app directory setup
    # dir_to_save_emails = './emails_from_enbridge'

    # os.makedirs(dir_to_save_emails, exist_ok=True)
    access_token = generate_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    
    total_charge = main(headers)
    print(f"Total Charges for enbridge: ${total_charge}")
            

    # parse pdfs
    # total_charges = None
    # for file in os.listdir(dir_to_save_emails):
    #     if file.endswith('.pdf'):
    #         file_path = os.path.join(dir_to_save_emails, file)
    #         text_content = parse_pdf(file_path)
    #         total_charges = extract_total_charges_from_email_attachment(text_content)
    
    # if total_charges:
    #     print(f"Total Charges for Natural Gas: ${total_charges}")