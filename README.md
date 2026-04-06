# Truth-Seeking Pod

![TruthSeekers](https://github.com/user-attachments/assets/8322563e-2504-4f01-b208-785fba41db75)

**Truth-Seeking Pod** is an open-source, local-first Streamlit application designed to run two large language models (LLMs) concurrently in a structured debate format. By leveraging `llama.cpp`, the application orchestrates a continuous interaction between a **Debater** model and a **Referee** model, facilitating adversarial debate and rigorous fact-checking entirely on your local hardware.

## 🌟 Overview

The Truth-Seeking Pod creates an environment where an AI Debater proposes arguments or answers, and an AI Referee critiques, challenges, and validates those claims. This adversarial interaction is exposed through a clean, interactive Streamlit frontend. It relies on local GGUF models running via `llama.cpp` to ensure complete data privacy and local execution.

## ✨ Features

- **Hardware Isolation**: Runs multiple local GGUF models concurrently on isolated or shared hardware resources without interference.
- **Reasoning Token Parsing**: Intelligently extracts and formats `<think>` reasoning tokens from the models, allowing users to inspect the internal logic and chain-of-thought of both the Debater and Referee.
- **Persistent System Prompts**: Easily customizable behavior via persistent system prompt text files located in the `prompts/` directory (`debater_system_prompt.txt` and `referee_system_prompt.txt`).
- **One-Click Execution**: Includes convenient `start_servers.bat` and `kill_servers.bat` scripts for seamless background management of the local `llama.cpp` servers.

## 🚀 Setup Instructions

### Prerequisites
- Windows 10/11 (for the included `.bat` scripts)
- Python 3.8+
- Hardware capable of running large GGUF models (GPU acceleration recommended but not required) - *demo was filmed on 6GB VRAM 3060ti*

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/TruthSeekers.git
   cd TruthSeekers
   ```

2. **Install Python Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download models and llama.cpp:**
   Use the provided Python script to download the necessary llama.cpp into the designated directory.
   ```bash
   python download_llama.py
   ```

### Running the Application

1. **Start the Local LLM Servers and Streamlit UI:**
   Run the batch script to initialise the `llama.cpp` servers for both the Debater and Referee models in the background, plus the Streamlit UI.
   ```cmd
   start_servers.bat
   ```

2. **Use in your browser:**
   The batch script will open the Streamlit UI in your default browser, otherwise open http://localhost:8501. *Confer with your truth-seeking pod!*

3. **Stop the Servers:**
   When finished, ensure all background server processes are terminated cleanly:
   ```cmd
   kill_servers.bat
   ```

## 📚 Annie Duke's Truth-Seeking Pod

The convergence of decision science, behavioral psychology, and computational linguistics has facilitated a transformative shift in how intellectual inquiry is conducted within digital environments. At the center of this evolution is the "Truth-Seeking Pod," a concept derived from Annie Duke’s seminal work on decision-making under uncertainty, which seeks to mitigate the pervasive human tendency toward cognitive bias and "resulting". I personally loved reading Duke's *Thinking in Bets*, and thought this could be a useful application of local-hosted LLMs for private, offline truth-seeking.

### Lerner and Tetlock: Process vs. Outcome Accountability
The psychological mechanism that drives the pod’s efficacy is "process accountability," a concept advanced by Lerner and Tetlock. Their research demonstrates that when individuals are held accountable for the outcome of their decisions, they tend to engage in "confirmatory thought"—a reactive state where the mind searches for evidence to rationalisse a pre-existing conclusion. Conversely, "process accountability"—where individuals must justify the steps of their reasoning to an audience with unknown views—triggers "exploratory thought".

### Haidt and the Necessity of Viewpoint Diversity
Jonathan Haidt’s work on Moral Foundations Theory (MFT) and viewpoint diversity provides the final pillar of the pod’s architecture. Haidt posits that moral and intellectual judgments are driven by intuitive "foundations"—Care, Fairness, Loyalty, Authority, and Purity—and that reasoning often serves as a "post-hoc" lawyer for these intuitions. Without intentional diversity, groups become "echo chambers" where confirmation bias is socially rewarded.

### The Pod Agreement: Establishing the Charter
For a Truth-Seeking Pod to be stable, the User must explicitly modify the standard social contract. This is achieved through a "Pod Agreement" that is pasted into the chat to prime both models toward adversarial accuracy.
1. Accuracy over Harmony: The goal is not to be helpful or agreeable. The goal is to calibrate our beliefs to reality.
2. No Resulting: We will not judge ideas by their hypothetical outcomes, only by the quality of the reasoning and the acknowledgment of luck.
3. Radical Transparency: I (the User) grant the Skeptic full permission to be intellectually aggressive. I grant the Referee full permission to penalize my logic.
4. CUDOS Norms: We adhere to Communalism (shared knowledge), Universality (impersonal criteria), Disinterestedness (no personal stake), and Organised Skepticism (suspension of judgment).
5. Quantified Beliefs: No assertion will be made without a confidence score (0-10).
6. The Winner: The 'winner' of this session is the one who most successfully updates their beliefs based on the counter-evidence provided."

## 🤝 Contributing
Contributions and comments are welcome! Please feel free to submit a Pull Request.

## 📜 License
[MIT License](LICENSE)
