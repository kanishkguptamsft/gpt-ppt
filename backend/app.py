# OPENAI

# import openai
# openai.api_key = ''
# model_name = 'gpt-3.5-turbo'
# generic_prompt = """
# Instruction: Analyse >>CONTENT<< to generate a design document which will contain the following information 1. Intention 2. Description 3. Section which contains information to create a diagram in plantuml format Question: I have a service called ABC which interacts with devices. devices can be of different skus and os versions, which has 3 dependencies, service1, service2 and service3. service 1 provides the information of the sku of the device. service 2 provides the configuration to be pushed on device. service 3 provides the OS version running on the device. Hwproxy interacts with service 1, gets the sku information. Then interacts with service 3 to get the OS running on device. It then interacts with Config to be pushed on device from service 2. Using the information it initialized a driver of the correct sku and os version, it then sends the sku and os version specific command to push the config fetched from service 2."
# """
 

# def get_completion():
#     chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": generic_prompt}])
#     print(chat_completion.choices[0].message.content)


# if __name__ == "__main__":
#     get_completion()

# PLANTUML code
# from plantuml import PlantUML

# server = PlantUML(url='http://www.plantuml.com/plantuml/img/',
#                           basic_auth={},
#                           form_auth={}, http_opts={}, request_opts={})

# server.processes_file('test.txt', 'test.png')

# DOCUMENT

# from docx import Document
# from docx.shared import Inches
# document = Document()

# document.add_heading('Document Title', 0)

# p = document.add_paragraph('A plain paragraph having some ')
# p.add_run('bold').bold = True
# p.add_run(' and some ')
# p.add_run('italic.').italic = True

# document.add_heading('Heading, level 1', level=1)
# document.add_paragraph('Intense quote', style='Intense Quote')

# document.add_paragraph(
#     'first item in unordered list', style='List Bullet'
# )
# document.add_paragraph(
#     'first item in ordered list', style='List Number'
# )

# document.add_picture('test.png', width=Inches(1.25))

# records = (
#     (3, '101', 'Spam'),
#     (7, '422', 'Eggs'),
#     (4, '631', 'Spam, spam, eggs, and spam')
# )

# table = document.add_table(rows=1, cols=3)
# hdr_cells = table.rows[0].cells
# hdr_cells[0].text = 'Qty'
# hdr_cells[1].text = 'Id'
# hdr_cells[2].text = 'Desc'
# for qty, id, desc in records:
#     row_cells = table.add_row().cells
#     row_cells[0].text = str(qty)
#     row_cells[1].text = id
#     row_cells[2].text = desc

# document.add_page_break()

# document.save('demo.docx')