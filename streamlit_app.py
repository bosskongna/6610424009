import streamlit as st
import google.generativeai as genai
import numpy as np

st.title("ยินดีต้อนรับเข้าสู่ มูเตลู's world 🔮")
# Capture Gemini API Key
gemini_api_key = st.text_input("Gemini API Key: ", placeholder="Type your API Key here...", type="password")
 
# Initialize the Gemini Model
if gemini_api_key:
    try:
        # Configure Gemini with the provided API Key
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel("gemini-pro")
        st.success("Gemini API Key successfully configured.")
    except Exception as e:
        st.error(f"An error occurred while setting up the Gemini model: {e}")


# Initialize session state for storing chat history and prompt history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # Initialize with an empty list
    
if "prompt_chain" not in st.session_state:
    st.session_state.prompt_chain = """I am a professional fortune teller in Thailand. I will begin by asking the user to choose from the following options and without asking personal information:

เพื่อดูดวงรายวัน (Daily Tarot Reading): I will randomly select 3 Tarot cards to predict what will happen today.
เพื่อถามตอบ 1 เรื่อง (ใช่/ไม่ใช่, ได้ไม่ได้) (Yes/No Question): The user can ask a specific yes/no question. I will then draw a random card to answer the question. If the card drawn is one of the following Major Arcana cards—The Magician, The Empress, The Emperor, The Strength, The Star, The Moon, The Sun, or The World—the possibility of the event happening is 100%.
เพื่อดูดวงรายเดือน (Monthly Tarot Reading): I will perform an in-depth Tarot reading for the month using the Celtic Cross spread. For this reading, I will draw 10 Tarot cards and mix thier meaing. 
Once the user makes their selection, I will interpret the Tarot cards based on their choice and provide detailed responses in Thai."""
# Initialize session state for storing chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [] # Initialize with an empty list

# Display previous chat history using st.chat_message (if available)
for role, message in st.session_state.chat_history:
    st.chat_message(role).markdown(message)
 
# st.write("วันนี้ มูเรื่องอะไรดี ?")
# Capture user input and generate bot response
if user_input := st.chat_input("Type your message here..."):
    # Store and display user message
    st.session_state.chat_history.append(("user", user_input))
    st.chat_message("user").markdown(user_input)
   
    # Append the new question to the prompt chain
    st.session_state.prompt_chain += f"\n{user_input}"
   
    # Combine the predefined prompt chain with the current user input
    full_input = st.session_state.prompt_chain
   
    # Use Gemini AI to generate a bot response
    if model:
        try:
            response = model.generate_content(full_input)
            bot_response = response.text
           
            # Append bot response to the chat history and update the prompt chain
            st.session_state.chat_history.append(("assistant", bot_response))
            st.chat_message("assistant").markdown(bot_response)
           
            # Update the prompt chain with the bot's response
            st.session_state.prompt_chain += f"\nAssistant: {bot_response}"
        except Exception as e:
            st.error(f"An error occurred while generating the response: {e}")
 
