import json
import os
import streamlit as st

SESSION_FILE = "session_data.json"

def save_session():
    """Saves the current session state to a local JSON file."""
    try:
        data = {
            "messages": st.session_state.get('messages', []),
            "plan_generated": st.session_state.get('plan_generated', False),
            "generated_plan_text": st.session_state.get('generated_plan_text', ""),
            "selected_model": st.session_state.get('selected_model', "models/gemini-1.5-flash")
        }
        with open(SESSION_FILE, "w") as f:
            json.dump(data, f, indent=4)
        # print("Session saved.") # Debug
    except Exception as e:
        print(f"Error saving session: {e}")

def load_session():
    """Loads session state from the local JSON file if it exists."""
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, "r") as f:
                data = json.load(f)
            
            # Restore state
            if "messages" in data:
                st.session_state['messages'] = data["messages"]
            if "plan_generated" in data:
                st.session_state['plan_generated'] = data["plan_generated"]
            if "generated_plan_text" in data:
                st.session_state['generated_plan_text'] = data["generated_plan_text"]
            if "selected_model" in data:
                st.session_state['selected_model'] = data["selected_model"]
                
            # print("Session loaded.") # Debug
            return True
        except Exception as e:
            print(f"Error loading session: {e}")
            return False
    return False

def clear_session():
    """Clears the local session file and resets state variables."""
    if os.path.exists(SESSION_FILE):
        try:
            os.remove(SESSION_FILE)
        except Exception as e:
            print(f"Error deleting session file: {e}")
    
    # Reset in-memory state (partially, app rerun usually handles the rest or re-init)
    st.session_state['messages'] = []
    st.session_state['plan_generated'] = False
    st.session_state['generated_plan_text'] = ""
    # We might keep selected_model or reset it, user choice. Keeping it is usually better.
