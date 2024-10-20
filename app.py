from flask import Flask, render_template, request, jsonify, Response, stream_with_context
import requests
import json
from datetime import datetime
import time

app = Flask(__name__)

# Global variables to store the endpoints and system prompts
ENDPOINT1 = ""
ENDPOINT2 = ""
SYSTEM_PROMPT1 = ""
SYSTEM_PROMPT2 = ""
MODEL1 = ""
MODEL2 = ""

def get_model_name(endpoint):
    try:
        response = requests.get(f"{endpoint}/v1/models")
        response.raise_for_status()
        models = response.json().get('data', [])
        if models:
            return models[0].get('id', 'Unknown Model')
        return 'Unknown Model'
    except:
        return 'Unknown Model'

def stream_response(endpoint, prompt, conversation_history):
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": conversation_history + [{"role": "user", "content": prompt}],
        "stream": True  # We need to stream the response
    }

    try:
        response = requests.post(f"{endpoint}/v1/chat/completions", headers=headers, json=data, stream=True)
        response.raise_for_status()

        total_tokens = 0  # Track number of tokens
        start_time = time.time()  # Time tracking

        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    line = line[6:]  # Remove 'data: ' prefix
                if line != '[DONE]':
                    try:
                        chunk = json.loads(line)

                        if 'choices' in chunk:
                            # Count tokens generated in this chunk
                            content = chunk['choices'][0]['delta'].get('content', '')
                            token_count = len(content.split())  # Naive token estimation by word count
                            total_tokens += token_count

                            yield chunk  # Yield valid responses to the frontend
                    except json.JSONDecodeError:
                        print(f"Invalid JSON: {line}")

        elapsed_time = time.time() - start_time  # Time taken to generate the tokens
        if elapsed_time > 0:  # Avoid division by zero errors
            tokens_per_second = total_tokens / elapsed_time
        else:
            tokens_per_second = 0
        
        # Yield a summary with token count and token per second rate
        yield {"total_tokens": total_tokens, "elapsed_time": elapsed_time, "tps": tokens_per_second}
    except requests.RequestException as e:
        yield json.dumps({"error": str(e)})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/connect', methods=['POST'])
def connect():
    global ENDPOINT1, ENDPOINT2, SYSTEM_PROMPT1, SYSTEM_PROMPT2, MODEL1, MODEL2
    endpoint_num = request.json['endpoint_num']
    endpoint_url = request.json['endpoint_url']
    system_prompt = request.json['system_prompt']
    
    if endpoint_num == 1:
        ENDPOINT1 = endpoint_url
        SYSTEM_PROMPT1 = system_prompt
        MODEL1 = get_model_name(ENDPOINT1)
    else:
        ENDPOINT2 = endpoint_url
        SYSTEM_PROMPT2 = system_prompt
        MODEL2 = get_model_name(ENDPOINT2)
    
    try:
        response = requests.get(endpoint_url)
        if response.status_code == 200:
            return jsonify({"status": "success", "message": f"Connected to Endpoint {endpoint_num}"})
        else:
            return jsonify({"status": "error", "message": f"Failed to connect to Endpoint {endpoint_num}"})
    except requests.RequestException:
        return jsonify({"status": "error", "message": f"Failed to connect to Endpoint {endpoint_num}"})

@app.route('/chat', methods=['POST'])
def chat():
    if not ENDPOINT1 or not ENDPOINT2:
        return jsonify({"error": "Please connect to both endpoints first"})
    
    initial_prompt = request.json['prompt']
    num_exchanges = int(request.json['num_exchanges'])

    conversation_history = [
        {"role": "system", "content": SYSTEM_PROMPT1},
        {"role": "user", "content": initial_prompt}
    ]

    def generate():
        current_prompt = initial_prompt

        for i in range(num_exchanges):
            # Stream response from Model 2
            yield json.dumps({"sender": "Model 2", "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "model": MODEL2}) + '\n'
            full_response = ""
            tokens = 0  # Track tokens from Model 2
            for chunk in stream_response(ENDPOINT2, current_prompt, conversation_history):
                if 'choices' in chunk:
                    content = chunk['choices'][0]['delta'].get('content', '')
                    full_response += content
                    yield json.dumps({"content": content}) + '\n'
                if 'total_tokens' in chunk:  # Pass token stats data
                    tokens = chunk['total_tokens']
                    tps = chunk['tps']
                    elapsed_time = chunk['elapsed_time']

            # Append model stats (timestamp, tokens, t/s)
            yield json.dumps({
                "end": True,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "model": MODEL2,
                "total_tokens": tokens,
                "tps": tps
            }) + '\n'
            
            current_prompt = full_response  # Prepare next response for Model 1
            conversation_history.append({"role": "assistant", "content": full_response})

            # Stream response from Model 1
            yield json.dumps({"sender": "Model 1", "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "model": MODEL1}) + '\n'
            full_response = ""
            tokens = 0  # Track tokens from Model 1
            for chunk in stream_response(ENDPOINT1, current_prompt, conversation_history):
                if 'choices' in chunk:
                    content = chunk['choices'][0]['delta'].get('content', '')
                    full_response += content
                    yield json.dumps({"content": content}) + '\n'
                if 'total_tokens' in chunk:
                    tokens = chunk['total_tokens']
                    tps = chunk['tps']
                    elapsed_time = chunk['elapsed_time']

            # Append model stats (timestamp, tokens, t/s)
            yield json.dumps({
                "end": True,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "model": MODEL1,
                "total_tokens": tokens,
                "tps": tps
            }) + '\n'

            current_prompt = full_response  # Prepare next response for Model 2
            conversation_history.append({"role": "assistant", "content": full_response})

    return Response(stream_with_context(generate()), content_type='application/json')

if __name__ == '__main__':
    app.run(debug=True)
