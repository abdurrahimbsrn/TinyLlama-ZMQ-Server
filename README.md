# TinyLlama-ZMQ-Server

A lightweight server application that serves the TinyLlama model in a Docker container with ZeroMQ interface.

![Docker](https://img.shields.io/badge/Docker-✓-blue?logo=docker)
![ZeroMQ](https://img.shields.io/badge/ZeroMQ-✓-green?logo=zeromq)
![TinyLlama](https://img.shields.io/badge/TinyLlama-1.1B-ff69b4)

## Features

- 🐳 Docker container support
- ⚡ High-performance messaging with ZeroMQ
- 🤖 TinyLlama-1.1B-Chat model integration
- 🔌 JSON-based API interface
- 📊 System resource optimization

## Installation

### 1. Run with Docker

```bash
docker build -t tinyllama-server .
docker run -p 5555:5555 --gpus all tinyllama-server
```

### 2. Manual Installation

```bash
git clone https://github.com/your-username/tinyllama-zmq-server.git
cd tinyllama-zmq-server
pip install -r requirements.txt
python server.py
```

## Usage

### Client Example (Python)

```python
import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant that provides concise and accurate answers.",
    },
    {
        "role": "user",
        "content": "Who are you?"
    }
]

payload = {
    "prompt": messages,
    "max_tokens": 60
}

socket.send_string(json.dumps(payload))
response = json.loads(socket.recv_string())
print(response["response"])
```

### API Format

**Request:**
```json
{
    "messages": [
        {"role": "system", "content": "System message"},
        {"role": "user", "content": "User question"}
    ],
    "max_tokens": 60
}
```

**Response:**
```json
{
    "response": "Model response",
    "tokens_used": 42,
    "status": "success"
}
```

## Configuration

Environment variables:

| Variable       | Default Value               | Description                  |
|----------------|-----------------------------|------------------------------|
| `MODEL_PATH`   | `TinyLlama/TinyLlama-1.1B-Chat-v1.0` | Model path          |
| `ZMQ_PORT`     | `5555`                      | ZeroMQ connection port       |
| `MAX_TOKENS`   | `100`                       | Maximum token count          |


## Contributing

1. Fork it (https://github.com/your-username/TinyLlama-ZMQ-Server/fork)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

## License

Apache License 2.0 - See [LICENSE](LICENSE) file

---

> **Note:** TinyLlama may sometimes produce inconsistent answers. Optimize your system prompt for more stable results.
