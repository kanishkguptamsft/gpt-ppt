To run app.py:
  1. Open an elevated cmd and run the following: 
    pip install openai
    pip install plantuml
    pip install python-docx
    pip install azure-storage-blob
    pip install flask
    pip install azure-storage-blob --upgrade
  
  2. Add the openai key in app.py
  3. in an elevated cmd go to the repo and run app.py. This would host the app and it should return "Running on http://127.0.0.1:5000" if the hosting was successful
  4. To send a request to the api use the following command in another elevated cmd run "curl http://127.0.0.1:5000/gpt?text_input={input}" where {input} would be the user input we would be passing to gpt to create our document
