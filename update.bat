@echo off
start https://github.com/tutumomo/langchain-tutorials-gkamradt-
start https://github.com/tutumomo/LangChain-Tutorials
pause

git pull 

call ac
pip install -U langchain langchain-core langchain-community langchain-openai

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

pause