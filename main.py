# -*- coding: utf-8 -*-
"""
Model Server for TinyLlama using ZeroMQ and Transformers
This script sets up a ZeroMQ server that listens for incoming requests,
loads a TinyLlama model, and generates responses based on the received prompts.
""" 

import os
import time
import zmq
import torch
import logging
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import json
import re

# ----------------------------
# Configurations
# ----------------------------

MODEL_PATH = os.getenv("MODEL_PATH", "/models/tinyllama")
PORT = int(os.getenv("ZMQ_PORT", 5555))
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MAX_TOKENS = int(os.getenv("MAX_TOKENS", 100))

# ----------------------------
# Logging Settings
# ----------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger("ModelServer")

# ----------------------------
# Model Loading
# ----------------------------

def load_model(path: str):
    while True:
        try:
            logger.info(f"Model loading: {path}")
            tokenizer = AutoTokenizer.from_pretrained(path)
            model = AutoModelForCausalLM.from_pretrained(
                path,
                torch_dtype=torch.float16 if DEVICE == "cuda" else torch.float32,
                device_map="auto"
            )
            logger.info("Model loading successful.")
            return tokenizer, model
        except Exception as e:
            logger.error(f"Model not loaded: {e}")
            logger.info("🔄 Will try again in 5 seconds ...")
            time.sleep(5)

tokenizer, model = load_model(MODEL_PATH)

# ----------------------------
# ZeroMQ Listening
# ----------------------------

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind(f"tcp://*:{PORT}")
logger.info(f"ZeroMQ listening on {PORT} ...")

# ----------------------------
# Service Loop
# ----------------------------

while True:
    try:
        raw_message = socket.recv_string()
        logger.info(f"[Input] {raw_message}")

        # JSON parse and extract messages
        try:
            payload = json.loads(raw_message)
            messages = payload["prompt"]
            max_tokens = int(payload.get("max_tokens", MAX_TOKENS))

            # Special chat template for TinyLlama
            prompt = ""
            for msg in messages:
                if msg["role"] == "system":
                    prompt += f"<|system|>\n{msg['content']}</s>\n"
                elif msg["role"] == "user":
                    prompt += f"<|user|>\n{msg['content']}</s>\n"
            prompt += "<|assistant|>\n"

        except Exception as e:
            error = f"[ERROR] JSON not parse: {e}"
            logger.error(error)
            socket.send_string(json.dumps({"error": error}))
            continue


        # Tokenize the propt
        inputs = tokenizer(prompt, return_tensors="pt").to(DEVICE)

        # Generate response using the model
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            do_sample=True,   # Random sampling
            temperature=0.7,  # Creativity
            top_p=0.95,       # Nucleus sampling
            top_k=50,         # Word diversity
        )

        # Clean and decode the response
        full_response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        response = full_response.split("<|assistant|>")[-1].strip()

        response = re.sub(r'(\b\w+\b)(?:\s+\1)+', r'\1', response)  # Basit tekrarları siler
        
        response_cleaned = re.sub(r"<[^>]+>", "", response)  # <s>, </s>, vs.
        response_cleaned = response_cleaned.replace("[INST]", "").replace("[/INST]", "").strip()

        logger.info(f"[ANSWER] {response[:100]}...")


        # Send the response back
        response_payload = {
            "response": response_cleaned,
            "tokens_used": len(outputs[0])
        }
        socket.send_string(json.dumps(response_payload))
        logger.info(f"[ANSWER] {response[:100]}...")

    except Exception as e:
        error = f"[EXCEPTION] {str(e)}"
        logger.error(error)
        socket.send_string(json.dumps({"error": error}))