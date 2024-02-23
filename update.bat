REM https://github.com/tutumomo/langchain
@echo off
start https://github.com/tutumomo/langchain-tutorials-gkamradt-
start https://github.com/tutumomo/LangChain-Tutorials
start https://github.com/tutumomo/LangChain-Chinese-Getting-Started-Guide
pause

git pull 

call ac
pip install -U langchain langchain-core langchain-community langchain-openai openai google-search-results unstructured chromadb pinecone-client youtube-transcript-api pytube jupyter ipywidgets

if not exist langchain-tutorials-gkamradt- (
   git clone https://github.com/tutumomo/langchain-tutorials-gkamradt-.git
) else (
   cd langchain-tutorials-gkamradt-
   git pull
   cd ..
)

if not exist LangChain-Tutorials (
   git clone https://github.com/tutumomo/LangChain-Tutorials.git
) else (
   cd LangChain-Tutorials
   git pull
   cd ..
)

if not exist LangChain-Chinese-Getting-Started-Guide (
   git clone https://github.com/tutumomo/LangChain-Chinese-Getting-Started-Guide.git
) else (
   cd LangChain-Chinese-Getting-Started-Guide
   git pull
   cd ..
)
pause
