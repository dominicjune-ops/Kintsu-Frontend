import os
import sys
from datetime import datetime
from generate_reports import generate_daily_report, generate_weekly_report, generate_monthly_report
from slack_report_delivery import send_slack_message
from email_report_delivery import send_email
from notion_report_delivery import update_notion_page

def deliver_reports(report_type, content):
    # Slack delivery
    try:
        send_slack_message("#project-updates", f"{report_type.capitalize()} Report: {content[:100]}...")
    except Exception as e:
        print(f"Slack delivery failed: {e}")

    # Email delivery
    try:
        send_email(f"{report_type.capitalize()} Report", content, "user@example.com")
    except Exception as e:
        print(f"Email delivery failed: {e}")

    # Notion delivery
    try:
        update_notion_page("your-page-id", content)
    except Exception as e:
        print(f"Notion delivery failed: {e}")

def main():
    today = datetime.now()
    day_of_week = today.weekday()  # 0 = Monday
    day_of_month = today.day

    if day_of_month == 1:  # Monthly on 1st
        report_type = "monthly"
        content = generate_monthly_report()
    elif day_of_week == 0:  # Weekly on Monday
        report_type = "weekly"
        content = generate_weekly_report()
    else:  # Daily otherwise
        report_type = "daily"
        content = generate_daily_report()

    deliver_reports(report_type, content)
    print(f"{report_type.capitalize()} report delivered.")

if __name__ == "__main__":
    main()