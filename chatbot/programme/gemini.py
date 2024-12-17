import google.generativeai as genai

def init_generative_model():
    """Initializes and configures the generative AI model."""
    genai.configure(api_key="AIzaSyDddmKRfs7-dnN7uZX1kSUmX3VuW7EhqxM")

    # Set up the model configuration
    generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }

    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
    ]

    # Create and return the generative model instance
    return genai.GenerativeModel(model_name="gemini-1.0-pro",
                                 generation_config=generation_config,
                                 safety_settings=safety_settings)

def chat_with_model(x):
    """Initiates a chat with the generative model."""
    model = init_generative_model()
    convo = model.start_chat(history=[])
    convo.send_message("dans une petite paragraphe ,"+x)
    return convo.last.text

if __name__ == "__main__":
    print(chat_with_model())
