# 🧠 Chatbot-App

A lightweight chatbot application using an open-source **quantized** LLM: `Llama-3.2-1B-Instruct-IQ3_M.gguf`.  
It provides a **simple Streamlit-based web interface**, supports **local network access**, and saves **chat history in MongoDB**.

---

## 📸 GUI Preview

Authentication Screen | Chatbot Screen  
:-------------------------:|:-------------------------:
![Authentication](imgs/authentication.png) | ![ChatBot](imgs/chatbot.png)

---

## ✨ Features

- ✅ **Quantized LLM (GGUF format)**  
  Uses `Llama-3.2-1B-Instruct-IQ3_M.gguf` for generating conversational responses.

- 💬 **Streamlit Web Interface**  
  A clean and responsive chat interface in the browser.

- 💾 **Persistent Chat History**  
  MongoDB stores all chats and user authentication data.

- 🌐 **Local Network Access**  
  Access the app from any device on your local Wi-Fi.

---

## 📥 Prerequisites

1. **Model Download**

   Download the quantized GGUF model from Hugging Face:

   [Llama-3.2-1B-Instruct-IQ3_M.gguf](https://huggingface.co/bartowski/Llama-3.2-1B-Instruct-GGUF/blob/main/Llama-3.2-1B-Instruct-IQ3_M.gguf)

   Or run:

   ```bash
   wget https://huggingface.co/bartowski/Llama-3.2-1B-Instruct-GGUF/resolve/main/Llama-3.2-1B-Instruct-IQ3_M.gguf
   ```
    Place the downloaded file inside the `model/` directory.

2. **MongoDB Compass**
   Install [MongoDB Compass](https://www.mongodb.com/try/download/compass) to visually inspect stored users and chat data.

---

## 🚀 Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/muhammad-faizan-122/chatbot.git
   cd chatbot
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Running the App

To start the chatbot locally:

```bash
streamlit run app.py
```

After running, you’ll see:

```
Local URL:   http://localhost:8501
Network URL: http://192.168.x.x:8501
```

* Open the **Local URL** on the same machine.
* Open the **Network URL** from another device on the same Wi-Fi/LAN.

---

## 🌐 Access from Other Devices

To access the chatbot from other devices on your network:

```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

Then open in a browser:

```
http://<your-local-IP>:8501
```

**Example:**

```
http://192.168.0.101:8501
```

---

## 📧 Contact

If you find this useful or have feedback, feel free to [open an issue](https://github.com/muhammad-faizan-122/chatbot/issues) or reach out!

---

## 🪪 License

This project is open-source and available under the MIT License

---

