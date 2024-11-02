import gradio as gr
from transformers import pipeline

# Load a pre-trained model for classification (for simplicity, we use a general classifier here)
classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

def analyze_message(message):
    """
    Analyzes the message and returns an assessment of its fraudulence with an explanation.
    """
    # Placeholder model prediction (replace this with a custom fraud detection model)
    result = classifier(message)[0]
    label = result['label']
    
    # Crafting an analysis response based on model prediction
    if label == "LABEL_1":  # Assuming LABEL_1 represents fraud
        explanation = (
            "This message is likely fraudulent. Common red flags include a sense of urgency, suspicious links, "
            "vague sender information, generic greetings, and requests for sensitive information. "
            "Please avoid clicking on any links or sharing personal information."
        )
        fraud_status = "Fraudulent"
    else:
        explanation = (
            "This message does not display typical signs of fraud. However, always be cautious with unknown senders, "
            "unsolicited links, and requests for sensitive information."
        )
        fraud_status = "Not Fraudulent"
    
    return fraud_status, explanation

def chatbot_response(user_input, chat_history):
    """
    Simulates a chatbot response based on user follow-up questions.
    """
    # Append user's question to the chat history
    chat_history.append(("User", user_input))
    
    # Placeholder response (replace with actual model for a more sophisticated response)
    response = "I'm here to help you understand potential fraud risks. Feel free to ask any questions."
    chat_history.append(("Assistant", response))
    
    return chat_history, chat_history

# Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# Fraud Detection Assistant")
    gr.Markdown("Enter any suspicious message in the box below to analyze if it may be fraudulent.")
    
    # User input for suspicious message
    with gr.Row():
        message_input = gr.Textbox(label="Suspicious Message", placeholder="Enter the suspicious message here")
        submit_button = gr.Button("Submit")

    # Output for fraud analysis
    with gr.Row():
        fraud_status_output = gr.Textbox(label="Fraud Status", interactive=False)
        explanation_output = gr.Textbox(label="Explanation", interactive=False)
    
    # Chatbot for follow-up questions
    with gr.Row():
        chatbot = gr.Chatbot(label="Fraud Prevention Chat")
        followup_input = gr.Textbox(label="Ask Follow-up Question", placeholder="Type your question here")
        followup_button = gr.Button("Send")

    # Set up actions for submit button and follow-up button
    submit_button.click(fn=analyze_message, inputs=message_input, outputs=[fraud_status_output, explanation_output])
    followup_button.click(fn=chatbot_response, inputs=[followup_input, chatbot], outputs=[chatbot, chatbot])

demo.launch(share=True)
