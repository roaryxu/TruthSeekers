# Truth-Seeking Pod: System Architecture

## Overview
The "Truth-Seeking Pod" is a multi-agent chat application where a human user interacts with two distinct AI models concurrently:
1. **The Debater:** A smaller, CPU-bound model.
2. **The Referee:** A larger, GPU-bound model.

This document outlines the technical architecture, including the inference engine, UI framework, and multi-agent communication flow.

## 1. Inference Engine Setup
To ensure true concurrent execution without running into Python Global Interpreter Lock (GIL) limitations or complex resource sharing constraints, we will use the native **`llama.cpp` HTTP server** binaries (`llama-server.exe` on Windows). This provides OpenAI-compatible API endpoints for both models, with strict hardware isolation.

### The Debater (CPU-Exclusive)
- **Model:** `debater-model-placeholder.gguf` (Tiny model)
- **Configuration:** We strictly limit the model to the CPU by setting the number of GPU layers to zero.
- **Execution Command:**
  ```cmd
  llama-server.exe --model debater-model-placeholder.gguf --n-gpu-layers 0 --port 8080
  ```

### The Referee (GPU-Accelerated)
- **Model:** `referee-model-placeholder.gguf` (Larger model)
- **Configuration:** We offload layers to the GPU by setting a high number of GPU layers.
- **Execution Command:**
  ```cmd
  llama-server.exe --model referee-model-placeholder.gguf --n-gpu-layers 99 --port 8081
  ```

*Alternative:* You can achieve the exact same isolation using `llama-cpp-python`'s web server module by launching two separate Python processes with different `--n_gpu_layers` flags and ports.

## 2. UI Stack
The user interface will be built using **Streamlit**, which offers excellent built-in chat components (`st.chat_message`, `st.chat_input`) and robust session state management.

- **Frontend:** Streamlit (`app.py`).
- **Client Library:** The official `openai` Python library. Since `llama-server` provides an OpenAI-compatible API, we can easily create two separate client instances pointing to our local ports (8080 and 8081).
- **State Management:** `st.session_state` will store the unified conversation history, allowing seamless rendering of messages from the User, Debater, and Referee in a single chronological thread.

## 3. Communication Flow
The multi-agent interaction is orchestrated by the Streamlit backend logic in a single chronological chat window.

1. **User Input:** The user types a message in the chat input.
2. **Display & Log:** The user's message is added to `st.session_state.messages` and rendered on the screen.
3. **Debater Turn:**
   - Streamlit sends the conversation history to the **Debater API** (`localhost:8080`).
   - The Debater streams or returns its response.
   - The UI renders the Debater's response (using a specific avatar, e.g., 🗣️).
   - The response is appended to the session state.
4. **Referee Turn:**
   - Streamlit compiles the updated context (User message + Debater's argument) and sends it to the **Referee API** (`localhost:8081`).
   - The Referee streams or returns its evaluation/judgment.
   - The UI renders the Referee's response (using a distinct avatar, e.g., ⚖️).
   - The response is appended to the session state.
5. **Loop:** The system waits for the next User input, repeating the cycle.

*Optional UI Feature:* The Streamlit sidebar can include toggles to let the user decide if the Referee should evaluate *every* turn automatically, or only when explicitly requested.
