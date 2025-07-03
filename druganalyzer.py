import os
import base64
import traceback
import shutil
import json
from time import sleep

from fileloader import encode_pdf_to_base64

prompt="Attached files contain patient charts , lab results for multiple visits. Analyze the documents and provide a report in the following structure\n\n- analyze drug compatibility and highlight potential risks such as known allergies, disease contraindications, unfavorable lab values\n- check for therapeutic duplication or potential ineffectiveness based on patient history\n- highlight high risk profiles and alert risky drug classes based on patient history\n- provide a summary that includes Key facts from patient history relevant to the prescription, Risk assessment, Monitoring recommendations (e.g., check blood sugar, LDL, HDL), Suggested drug alternatives (if relevant)"
requestInputSection = '"content": ['
from openai import OpenAI
import openai
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

uploaded_files = []

def upload_files(fileObjectList, error_folder):    
    try:
      for file_name in fileObjectList:
        response = client.files.create(
          file=open(file_name, "rb"),
          purpose="user_data"
        )
        print(f"Uploaded file ID: {response.id}, Name: {file_name}")
        uploaded_files.append(response.id)
      sleep(5)  # Wait for a moment to ensure files are uploaded  
      return uploaded_files
    except Exception as e:
      print(f"Error uploading files: {e}")
      traceback.print_exc()
      shutil.move(file_name, error_folder)  # Move file to error folder
      return e
    
def analyze_documents(fileList, error_folder):  
  print(f"Inside Analyze Documents")
  try:
    fileIDList = upload_files(fileList,error_folder)     
    openai_request = (construct_request(prompt,fileIDList))  
    print(f"Constructed OpenAI request: {openai_request}")
    openai_response = client.responses.create(      
      input=openai_request, store=False , temperature=0.3, model="gpt-4.1"     
    )  
    print(f"OpenAI response: {openai_response.output_text}")    
    delete_uploads()
    return openai_response

  except Exception as e:
    print(f"Error during file upload or analysis: {e}")
    traceback.print_exc()
    return None


def analyze_documents_without_upload(fileList, error_folder):  
  print(f"Inside Analyze Documents without upload")
  try:
       
    openai_request = (construct_request(prompt,fileList))  
    print(f"Constructed OpenAI request: {openai_request}")
    openai_response = client.responses.create(      
      input=openai_request, store=False , temperature=0.3, model="gpt-4.1"     
    )  
    print(f"OpenAI response: {openai_response.output_text}")    
    
    return openai_response

  except Exception as e:
    print(f"Error during file analysis: {e}")
    traceback.print_exc()
    shutil.move(fileList, error_folder)
    return None

def delete_uploads():
   print("Deleting uploaded files...")   
   for file in client.files.list(purpose="user_data"):
      try:        
        client.files.delete(file.id)
        print(f"Deleted file ID: {file.id}")
      except Exception as e:
        print(f"Error deleting file ID {file.id}: {e}")


def fetch_response():
  response = client.responses.retrieve("resp_123")
  return response


def construct_request(prompt, files):  
    # Base structure of the request
    request = {
        "role": "user",
        "content": [
            {
                "type": "input_text",
                "text": prompt
            }
        ]
    }
    # Add files dynamically to the "content" section
    for file in files:
        request["content"].append({
            "type": "input_file",
            "filename": file,
            "file_data": encode_pdf_to_base64(file)
        })
    # Convert the Python object to a JSON string
    json_request = json.dumps(request, indent=4)
    return json_request

def construct_request_with_uploads( prompt, file_ids):
    # Base structure of the request
    request = {
        "role": "user",
        "content": [
            {
                "type": "input_text",
                "text": prompt
            }
        ]
    }

    # Dynamically add file IDs to the "content" section
    for file_id in file_ids:
        request["content"].append({
            "type": "input_file",
            "file_id": file_id
        })

    # Convert the Python object to a JSON string
    json_request = json.dumps(request, indent=4)
    return json_request

