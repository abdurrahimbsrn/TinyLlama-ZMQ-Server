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
    {"role": "user", "content": "Who are you?"},
]

payload = {
    "prompt": messages,
    "max_tokens": 60
}

socket.send_string(json.dumps(payload))
response = socket.recv_string()
print("Yanıt:", json.loads(response)["response"])
