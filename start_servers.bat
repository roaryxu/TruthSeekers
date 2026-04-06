@echo off
echo Starting the Truth-Seeking Pod Servers...

echo Starting Debater (GPU-Accelerated) on port 8080...
start "Debater Server" cmd /k ".\llama_cpp\llama-server.exe --model "C:\LLMs\google_gemma-3-4b-it-Q4_K_M.gguf" -c 24576 --n-gpu-layers 99 --port 8080"

echo Starting Referee (GPU-Accelerated) on port 8081...
start "Referee Server" cmd /k ".\llama_cpp\llama-server.exe --model "C:\LLMs\Qwen3.5-9B-UD-Q4_K_XL.gguf" -c 24576 --n-gpu-layers 99 --reasoning off --port 8081"

echo Starting Streamlit UI...
start "Streamlit UI" cmd /k "streamlit run app.py"

echo All servers are starting in separate windows.
pause
