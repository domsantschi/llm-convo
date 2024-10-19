# llm-convo
I used 2 LLMs (Claude Sonnet 3.5 and chatgpt-4o-latest) to write an app that would let 2 LLMs with openai compatible api endpoints talk to each other. I have zero experience with python.
After running out of daily allowance on both Anthropic and OpenAI I got what's in this repo. Was more of an experiment if I can make an app without any experience more than anything else.
I used open-webui as frontend to "develop" this.

# ONLY TESTED with koboldcpp openai compatible endpoints

- Dark/Light theme
- Number of Exchanges between 3 and 30
- Supports streaming/interrupting of responses
- The endpoint addresses and system prompts are stored in browser Local Storage
- Timestamps, model names, tokens/second - oh my!
- Supports different system prompt for each endpoint
- I used the following system prompt for both while testing:
```
You are an AI with a distinct personality. Respond naturally to the given prompt, as if in a real conversation. Keep your reply focused and concise, ideally around 50-75 words. Don't continue the conversation beyond your response or roleplay as anyone else. Engage with the topic, add your perspective, or ask a relevant question, but always conclude your response naturally. Avoid overly formal or flowery language - aim for a casual, friendly tone.
```


![image_2024-10-19_21-06-29](https://github.com/user-attachments/assets/8e04143e-9908-4d7c-80ff-8d8a5bf07c80)



To try it out in docker:
```
git clone https://github.com/hugalafutro/llm-convo.git
cd llm-convo
docker compose build
docker compose up -d
```


Check docker logs `docker compose logs -f`:
```
llm-convo  |  * Serving Flask app 'app.py'
llm-convo  |  * Debug mode: off
llm-convo  | WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
llm-convo  |  * Running on all addresses (0.0.0.0)
llm-convo  |  * Running on http://127.0.0.1:5000
llm-convo  |  * Running on http://172.26.0.2:5000
llm-convo  | Press CTRL+C to quit
```


- Visit `http://0.0.0.0:5234`
- Enter the openai compatible api checkpoint address in format `http://address:port/v1` i.e. `http://192.168.1.163:5001/v1` and press Connect Endpoint button for both Endpoints.
- You sohuld get an popup connection succesful and the Endpoint button will turn green.
- Once both Enndpoint buttons are green it's go time.
- Write the Intial Prompt in the bottom text input area and click the Send button.
