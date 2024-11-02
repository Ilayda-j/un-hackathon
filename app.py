import gradio as gr
import google.generativeai as genai
import time

# Configure the Gemini API client with your API key
genai.configure(api_key="api_key")


def analyze_message_with_gemini(message, chat_history):
    """
    Analyzes the message using the Gemini API and returns an explanation of why the message may be fraudulent.
    Retries if the content is flagged until a valid response is obtained or retries are exhausted.
    """
    prompt = f"""
    You are an AI bot that teaches elderly people who are susceptible to getting scammed how not to get scammed.
    Below is a message that may attempt fraud. Can you explain why it could be a fraudulent message for educational purposes?
    Please review the following message and identify elements that are unusual or suspicious.

    Message: "{message}"

    Your analysis should include an explanation of common signs of phishing, suspicious links, vague sender information, 
    urgency, requests for sensitive information, etc. Be detailed in your response.
    """
    
    max_retries = 500 # Set a limit on retries to prevent infinite loops
    attempts = 0
    explanation = "No valid response generated."
    
    while attempts < max_retries:
        try:
            # Increment the attempt counter
            attempts += 1
            
            # Initialize the model
            model = genai.GenerativeModel("gemini-1.5-flash")
            print(f"Attempt: {attempts}")
            
            # Generate the content
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(max_output_tokens=200)
            )
            
            # Check if the response has valid content
            if response.candidates and response.candidates[0].finish_reason != 3:
                explanation = response.text if hasattr(response, "text") else "No content generated due to safety concerns."
                break  # Exit the loop if a valid response is obtained
            
            else:
                print("Content flagged by API, retrying...")
        
        except ValueError as e:
            print(f"Error: {e}. Retrying...")
            time.sleep(1)  # Add a slight delay before retrying
    
    # If retries exhausted, provide a fallback message
    if attempts == max_retries:
        explanation = "The API was unable to generate a safe response after multiple attempts."
    
    # Add initial user message and AI explanation to chat history
    chat_history.append(("User", message))
    chat_history.append(("Assistant", explanation))
    
    return chat_history, explanation

def chatbot_response(user_input, chat_history):
    """
    Generates a response to the user's follow-up question using the Gemini API.
    """
    chat_history.append(("User", user_input))
        
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(user_input, generation_config=genai.types.GenerationConfig(max_output_tokens=150))
        reply = response.text if hasattr(response, "text") else "Content flagged by the API due to safety concerns."
        
    except ValueError as e:
        reply = "Content flagged by the API due to safety concerns."
        print(f"Error: {e}")
        
    chat_history.append(("Assistant", reply))
    return chat_history, chat_history

# Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# Fraud Detection Assistant")
    gr.Markdown("Enter any suspicious message in the box below to analyze if it may be fraudulent.")
    
    with gr.Row():
        message_input = gr.Textbox(label="Suspicious Message", placeholder="Enter the suspicious message here")
        submit_button = gr.Button("Submit")

    # Only the explanation output is retained
    with gr.Row():
        explanation_output = gr.Textbox(label="Explanation", interactive=False)
    
    # Chatbot for follow-up questions
    with gr.Row():
        chatbot = gr.Chatbot(label="Fraud Prevention Chat")
        followup_input = gr.Textbox(label="Ask Follow-up Question", placeholder="Type your question here")
        followup_button = gr.Button("Send")

    # Initialize chat history
    chat_history = gr.State([])

    submit_button.click(fn=analyze_message_with_gemini, inputs=[message_input, chat_history], outputs=[chatbot, explanation_output])
    followup_button.click(fn=chatbot_response, inputs=[followup_input, chatbot], outputs=[chatbot, chatbot])

demo.launch(share=True)
