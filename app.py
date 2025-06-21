import streamlit as st
import requests
import json
import os
from datetime import datetime

# Configuration
API_URL = "http://localhost:1234/api/prompt"
HISTORY_FILE = "history.json"

# Page configuration
st.set_page_config(
    page_title="Chatbot Interface",
    page_icon="💬",
    layout="wide",
)

# Add custom CSS for better styling
st.markdown("""
<style>
    /* Message containers */
    .user-message {
        background-color: #e6f7ff;
        border-radius: 15px;
        padding: 10px 15px;
        margin: 5px 0;
        border-top-right-radius: 3px;
        text-align: right;
        max-width: 80%;
        margin-left: auto;
    }
    
    .assistant-message {
        background-color: #f0f2f6;
        border-radius: 15px;
        padding: 10px 15px;
        margin: 5px 0;
        border-top-left-radius: 3px;
        max-width: 80%;
        margin-right: auto;
    }
    
    /* Chat container */
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 10px;
        padding: 10px;
    }
    
    /* Sidebar styling */
    .history-item {
        border-radius: 5px;
        padding: 8px;
        margin: 5px 0;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    
    .history-item:hover {
        background-color: #f0f2f6;
    }
    
    /* Button styling */
    .stButton>button {
        border-radius: 20px;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Make text areas look better */
    .stTextArea textarea {
        border-radius: 10px;
    }
    
    /* Header styling */
    h1, h2, h3 {
        color: #0066cc;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Track current conversation
if "current_conversation" not in st.session_state:
    st.session_state.current_conversation = []

# Track if we're in a continuous chat
if "is_continuous_chat" not in st.session_state:
    st.session_state.is_continuous_chat = False

def load_history_from_file():
    """Load chat history from JSON file if it exists"""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Error loading history: {e}")
    return []

def save_history_to_file(history):
    """Save chat history to JSON file"""
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.error(f"Error saving history: {e}")

def send_prompt_to_api(prompt, conversation_history=None):
    """Send prompt to API and return response
    
    Args:
        prompt (str): The current user prompt
        conversation_history (list, optional): List of previous messages and responses
    """
    try:
        headers = {"Content-Type": "application/json"}
        
        # If we have conversation history, format it for the API
        if conversation_history:
            # Format the conversation history as a single string
            formatted_history = ""
            for item in conversation_history:
                formatted_history += f"User: {item['prompt']}\n"
                formatted_history += f"Assistant: {item['response']}\n\n"
            
            # Add the current prompt
            full_prompt = f"{formatted_history}User: {prompt}"
            
            # Log the full prompt for debugging (optional)
            # st.write("Debug - Full prompt being sent:")
            # st.code(full_prompt)
            
            payload = {"prompt": full_prompt}
        else:
            # Just send the current prompt if no history
            payload = {"prompt": prompt}
        
        with st.spinner("Waiting for response..."):
            response = requests.post(
                API_URL, 
                data=json.dumps(payload), 
                headers=headers,
                timeout=30  # 30 seconds timeout
            )
        
        if response.status_code == 200:
            return response.json().get("resposta", "No response content"), None
        else:
            return None, f"Error: API returned status code {response.status_code}"
    
    except requests.exceptions.ConnectionError:
        return None, "Error: Could not connect to API. Is the API server running at localhost:1234?"
    except requests.exceptions.Timeout:
        return None, "Error: Request timed out. The API server might be overloaded."
    except Exception as e:
        return None, f"Error: {str(e)}"

def add_to_history(prompt, response, timestamp=None):
    """Add a new conversation to history"""
    if timestamp is None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    conversation = {
        "id": len(st.session_state.chat_history) + 1,
        "timestamp": timestamp,
        "prompt": prompt,
        "response": response,
        "rating": None  # Will be updated when user rates
    }
    
    st.session_state.chat_history.append(conversation)
    save_history_to_file(st.session_state.chat_history)
    return conversation["id"]

def rate_response(conversation_id, rating):
    """Rate a response (positive/negative)"""
    for i, conv in enumerate(st.session_state.chat_history):
        if conv["id"] == conversation_id:
            st.session_state.chat_history[i]["rating"] = rating
            save_history_to_file(st.session_state.chat_history)
            return True
    return False

# Load history when app starts
if not st.session_state.chat_history:
    st.session_state.chat_history = load_history_from_file()

# Main layout
st.title("Chatbot Interface")

# Sidebar with history
with st.sidebar:
    # Add header with clear button in the same row
    col1, col2 = st.columns([3, 1])
    with col1:
        st.header("Chat History")
    with col2:
        if st.session_state.chat_history and st.button("🗑️ Clear", help="Clear all chat history"):
            if "confirm_clear" not in st.session_state:
                st.session_state.confirm_clear = True
                st.warning("Are you sure you want to clear all chat history? This cannot be undone.")
            else:
                # Clear history
                st.session_state.chat_history = []
                save_history_to_file([])  # Save empty history to file
                st.session_state.current_conversation = []
                st.session_state.new_response = None
                st.session_state.new_conv_id = None
                if "confirm_clear" in st.session_state:
                    del st.session_state.confirm_clear
                st.success("Chat history cleared!")
                st.experimental_rerun()
    
    # Cancel button appears if confirmation is pending
    if "confirm_clear" in st.session_state and st.session_state.confirm_clear:
        if st.button("Cancel"):
            del st.session_state.confirm_clear
            st.experimental_rerun()
    
    if not st.session_state.chat_history:
        st.info("No chat history yet. Start a conversation!")
    else:
        # Add a search box for history
        search_term = st.text_input("Search history", "", placeholder="Type to search...")
        
        # Group conversations by date
        from itertools import groupby
        from datetime import datetime
        
        # Extract date from timestamp
        def get_date(conv):
            try:
                dt = datetime.strptime(conv['timestamp'], "%Y-%m-%d %H:%M:%S")
                return dt.strftime("%Y-%m-%d")
            except:
                return "Unknown date"
        
        # Sort by date first
        sorted_history = sorted(st.session_state.chat_history, 
                               key=lambda x: x['timestamp'] if 'timestamp' in x else "", 
                               reverse=True)
        
        # Filter by search term if provided
        if search_term:
            sorted_history = [
                conv for conv in sorted_history 
                if search_term.lower() in conv['prompt'].lower() or 
                   search_term.lower() in conv['response'].lower()
            ]
        
        # Group by date
        for date, group in groupby(sorted_history, key=get_date):
            st.markdown(f"**{date}**")
            
            # Display conversations for this date
            for conv in group:
                # Create a cleaner preview
                preview = conv['prompt'][:40] + "..." if len(conv['prompt']) > 40 else conv['prompt']
                
                # Add rating indicator if rated
                rating_indicator = ""
                if conv.get('rating') == "positive":
                    rating_indicator = " 👍"
                elif conv.get('rating') == "negative":
                    rating_indicator = " 👎"
                
                # Create a clickable element with better styling
                if st.button(
                    f"{conv['timestamp'][11:16]} • {preview}{rating_indicator}", 
                    key=f"history_{conv['id']}",
                    help=f"Click to view this conversation"
                ):
                    # When clicked, set this as the active conversation
                    st.session_state.active_conversation = conv["id"]
                    st.experimental_rerun()

# Check if there's an active conversation to display
if "active_conversation" in st.session_state:
    # Find the active conversation
    active_conv = None
    for conv in st.session_state.chat_history:
        if conv["id"] == st.session_state.active_conversation:
            active_conv = conv
            break
    
    if active_conv:
        st.subheader("From History:")
        
        # Display conversation in chat-like format
        with st.container():
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            
            # User message
            st.markdown(f'<div class="user-message">{active_conv["prompt"]}</div>', unsafe_allow_html=True)
            
            # Assistant response
            st.markdown(f'<div class="assistant-message">{active_conv["response"]}</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Action buttons in a cleaner layout
            col1, col2, col3, col4 = st.columns([1, 1, 2, 3])
            
            with col1:
                if st.button("👍", key=f"up_{active_conv['id']}"):
                    rate_response(active_conv["id"], "positive")
                    st.success("Rated positive!")
                    st.experimental_rerun()
            
            with col2:
                if st.button("👎", key=f"down_{active_conv['id']}"):
                    rate_response(active_conv["id"], "negative")
                    st.error("Rated negative!")
                    st.experimental_rerun()
            
            with col3:
                if st.button("Copy", key=f"copy_{active_conv['id']}"):
                    st.code(active_conv["response"])
                    st.success("Copied!")
        
        # Show current rating with better styling
        if active_conv["rating"]:
            if active_conv["rating"] == "positive":
                st.markdown("**Rating:** 👍 Positive")
            else:
                st.markdown("**Rating:** 👎 Negative")
        
        # Buttons for navigation
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Start New Chat"):
                del st.session_state.active_conversation
                st.experimental_rerun()
        
        with col2:
            if st.button("Continue This Conversation"):
                # Set up the current conversation with this history item
                for conv in st.session_state.chat_history:
                    if conv["id"] == st.session_state.active_conversation:
                        st.session_state.current_conversation = [{
                            "prompt": conv["prompt"],
                            "response": conv["response"],
                            "timestamp": conv["timestamp"]
                        }]
                        st.session_state.is_continuous_chat = True
                        break
                
                del st.session_state.active_conversation
                st.experimental_rerun()
        
        st.markdown("---")

# Chat form (new or continuous)
if "active_conversation" not in st.session_state:
    # Display current conversation if in continuous mode
    if st.session_state.is_continuous_chat and st.session_state.current_conversation:
        st.subheader("Current Conversation")
        
        # Create a chat-like container
        chat_container = st.container()
        
        with chat_container:
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            
            # Display the conversation history
            for i, message in enumerate(st.session_state.current_conversation):
                # User message
                st.markdown(f'<div class="user-message">{message["prompt"]}</div>', unsafe_allow_html=True)
                
                # Assistant response
                st.markdown(f'<div class="assistant-message">{message["response"]}</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.subheader("New Chat")
    
    # Initialize session state for new response if not exists
    if "new_response" not in st.session_state:
        st.session_state.new_response = None
        st.session_state.new_conv_id = None
    
    # Create a cleaner chat interface
    chat_container = st.container()
    
    # Form for submitting the prompt
    with st.form(key="prompt_form", clear_on_submit=True):
        # Add a cleaner prompt input
        user_prompt = st.text_area("Type your message", 
                                  height=100, 
                                  placeholder="Ask me anything...",
                                  label_visibility="collapsed")
        
        # Add controls in columns for better layout
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Add a checkbox to enable/disable continuous chat with better label
            continuous_chat = st.checkbox("Remember conversation context", 
                                         value=st.session_state.is_continuous_chat,
                                         help="When enabled, the entire conversation history is sent to the API")
        
        with col2:
            # Better styled submit button
            submit_button = st.form_submit_button("Send Message")
        
        if submit_button and user_prompt:
            # Update continuous chat setting
            st.session_state.is_continuous_chat = continuous_chat
            
            # Send prompt to API with conversation history if in continuous mode
            if continuous_chat and st.session_state.current_conversation:
                response_text, error = send_prompt_to_api(user_prompt, st.session_state.current_conversation)
            else:
                response_text, error = send_prompt_to_api(user_prompt)
            
            if error:
                st.error(error)
            else:
                # Add to global history
                conv_id = add_to_history(user_prompt, response_text)
                
                # Add to current conversation if in continuous mode
                if continuous_chat:
                    new_exchange = {
                        "prompt": user_prompt,
                        "response": response_text,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    st.session_state.current_conversation.append(new_exchange)
                else:
                    # Reset current conversation if not in continuous mode
                    st.session_state.current_conversation = [{
                        "prompt": user_prompt,
                        "response": response_text,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }]
                
                # Store in session state for display outside the form
                st.session_state.new_response = response_text
                st.session_state.new_conv_id = conv_id
    
    # Display latest response and conversation in a chat-like interface
    with chat_container:
        # If we have a conversation, display it in a chat-like format
        if st.session_state.current_conversation:
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            
            for message in st.session_state.current_conversation:
                # User message
                st.markdown(f'<div class="user-message">{message["prompt"]}</div>', unsafe_allow_html=True)
                
                # Assistant response
                st.markdown(f'<div class="assistant-message">{message["response"]}</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Action buttons for the latest response
            if st.session_state.new_response:
                with st.container():
                    col1, col2, col3, col4 = st.columns([1, 1, 1, 4])
                    with col1:
                        if st.button("👍", key=f"up_new"):
                            rate_response(st.session_state.new_conv_id, "positive")
                            st.success("Rated positive!")
                            st.experimental_rerun()
                    
                    with col2:
                        if st.button("👎", key=f"down_new"):
                            rate_response(st.session_state.new_conv_id, "negative")
                            st.error("Rated negative!")
                            st.experimental_rerun()
                    
                    with col3:
                        if st.button("Copy", key="copy_new"):
                            st.code(st.session_state.new_response)
                            st.success("Copied!")
                            
                    with col4:
                        if st.button("New Chat", key="new_chat"):
                            st.session_state.current_conversation = []
                            st.session_state.new_response = None
                            st.session_state.new_conv_id = None
                            st.experimental_rerun()

# Footer with better styling
st.markdown("---")
footer_container = st.container()
with footer_container:
    cols = st.columns([3, 1])
    with cols[0]:
        st.markdown("<p style='color: #888; font-size: 0.8em;'>Chatbot Interface with History © 2023</p>", unsafe_allow_html=True)
    
    with cols[1]:
        # Health check for API with better styling
        try:
            health_response = requests.get("http://localhost:1234/health", timeout=2)
            if health_response.status_code == 200:
                st.markdown("<p style='color: #4CAF50; text-align: right;'>● API Online</p>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='color: #FFC107; text-align: right;'>● API Warning</p>", unsafe_allow_html=True)
        except:
            st.markdown("<p style='color: #F44336; text-align: right;'>● API Offline</p>", unsafe_allow_html=True)

# Also add API status to sidebar
try:
    health_response = requests.get("http://localhost:1234/health", timeout=2)
    if health_response.status_code == 200:
        st.sidebar.markdown("<p style='color: #4CAF50;'>● API Online</p>", unsafe_allow_html=True)
    else:
        st.sidebar.markdown("<p style='color: #FFC107;'>● API Warning</p>", unsafe_allow_html=True)
except:
    st.sidebar.markdown("<p style='color: #F44336;'>● API Offline</p>", unsafe_allow_html=True)