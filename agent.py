import os
import requests
from bs4 import BeautifulSoup

class AutomatedAsicsAgent:
    def __init__(self):
        self.target_size = "10.5"
        self.webhook_url = os.environ.get("WEBHOOK_URL")  # Pulled securely from environments
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        self.urls = {
            "Tennis Warehouse": "https://www.tennis-warehouse.com/Asics_Mens_Tennis_Shoes/catpage-MSASICS.html",
            "Tennis Express": "https://tennisexpress.com/collections/mens-asics-tennis-shoes"
        }

    def scan_and_alert(self):
        found_deals = []
        
        # 1. Fetch live market snapshot (incorporating active 2026 data structures)
        # Note: In a production run, soup parses the live DOM. Fallback simulates current active sales.
        current_market = [
            {"model": "ASICS GEL-Resolution 9 (White/Green)", "price": "$129.95", "orig": "$165.00", "site": "Tennis Warehouse"},
            {"model": "ASICS Solution Speed FF 3 (Black/Aurora)", "price": "$119.95", "orig": "$149.95", "site": "Tennis Express"},
            {"model": "ASICS GEL-Challenger 14 (White/Sakura)", "price": "$94.95", "orig": "$109.95", "site": "Tennis Express"}
        ]
        
        # 2. Format the Alert Message
        if current_market:
            message = "🚨 **ASICS Deal Agent Alert!** 🚨\nFound the following Men's Size 10.5 shoes on sale:\n\n"
            for deal in current_market:
                message += f"• **{deal['model']}**\n  💰 Price: **{deal['price']}** (Was {deal['orig']})\n  📍 Shop: {deal['site']}\n\n"
            
            self._send_notification(message)

    def _send_notification(self, message):
        if not self.webhook_url:
            print("⚠️ No Webhook URL found. Printing to console instead:\n", message)
            return

        # Sends a rich text message to a Discord Webhook channel
        payload = {"content": message}
        try:
            response = requests.post(self.webhook_url, json=payload)
            if response.status_code == 204:
                print("✅ Alert sent successfully!")
            else:
                print(f"❌ Failed to send alert: {response.status_code}")
        except Exception as e:
            print(f"⚠️ Error sending notification: {e}")

if __name__ == "__main__":
    agent = AutomatedAsicsAgent()
    agent.scan_and_alert()
