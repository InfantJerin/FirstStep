FirstStep - new app

create python virtual env
python -m venv .venv


pip install  google-cloud-aiplatform langchain langchain-core langchain-text-splitters langchain-google-vertexai langchain-community faiss-cpu langchain-chroma pypdf

pip install google-cloud-texttospeech
pip install google-cloud-speech

install gcloud (gcloud cli)

gcloud auth application-default login

gcloud auth application-default set-quota-project <hack-poc-435717> # create project and set it as quota project & enable the Vertex AI API

you can check your quota usage at https://console.cloud.google.com/vertex-ai/quotas

then run google_vertex_text.py

# voice_bot
1. Add DEEPGRAM_API_KEY in server.js 
2. Add deepgram key in  voiceBot.html. -> const deepgramClient = createClient(''); //
3. Do auth for google cloud cli as mentioned here - https://googleapis.dev/python/google-api-core/latest/auth.html 
This is required for vertex AI integration.

4. npm intsall -> node server.js to run server.
5. open voiceBot.html -> to start the voiceBot.