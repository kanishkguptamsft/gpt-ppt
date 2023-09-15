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

openai.api_key = ''
model_name = 'gpt-3.5-turbo'
template_dict = {
   '1' : """
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
""",
'2' : """ 
>>><input_text><<<

======
Intsuction prompt
Read >>>CONTENT<<< and generate JSON in the below format(Use this template if you want to generate a design document for a new service, ensure that the result has all the fields mentioned below)
{
"DesignDoc": {
  "Title": Title of the design document,
  "Introduction" : Provide an overview of the entire document,
  "System Overview" : Provide a general description and functionality of the software system. ,
  "Design Considerations": Describe the issues that need to be addressed before creating a design solution,
  "Assumptions and Dependencies" : Describe any assumptions that may be wrong or any dependencies on other things,
  "System Architecture" : This section should provide a high-level overview of how the functionality and responsibilities of the system were partitioned and then assigned to subsystems or components.,
  "Policies and Tactics": Describe any design policies and/or tactics that do not have sweeping architectural implications (meaning they would not significantly affect the overall organization of the system and its high-level structures),
  "Detailed System Design": Most components described in the System Architecture section will require a more detailed discussion. Other lower-level components and subcomponents may need to be described as well.,
  "Glossary": An ordered list of defined terms and concepts used throughout the document.},
"Diagram": this provides diagram of the content in plantuml output format
}
======
Please ensure that the output is in a perfect JSON format which can be serialized and deserialized. Please ensure that system overview section and detailed system design section are atleast 100 words long
---
Example

User:I have a service A, which calls service B for sku info, and service C for OS info. Based on information from B and C, service A calls a method called pushConfig which takes sku and os as input. Based on sku and os, the pushConfig method sends a command to a device.
Assistant: Here is the data you requested:
{
"DesignDoc": {
  "Title":,
  "Introduction",
  "System Overview",
  "Design Considerations":,
  "Assumptions and Dependencies",
  "System Architecture",
  "Policies and Tactics":,
  "Detailed System Design",
  "Glossary"},
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
      document.add_paragraph(json_obj[key])

    if(isinstance(json_obj[key], list)):
      for list_item in json_obj[key]:
        document.add_paragraph(list_item, style='List Bullet')

  document.add_picture(img_path, width=Inches(3.5))

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
    # text_input = "I have a complaint management, we are implementing a password based authentication of the user. The authentication be 2 factor, the first factor will be done by checking the password for the corresponding username in an azure cosmos db. The password passed will be encrypted. The second authentication will be done by producing a random produced at runtime otp, sending it to the user and verifying "
    # Add Open Ai Key before running get_completion.
    output_gpt = get_completion(template_input, text_input)
    # response = {'input_text': text_input, 'output_gpt': output_gpt}
    # return jsonify(response)
    # Below string is a sample output from GPT-3. This can be used to text other methods. Uncomment the below line and comment the above line for that.
    # output_gpt = '{\n    \"DesignDoc\": {\n        \"Title\": \"Extend IService for Service A\",\n        \"Introduction\": \"This design document outlines the extension of the IService interface to support a new service A in the application. The goal is to allow Service A to take a JSON file input from a provided location and deserialize it into an object. The design will utilize the singleton pattern for implementation.\",\n        \"System Overview\": \"The software system consists of multiple services that implement the IService interface. These services are responsible for handling JSON file inputs and deserializing them into objects. The new service A will be added to the system, extending the existing IService interface.\",\n        \"Design Considerations\": \"Before adding the new service A, the design must consider the following issues: 1. How to ensure a single instance of the service is created and used throughout the application. 2. How to handle the JSON file input and deserialize it into an object. 3. How to provide flexibility for the caller to specify the location of the JSON file.\",\n        \"Assumptions and Dependencies\": \"The design assumes that the existing services implementing IService are functional and correctly handle JSON file inputs. The design also assumes that the caller will provide the location of the JSON file. The new service A depends on the existing IService interface and its implementation.\",\n        \"System Architecture\": \"The system architecture follows a modular approach, where each service implements the IService interface. The addition of service A will not significantly affect the overall organization of the system. Service A will be a singleton class that extends the IService interface.\",\n        \"Policies and Tactics\": \"The design policy for the new service A is to use the singleton pattern for implementation. This ensures that only one instance of the service is created and used throughout the application. The design tactic for handling JSON file inputs is to provide a parameter in the IService method for specifying the location of the JSON file.\",\n        \"Detailed System Design\": \"The implementation details of the new service A are as follows: 1. Create a new class called ServiceA that extends the IService interface. 2. Implement the IService method to take a parameter for the location of the JSON file. 3. Use the singleton pattern to ensure only one instance of the ServiceA class is created. 4. Inside the implementation of the IService method, read the JSON file from the specified location and deserialize it into an object. 5. Return the deserialized object as the output of the IService method.\",\n        \"Glossary\": \"IService - Interface implemented by multiple services in the application for handling JSON file inputs and deserialization. Service A - New service being added to the application, extending the IService interface. JSON file - A file containing data in the JSON format. Deserialization - The process of converting JSON data into a structured object representation.\"\n    },\n    \"Diagram\": \"\"\"\n    @startuml\n    IService <|.. ServiceA : extends\n    IUser <|-- ServiceA : implements\n\n    class ServiceA {\n        +getInstance(): ServiceA\n        +processJsonFile(location: string): Object\n    }\n    IUser <|-- ServiceB : implements\n    IUser <|-- ServiceC : implements\n\n    IUser <|.. ServiceB\n    IUser <|.. ServiceC\n\n    IUser <|.. ServiceN\n\n    IUser : Request JSON File\n    ServiceA : processJsonFile()\n    IUser : Receive Deserialized Object\n\n    @enduml\n    \"\"\"\n}'
    json_output_gpt = Convert_string_to_json(output_gpt)
    write_file(json_output_gpt['Diagram'], uml_text_file_path)
    Create_plantUml_img(uml_text_file_path, uml_img_file_path)
    create_document_from_json(json_output_gpt['DesignDoc'], json_output_gpt['DesignDoc']['Title'], uml_img_file_path, doc_path)
    output_doc_blob_link = add_file_to_blob(doc_path, generate_random_string(10)+".docx", container_name)
    output_img_blob_link = add_file_to_blob(uml_img_file_path, generate_random_string(10)+".png", container_name)
    response = {'document': output_doc_blob_link, 'diagram' : output_img_blob_link, 'input_text': text_input, 'output_gpt': output_gpt}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
