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
