import re
from bs4 import BeautifulSoup
from datetime import datetime

from gen_helper.config import CONFIG
from msft_helper.auth import generate_token
from msft_helper.outlook_client import fetch_emails, fetch_email_body


"""
    Using BeautifulSoup and regex extract the total charges from the email body.
    If the email format changes slightly, you may need to adjust the regex pattern.
"""


def extract_total_charges_from_email_body(html_content):

    balance_amount = None
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Find the td that contains the amount due by searching for the pattern or specific style
    amount_due_td = soup.find("td", string=re.compile(r"\$\s*\d+\.\d{2}"))

    # Extract the number without the dollar sign using regex
    if amount_due_td:
        amount_due_text = amount_due_td.get_text(strip=True)
        amount_match = re.search(
            r"\d+\.\d{2}", amount_due_text
        )  # Extract only the numeric part
        if amount_match:
            balance_amount = amount_match.group(0).replace("$", "")
            print(f"Amount Due: {balance_amount}")
        else:
            print("Amount not found.")
    else:
        print("Amount due field not found.")

    return balance_amount


"""
    Main function to login to outlook main and extract the total charge for reliance
    @return: total_charge: float or None
"""


def main(headers):
    try:
        sender_filter = CONFIG.reliance_water_sender_filter
        subject_filter = CONFIG.reliance_water_subject_filter

        # get emails
        emails = fetch_emails(headers, subject_filter, sender_filter)

        total_charge = None
        received_date = None
        # read email body
        if not emails:
            print("No emails found matching the criteria.")
        else:
            for email in emails:
                # download_attachments(email['id'], headers, dir_to_save_emails)
                body = fetch_email_body(headers, email["id"])
                received_date_str = email["receivedDateTime"]
                received_date = datetime.strptime(received_date_str, "%Y-%m-%dT%H:%M:%SZ")
                total_charge = extract_total_charges_from_email_body(body)

        return {
            "total_charge": total_charge if total_charge else 0,
            "month": received_date.month if received_date else None,
            "year": received_date.year if received_date else None,
        }
    except Exception as e:
        print(f"failed to get bill for RL water heater {str(e)}")


if __name__ == "__main__":
    access_token = generate_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    total_charge = main(headers)
    print(f"Total Charges for reliance: ${total_charge}")
