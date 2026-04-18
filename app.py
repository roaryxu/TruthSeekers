import streamlit as st
from openai import OpenAI
import os

# Initialize OpenAI clients pointing to the local llama.cpp servers
debater_client = OpenAI(base_url="http://localhost:8080/v1", api_key="not-needed")
referee_client = OpenAI(base_url="http://localhost:8081/v1", api_key="not-needed")

st.set_page_config(page_title="Truth-Seeking Pod", page_icon="⚖️")

st.title("Truth-Seeking Pod")
st.markdown("Interact with the **Debater** 🗣️ and the **Referee** ⚖️.")

def load_prompt(filename, default_content):
    path = os.path.join("prompts", filename)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        os.makedirs("prompts", exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(default_content)
        return default_content

def save_prompt(filename, content):
    path = os.path.join("prompts", filename)
    os.makedirs("prompts", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# Sidebar settings
st.sidebar.image("logo.svg", use_container_width=True)
st.sidebar.title("Settings")
auto_referee = st.sidebar.checkbox("Auto-Referee Evaluation", value=True, help="If enabled, the Referee automatically evaluates after the Debater responds.")

if st.sidebar.button("Clear Chat History", use_container_width=True):
    st.session_state.messages = []
    st.rerun()

st.sidebar.subheader("System Prompts")
debater_default = "You are the Debater. Engage with the user's input, challenge their ideas, and present compelling arguments."
referee_default = "You are the Referee. Objectively evaluate the arguments presented by both the User and the Debater. Provide a fair, reasoned judgment based strictly on the logic and evidence presented in the conversation."

debater_prompt_text = load_prompt("debater_system_prompt.txt", debater_default)
referee_prompt_text = load_prompt("referee_system_prompt.txt", referee_default)

new_debater_prompt = st.sidebar.text_area("Debater Prompt", value=debater_prompt_text, height=150)
if new_debater_prompt != debater_prompt_text:
    save_prompt("debater_system_prompt.txt", new_debater_prompt)
    debater_prompt_text = new_debater_prompt

new_referee_prompt = st.sidebar.text_area("Referee Prompt", value=referee_prompt_text, height=150)
if new_referee_prompt != referee_prompt_text:
    save_prompt("referee_system_prompt.txt", new_referee_prompt)
    referee_prompt_text = new_referee_prompt

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    avatar = "👤" if message["role"] == "user" else "🗣️" if message["name"] == "Debater" else "⚖️"
    with st.chat_message(message["role"], avatar=avatar):
        if message.get("reasoning"):
            with st.expander("Thinking Process"):
                st.markdown(message["reasoning"])
        st.markdown(message.get("content", ""))

# Helper function to prepare messages for the API
def prepare_history(messages, current_agent):
    api_messages = []
    for msg in messages:
        # If the message is from the agent being prompted, treat as 'assistant'
        # Otherwise, treat as 'user' because it's an external input to them.
        role = "assistant" if msg["name"] == current_agent else "user"
        # Prefix the content so the models understand who is speaking in the transcript
        name_prefix = f"**{msg['name']}**: "
        formatted_content = f"{name_prefix}{msg.get('content', '')}"
        
        if api_messages and api_messages[-1]["role"] == role:
            api_messages[-1]["content"] += f"\n\n{formatted_content}"
        else:
            api_messages.append({"role": role, "content": formatted_content})
    return api_messages

# React to user input
if prompt := st.chat_input("Enter your argument or question..."):
    # Display user message in chat message container
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt, "name": "User"})

    # ---------- DEBATER TURN ----------
    with st.chat_message("assistant", avatar="🗣️"):
        expander_placeholder = st.empty()
        content_placeholder = st.empty()
        
        debater_response = ""
        debater_reasoning = ""
        
        # Prepare history for the Debater
        debater_messages = prepare_history(st.session_state.messages, "Debater")
        debater_messages.insert(0, {
            "role": "system", 
            "content": debater_prompt_text
        })
        
        try:
            responses = debater_client.chat.completions.create(
                model="debater", # Model name is ignored by llama.cpp but required by OpenAI client
                messages=debater_messages,
                stream=True,
            )
            for chunk in responses:
                delta = chunk.choices[0].delta
                content = delta.content or ""
                reasoning = getattr(delta, "reasoning_content", None) or ""
                
                if reasoning:
                    debater_reasoning += reasoning
                if content:
                    debater_response += content
                    
                if debater_reasoning:
                    with expander_placeholder.container():
                        with st.expander("Thinking Process", expanded=True):
                            st.markdown(debater_reasoning + "▌")
                if debater_response:
                    content_placeholder.markdown(debater_response + "▌")
            
            if debater_reasoning:
                with expander_placeholder.container():
                    with st.expander("Thinking Process"):
                        st.markdown(debater_reasoning)
            else:
                expander_placeholder.empty()
                
            if debater_response:
                content_placeholder.markdown(debater_response)
            else:
                content_placeholder.empty()
                
        except Exception as e:
            st.error(f"Error communicating with Debater (Ensure it's running on port 8080): {e}")
            debater_response = f"*Connection Error: {e}*"

    # Add Debater response to history
    st.session_state.messages.append({"role": "assistant", "content": debater_response, "reasoning": debater_reasoning, "name": "Debater"})

    # ---------- REFEREE TURN ----------
    if auto_referee and not debater_response.startswith("*Connection Error"):
        with st.chat_message("assistant", avatar="⚖️"):
            expander_placeholder = st.empty()
            content_placeholder = st.empty()
            
            referee_response = ""
            referee_reasoning = ""
            
            # Prepare history for the Referee, which now includes the Debater's latest response
            referee_messages = prepare_history(st.session_state.messages, "Referee")
            referee_messages.insert(0, {
                "role": "system", 
                "content": referee_prompt_text
            })
            
            try:
                responses = referee_client.chat.completions.create(
                    model="referee",
                    messages=referee_messages,
                    stream=True,
                )
                for chunk in responses:
                    delta = chunk.choices[0].delta
                    content = delta.content or ""
                    reasoning = getattr(delta, "reasoning_content", None) or ""
                    
                    if reasoning:
                        referee_reasoning += reasoning
                    if content:
                        referee_response += content
                        
                    if referee_reasoning:
                        with expander_placeholder.container():
                            with st.expander("Thinking Process", expanded=True):
                                st.markdown(referee_reasoning + "▌")
                    if referee_response:
                        content_placeholder.markdown(referee_response + "▌")
                        
                if referee_reasoning:
                    with expander_placeholder.container():
                        with st.expander("Thinking Process"):
                            st.markdown(referee_reasoning)
                else:
                    expander_placeholder.empty()
                    
                if referee_response:
                    content_placeholder.markdown(referee_response)
                else:
                    content_placeholder.empty()
                    
            except Exception as e:
                st.error(f"Error communicating with Referee (Ensure it's running on port 8081): {e}")
                referee_response = f"*Connection Error: {e}*"

        # Add Referee response to history
        st.session_state.messages.append({"role": "assistant", "content": referee_response, "reasoning": referee_reasoning, "name": "Referee"})
