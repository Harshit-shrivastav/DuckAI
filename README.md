# 🤖 Duck AI API

Welcome to the **Duck AI API** repository! This project provides a simple interface to interact with an AI assistant. Below, you'll find examples of how to use the API for different scenarios, including simple responses, assistant responses without history, and assistant responses with history tracking. Additionally, you'll learn how to deploy this API on your own server.

---

## 🌟 Features

- **Simple Response**: Get quick responses from the AI assistant.
- **Assistant Response Without History**: Interact with the assistant without maintaining conversation history.
- **Assistant Response With History**: Maintain a conversation history for context-aware responses.

---

## 🚀 Quick Start

To get started, make sure you have Python installed and install the required dependencies:

```bash
pip install requests
```

---

## 📋 Code Examples

### 1. **Simple Response** 🛠️

This example demonstrates how to send a simple message to the AI assistant and get a response.

```python
import requests

BASE_URL = "https://api.h-s.site"

# Step 1: Get a token
token_response = requests.get(f"{BASE_URL}/v1/get-token")
if token_response.status_code == 200:
    token = token_response.json()["token"]
else:
    print("Error getting token:", token_response.text)
    exit()

# Step 2: Send a message to the chat completion API
payload = {
    "token": token,
    "model": "gpt-4o-mini",
    "message": [{"role": "user", "content": "Hello, how are you?"}],
    "stream": False
}

response = requests.post(f"{BASE_URL}/v1/chat/completions", json=payload)
print("Response:", response.text)
```

---

### 2. **Assistant Response Without History** 📤

This example shows how to get a response from the assistant without maintaining any conversation history.

```python
import requests
import sys

BASE_URL = "https://api.h-s.site"

def get_assistant_response(system_prompt, user_prompt):
    try:
        try:
            token_response = requests.get(f"{BASE_URL}/v1/get-token")
            token_response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error getting token: {e}")
            sys.exit(1)

        try:
            token = token_response.json()["token"]
        except KeyError:
            print("Error: 'token' key not found in the response.")
            sys.exit(1)
        except ValueError:
            print("Error: Invalid JSON response from the server.")
            sys.exit(1)

        payload = {
            "token": token,
            "model": "gpt-4o-mini",
            "message": [
                {"role": "user", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "stream": False
        }

        try:
            response = requests.post(f"{BASE_URL}/v1/chat/completions", json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error sending request to chat completions: {e}")
            sys.exit(1)

        try:
            response_data = response.json()
            content = response_data["choice"][0]["message"]["content"]
            return content
        except KeyError as e:
            print(f"Error: Missing expected key in the response - {e}")
            sys.exit(1)
        except IndexError:
            print("Error: No choices found in the response.")
            sys.exit(1)
        except ValueError:
            print("Error: Invalid JSON response from the server.")
            sys.exit(1)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

system_prompt = "You are a helpful assistant!"
user_prompt = "Can you tell me a joke?"
response_content = get_assistant_response(system_prompt, user_prompt)
print("Assistant Response:", response_content)
```

---

### 3. **Assistant Response With History Record** 📚

This example demonstrates how to maintain a conversation history with the assistant, allowing for context-aware responses.

```python
import requests
import sys
from collections import deque

BASE_URL = "https://api.h-s.site"

# Initialize a deque to store the last 10 conversations
conversation_history = deque(maxlen=10)

def get_assistant_response(system_prompt, user_prompt, record_history=True):
    try:
        # If recording history is enabled, add the current user prompt to the history
        if record_history:
            conversation_history.append({"role": "user", "content": user_prompt})

        try:
            token_response = requests.get(f"{BASE_URL}/v1/get-token")
            token_response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error getting token: {e}")
            sys.exit(1)

        try:
            token = token_response.json()["token"]
        except KeyError:
            print("Error: 'token' key not found in the response.")
            sys.exit(1)
        except ValueError:
            print("Error: Invalid JSON response from the server.")
            sys.exit(1)

        # Prepare the payload with the system prompt, user prompt, and conversation history
        payload = {
            "token": token,
            "model": "gpt-4o-mini",
            "message": [
                {"role": "user", "content": system_prompt},
                *([*conversation_history] if record_history else []),
                {"role": "user", "content": user_prompt}
            ],
            "stream": False
        }

        try:
            response = requests.post(f"{BASE_URL}/v1/chat/completions", json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error sending request to chat completions: {e}")
            sys.exit(1)

        try:
            response_data = response.json()
            content = response_data["choice"][0]["message"]["content"]
            # If recording history is enabled, add the assistant's response to the history
            if record_history:
                conversation_history.append({"role": "assistant", "content": content})
            return content
        except KeyError as e:
            print(f"Error: Missing expected key in the response - {e}")
            sys.exit(1)
        except IndexError:
            print("Error: No choices found in the response.")
            sys.exit(1)
        except ValueError:
            print("Error: Invalid JSON response from the server.")
            sys.exit(1)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

system_prompt = "You are a helpful assistant!"
user_prompt = "Tell me a joke."
response_content = get_assistant_response(system_prompt, user_prompt, record_history=True)
print("Assistant Response:", response_content)
```

---

## 🛠️ Deployment Steps

Follow these steps to deploy the API on your own server:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Harshit-shrivastav/DuckAI
   ```

2. **Navigate to the Project Directory**:
   ```bash
   cd DuckAI
   ```

3. **Install the Required Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Main Script**:
   ```bash
   python3 -m main
   ```

5. **Access the API**:
   Once the server is running, you can access the API at `http://localhost:5000` (or the port you configured).

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Feel free to explore, contribute, and make the most out of this AI API! 🚀

---
