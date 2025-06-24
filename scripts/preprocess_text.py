import os
import json
import re
from glob import glob
from typing import List
import emoji
import nltk
from nltk.tokenize import word_tokenize

# Download tokenizer model if not present
nltk.download('punkt', quiet=True)

# Amharic punctuation normalization map
PUNCTUATION_MAP = {
    '፡': ' ',  # Ethiopic wordspace to space
    '።': '.',
    '፣': ',',
    '፤': ';',
    '፥': ':',
    '፦': ':',
    '፧': '?',
    '፨': '.',
}

LATIN_PATTERN = re.compile(r'[A-Za-z]+')
MULTISPACE_PATTERN = re.compile(r'\s+')


def clean_amharic_text(text: str) -> str:
    """
    Clean Amharic text by:
    - Removing URLs
    - Removing emojis
    - Removing long dot sequences
    - Keeping Amharic Unicode, basic punctuation, letters, and numbers
    - Normalizing whitespace and punctuation
    """
    if not isinstance(text, str):
        return ""
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    # Remove emojis
    text = emoji.replace_emoji(text, replace='')
    # Remove long sequences of dots (e.g. .........)
    text = re.sub(r'\.{3,}', ' ', text)
    # Replace Amharic punctuation with standard
    for am_punct, std_punct in PUNCTUATION_MAP.items():
        text = text.replace(am_punct, std_punct)
    # Keep Amharic Unicode range (1200-137F), basic punctuation, letters, numbers
    text = re.sub(r'[^\w\s\u1200-\u137F.,!?]', '', text)
    # Remove Latin characters
    text = LATIN_PATTERN.sub('', text)
    # Normalize whitespace
    text = MULTISPACE_PATTERN.sub(' ', text)
    return text.strip()


def tokenize_amharic_text(text: str) -> List[str]:
    """Tokenize Amharic text using whitespace (safe for Amharic)."""
    return text.split()


def preprocess_channel(channel: str, raw_dir: str, processed_dir: str):
    """
    Preprocess all messages in a channel: clean and tokenize text, save as JSON.
    """
    in_dir = os.path.join(raw_dir, channel)
    out_dir = os.path.join(processed_dir, channel)
    os.makedirs(out_dir, exist_ok=True)
    files = glob(os.path.join(in_dir, 'msg_*.json'))
    count = 0
    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as f:
            msg = json.load(f)
        text = msg.get('text', '')
        cleaned_text = clean_amharic_text(text)
        tokens = tokenize_amharic_text(cleaned_text)
        msg['cleaned_text'] = cleaned_text
        msg['tokens'] = tokens
        out_path = os.path.join(out_dir, os.path.basename(file_path))
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(msg, f, ensure_ascii=False, indent=2)
        count += 1
    print(f"Channel {channel}: Processed {count} messages.")


def main():
    """
    Preprocess all channels: clean and tokenize all messages.
    """
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_dir = os.path.join(project_root, 'data', 'raw', 'text')
    processed_dir = os.path.join(project_root, 'data', 'processed', 'text')
    os.makedirs(processed_dir, exist_ok=True)
    channels = [d for d in os.listdir(raw_dir) if os.path.isdir(os.path.join(raw_dir, d))]
    for channel in channels:
        preprocess_channel(channel, raw_dir, processed_dir)


if __name__ == '__main__':
    main()
