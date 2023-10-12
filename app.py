import streamlit as st
import random
import time
import backup as t

if 'chat_history' not in st.session_state:
	st.session_state.chat_history = []

if 'ctr' not in st.session_state:
	st.session_state.ctr = 0



st.title(":violet[IGEM] ChatBot ")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("How can I assist you today?"):

    with st.spinner('Compiling Answer...'):
        #Getting answer
        answer, user_message, bot_message = t.get_answer(prompt, st.session_state.chat_history)
        # print(f"temp_chat: {temp_chat}")
        st.session_state.chat_history.append(user_message)
        st.session_state.chat_history.append(bot_message)

        print(f"chat_history_st: {st.session_state.chat_history}")
        temp_ctr = st.session_state.ctr
        if(temp_ctr > 2):
            st.session_state.chat_history.pop(0)
            st.session_state.chat_history.pop(0)
        st.session_state.ctr = st.session_state.ctr + 1
        time.sleep(5)

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)


    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        assistant_response = answer
        
        
        # Simulate stream of response with milliseconds delay
        for chunk in assistant_response.split():
            full_response += chunk + " "
            # time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})