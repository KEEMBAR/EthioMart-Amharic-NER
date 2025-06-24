import os
import json
import pandas as pd
from pyrogram import Client
from dotenv import load_dotenv
from datetime import datetime
from typing import List, Dict


def load_credentials():
    """Load Telegram API credentials from .env file."""
    load_dotenv()
    api_id = os.getenv("TELEGRAM_API_ID")
    api_hash = os.getenv("TELEGRAM_API_HASH")
    if not api_id or not api_hash:
        raise EnvironmentError("Missing TELEGRAM_API_ID or TELEGRAM_API_HASH in .env file.")
    return int(api_id), api_hash


def get_channels() -> List[str]:
    """Return the list of Telegram e-commerce channels to scrape."""
    return [
        "nevacomputer",
        "Shewabrand",
        "Fashiontera",
        "forfreemarket",
        "aradabrand2",
    ]


def scrape_channel_messages(app: Client, channel: str, limit: int = 500) -> List[Dict]:
    """
    Scrape messages from a single Telegram channel.
    Only collects text and metadata, does NOT download images or documents.
    Stores each message as a separate JSON file in data/raw/text/<channel>/.
    Returns a list of message dictionaries.
    """
    messages = []
    text_dir = os.path.join("..", "data", "raw", "text", channel)
    os.makedirs(text_dir, exist_ok=True)
    try:
        chat_info = app.get_chat(channel)
        channel_title = chat_info.title
        for message in app.get_chat_history(channel, limit=limit):
            text = message.text or message.caption or ""
            if not text.strip():
                continue
            # Prepare message dict with possible entity fields (to be filled by NER later)
            msg = {
                "channel_username": channel,
                "channel_title": channel_title,
                "message_id": message.id,
                "timestamp": message.date.isoformat(),
                "text": text.strip(),
                "views": message.views or 0,
                "media_type": str(message.media) if message.media else None,
                "has_photo": bool(message.photo),
                "has_document": bool(message.document),
                # Entity fields to be filled by NER later
                "product": None,
                "material": None,
                "location": None,
                "price": None,
                "delivery_fee": None,
                "contact_info": None
            }
            # Save each message as a separate JSON file
            msg_filename = f"msg_{message.id}.json"
            msg_path = os.path.join(text_dir, msg_filename)
            with open(msg_path, "w", encoding="utf-8") as f:
                json.dump(msg, f, ensure_ascii=False, indent=2)
            messages.append(msg)
    except Exception as e:
        print(f"[!] Error scraping {channel}: {e}")
    return messages


def main():
    """
    Main workflow: scrape all channels, save per-message, per-channel data, print summary.
    """
    api_id, api_hash = load_credentials()
    channels = get_channels()
    summary = {}
    with Client("ethioMart_session", api_id=api_id, api_hash=api_hash) as app:
        for channel in channels:
            print(f"\n[+] Scraping channel: {channel}")
            msgs = scrape_channel_messages(app, channel)
            summary[channel] = len(msgs)
    print("\n--- Scraping Summary ---")
    for ch, count in summary.items():
        print(f"{ch}: {count} messages scraped.")
    print(f"Total messages scraped: {sum(summary.values())}")


if __name__ == "__main__":
    main() 