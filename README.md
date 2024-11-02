# Financial Fraud Prevention Chatbot for Elderly Users

This Gradio-based chatbot application is designed to help elderly users identify and prevent financial fraud. The chatbot engages users in a conversation about potentially suspicious messages they receive, helping them recognize signs of fraud, and provides guidance on taking preventive actions.

## Features

- **Fraud Detection**: Identifies common indicators of fraud in messages, such as requests for money, urgency, or personal information.
- **Conversational Guidance**: Guides users through follow-up questions, prompting them to critically assess the message’s intent.
- **Warnings and Precautions**: Provides warnings against taking any hasty actions and offers recommendations for blocking the sender or ignoring the message.
- **User-Friendly Interface**: Uses Gradio to create a simple, accessible chat interface tailored for elderly users who may not be tech-savvy.

## How It Works

1. **Input the Message**: Users enter the suspicious message they received into the input field.
2. **Fraud Detection**: The app checks for keywords and common fraud tactics. If the message seems suspicious, the chatbot starts a conversation.
3. **Follow-Up Questions**: The chatbot asks questions to help the user understand the risks, simulating the kind of guidance a concerned family member might provide.
4. **Final Warnings**: The chatbot reminds the user not to take any immediate action, like clicking links or sharing personal information, and suggests blocking the sender if necessary.

## Requirements

- Python 3.8 or higher
- Gradio
- Transformers (Hugging Face)

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/financial-fraud-prevention-chatbot.git
