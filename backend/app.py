from flask import Flask, request, jsonify
from plantuml import PlantUML
from docx import Document
from docx.shared import Inches
import openai
import json
import random
import string
import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient


openai.api_key = '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'
model_name = 'gpt-3.5-turbo'
generic_prompt = """
>>><input_text><<<

======
Intsuction prompt
Read >>>CONTENT<<< and generate JSON in the below format
{
"DesignDoc": {
  "Intent":,
  "Pros",
  "Cons",}.
"Diagram": this provides diagram of the content in plantuml output format
}
======
Please ensure that the output is in a perfect JSON format which can be serialized and deserialized.
---
Example

User:I have a service A, which calls service B for sku info, and service C for OS info. Based on information from B and C, service A calls a method called pushConfig which takes sku and os as input. Based on sku and os, the pushConfig method sends a command to a device.
Assistant: Here is the data you requested:
{
"DesignDoc":{
  "Intent",
  "Solution",
  "Pros",
  "Cons"},
"Diagram": \"\"\"
@startuml
actor User

User -> ServiceA : Request SKU Info
ServiceA -> ServiceB : Request SKU Info
ServiceB -> ServiceA : Return SKU Info
ServiceA -> ServiceC : Request OS Info
ServiceC -> ServiceA : Return OS Info
ServiceA -> Device : Send Command

@enduml
\"\"\"
}
"""

template_dict = {
   '1' : """
>>><input_text><<<

======
Intsuction prompt
You are a design document generatror
Read >>>CONTENT<<< and generate JSON in the below format
{
"DesignDoc": {
  "Intent": this should provide the intent of the design,
  "Solution": this should go in detail of the solution proposed,
  "Pros": what are the benefits and strengths of this approach,
  "Cons": what are the disadvantages of the approach},
"Diagram": this provides diagram of the content in plantuml output format
}
======
Ensure that the output is in a perfect JSON format which can be serialized and deserialized.
---
Example

User:I have a service A, which calls service B for sku info, and service C for OS info. Based on information from B and C, service A calls a method called pushConfig which takes sku and os as input. Based on sku and os, the pushConfig method sends a command to a device.
Assistant:
{
"DesignDoc":{
  "Intent",
  "Solution",
  "Pros",
  "Cons"},
"Diagram": \"\"\"
@startuml
actor User

User -> ServiceA : Request SKU Info
ServiceA -> ServiceB : Request SKU Info
ServiceB -> ServiceA : Return SKU Info
ServiceA -> ServiceC : Request OS Info
ServiceC -> ServiceA : Return OS Info
ServiceA -> Device : Send Command

@enduml
\"\"\"
}
---
""",
'2' : "1"
}
uml_text_file_path = "C:\Hack23\ChatDesignDoc\plantUml.txt"
uml_img_file_path = "C:\Hack23\ChatDesignDoc\plantUml.png"
doc_path = 'C:\Hack23\ChatDesignDoc\chatgptdoc.docx'
blob_service_client = BlobServiceClient.from_connection_string("BlobEndpoint=https://testingaci.blob.core.windows.net/;QueueEndpoint=https://testingaci.queue.core.windows.net/;FileEndpoint=https://testingaci.file.core.windows.net/;TableEndpoint=https://testingaci.table.core.windows.net/;SharedAccessSignature=sv=2022-11-02&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=2024-01-25T02:57:58Z&st=2023-09-13T18:57:58Z&spr=https&sig=66XZYbaPFUROK4CI%2BAWP1%2BRghH%2BsfQKawjlnLoiZS98%3D")
container_name = 'hackchat'

# Functions

def replace_input_text(input_string, template):
    return template.replace("<input_text>", input_string)

def get_completion(template_enum, input_text):
    if template_enum is None:
        template_enum = "1"
    template = template_dict[template_enum]
    input_text_in_template = replace_input_text(input_text, template)
    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": input_text_in_template}])
    return chat_completion.choices[0].message.content

def Convert_string_to_json(st):
  st = st.replace('"""','"')
  json_output = json.loads(st, strict=False)
  return json_output

def write_file(text, path):
  with open(path, 'w') as f:
    f.write(text)

def Create_plantUml_img(source, destination):
  server = PlantUML(url='http://www.plantuml.com/plantuml/img/',
                            basic_auth={},
                            form_auth={}, http_opts={}, request_opts={})
  server.processes_file(source, destination)

def create_document_from_json(json_obj, main_heading, img_path, doc_path):
  document = Document()
  document.add_heading(main_heading, 0)

  for key in json_obj.keys():
    document.add_heading(key, level=1)

    if(isinstance(json_obj[key], str)):
      document.add_paragraph(json_obj[key], style='Intense Quote')

    if(isinstance(json_obj[key], list)):
      for list_item in json_obj[key]:
        document.add_paragraph(list_item, style='List Bullet')

  document.add_picture(img_path, width=Inches(1.25))

  document.add_page_break()

  document.save(doc_path)


def generate_random_string(size):
    chars = string.ascii_lowercase
    return ''.join(random.choice(chars) for _ in range(size))

def add_file_to_blob(file_path, blob_name, container_name):
    # Create a blob client using the local file name as the name for the blob
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(blob_name)

    # Upload the created file
    with open(file_path, "rb") as data:
        blob_client.upload_blob(data)
    return blob_client.url

app = Flask(__name__)

@app.route('/gpt', methods=['GET'])
def gpt():
    text_input = request.args.get('text_input')
    template_input = request.args.get('template', None)
    # text_input = "I have an application with interface IService. IService is implemented by multiple services in the application and is responsible for taking a json file input from a location provided by the caller and the output is a deserialized object of the json file. Write a design doc to extend the interface for a new service A. Use singleton to implement the same."
    # Add Open Ai Key before running get_completion.
    output_gpt = get_completion(template_input, text_input)
    # Below string is a sample output from GPT-3. This can be used to text other methods. Uncomment the below line and comment the above line for that.
    # output_gpt = '{\n\"DesignDoc\": {\n  \"Intent\": \"The intent of the design is to implement a chain of responsibility design pattern to handle different types of tasks based on specific requirements.\",\n  \"Pros\": [\n    \"Flexibility: The chain of responsibility design pattern allows adding or removing responsibilities dynamically at runtime.\",\n    \"Decoupling: The pattern decouples the sender and receiver of a request, allowing them to vary independently.\",\n    \"Simplification: It simplifies the client code by abstracting away the details of the handling logic and providing a unified interface.\"\n  ],\n  \"Cons\": [\n    \"Performance impact: The chain of responsibility may have performance implications as each handler needs to check if it can handle the request, potentially leading to multiple iterations.\",\n    \"Complexity: The pattern can introduce additional complexity, especially when the number of handlers increases, making it harder to maintain and debug.\"\n  ]\n},\n\"Diagram\": \"\"\"\n@startuml\nclass Client\n\ninterface ITaskHandler {\n  +handler()\n}\n\nclass AdditionTask {\n  +handler()\n}\n\nclass MultiplyTask {\n  +handler()\n}\n\nclass DivideTask {\n  +handler()\n}\n\nClient --> ITaskHandler\nITaskHandler <|- AdditionTask\nITaskHandler <|- MultiplyTask\nITaskHandler <|- DivideTask\n\n@enduml\n\"\"\"\n}'
    json_output_gpt = Convert_string_to_json(output_gpt)
    write_file(json_output_gpt['Diagram'], uml_text_file_path)
    Create_plantUml_img(uml_text_file_path, uml_img_file_path)
    create_document_from_json(json_output_gpt['DesignDoc'], "document", uml_img_file_path, doc_path)
    output_doc_blob_link = add_file_to_blob(doc_path, generate_random_string(10)+".docx", container_name)
    output_img_blob_link = add_file_to_blob(uml_img_file_path, generate_random_string(10)+".png", container_name)
    print(output_doc_blob_link)
    response = {'document': output_doc_blob_link, 'diagram' : output_img_blob_link, 'input_text': text_input, 'output_gpt': json_output_gpt}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
