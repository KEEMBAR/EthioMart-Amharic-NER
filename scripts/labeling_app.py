import streamlit as st
import os
import json
import random
from glob import glob

# --- CONFIG ---
ENTITY_LABELS = [
    "O", "B-Product", "I-Product", "B-LOC", "I-LOC", "B-PRICE", "I-PRICE"
]
LABEL_COLORS = {
    "O": "#f0f0f0",
    "B-Product": "#ffe082",
    "I-Product": "#fff9c4",
    "B-LOC": "#b3e5fc",
    "I-LOC": "#e1f5fe",
    "B-PRICE": "#c8e6c9",
    "I-PRICE": "#e8f5e9"
}

# --- DATA LOADING ---
@st.cache_data(show_spinner=False)
def load_all_messages(data_dir="../data/processed/text", sample_size=40):
    channel_dirs = [os.path.join(data_dir, d) for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d))]
    all_files = []
    for channel in channel_dirs:
        files = glob(os.path.join(channel, "*.json"))
        all_files.extend(files)
    if len(all_files) == 0:
        return []
    sample_files = random.sample(all_files, min(sample_size, len(all_files)))
    messages = []
    for file_path in sample_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            msg = json.load(f)
        messages.append({
            'file': file_path,
            'tokens': msg['tokens'],
            'text': msg.get('text', ''),
            'channel': msg.get('channel_username', ''),
            'id': msg.get('message_id', '')
        })
    return messages

# --- APP ---
st.set_page_config(page_title="Amharic NER Labeling", layout="wide")
st.title("Amharic NER Labeling Tool (CoNLL Format)")

st.markdown("""
Assign NER labels to each token. Your progress is saved in the browser until you export.
""")

messages = load_all_messages()
if not messages:
    st.error("No messages found. Please check your data directory.")
    st.stop()

# Session state for progress
if 'labeled_data' not in st.session_state:
    st.session_state.labeled_data = [{} for _ in range(len(messages))]
if 'current_idx' not in st.session_state:
    st.session_state.current_idx = 0

def show_message(idx):
    msg = messages[idx]
    st.subheader(f"Message {idx+1} / {len(messages)}")
    st.write(f"**Channel:** {msg['channel']} | **ID:** {msg['id']}")
    st.text_area("Original Text", msg['text'], height=120, disabled=True)
    st.markdown("**Label each token:**")
    cols = st.columns(min(len(msg['tokens']), 10))  # up to 10 columns for better layout
    labels = st.session_state.labeled_data[idx].get('labels', ["O"] * len(msg['tokens']))
    new_labels = []
    for i, token in enumerate(msg['tokens']):
        # Robust default index
        default_index = ENTITY_LABELS.index(labels[i]) if labels[i] in ENTITY_LABELS else 0
        with cols[i % len(cols)]:
            st.markdown(f'<span style="background-color:{LABEL_COLORS[ENTITY_LABELS[default_index]]};padding:2px 6px;border-radius:4px;">{token}</span>', unsafe_allow_html=True)
            new_label = st.selectbox(
                f"Label for token {i+1}", ENTITY_LABELS, index=default_index, key=f"label_{idx}_{i}"
            )
        new_labels.append(new_label)
    st.session_state.labeled_data[idx] = {
        'tokens': msg['tokens'],
        'labels': new_labels,
        'text': msg['text'],
        'file': msg['file']
    }

show_message(st.session_state.current_idx)

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Previous", disabled=st.session_state.current_idx == 0):
        st.session_state.current_idx -= 1
with col2:
    st.write(f"Message {st.session_state.current_idx+1} of {len(messages)}")
with col3:
    if st.button("Next", disabled=st.session_state.current_idx == len(messages)-1):
        st.session_state.current_idx += 1

st.markdown("---")

# Export section
def export_conll(labeled_data):
    lines = []
    for item in labeled_data:
        if not item or 'tokens' not in item or 'labels' not in item:
            continue
        for token, label in zip(item['tokens'], item['labels']):
            lines.append(f"{token} {label}")
        lines.append("")
    return "\n".join(lines)

if st.button("Export Labeled Data to CoNLL Format"):
    conll_data = export_conll(st.session_state.labeled_data)
    st.download_button(
        label="Download CoNLL File",
        data=conll_data,
        file_name="ner_labeled_sample.conll",
        mime="text/plain"
    )
    st.success("Exported labeled data!") 