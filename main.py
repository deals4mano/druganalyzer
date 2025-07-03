import os  
import time  
import zipfile
import traceback

from druganalyzer import analyze_documents, analyze_documents_without_upload, delete_uploads

from fileloader import encode_pdf_to_base64 
from queue import Queue
from threading import Thread
from watchdog.observers import Observer  
from watchdog.events import FileSystemEventHandler

class DirectoryMonitorHandler(FileSystemEventHandler):
    """
    Handles events for monitoring a directory.
    """
    def __init__(self, event_queue):
        super().__init__()
        self.event_queue = event_queue

    def on_created(self, event):
        print(f"Event detected: {event.event_type} on {event.src_path}")
        self.event_queue.put(event)


def monitor_folder(folder, event_queue):
    """
    Monitors the folder for new directories.
    :param folder: Path to the folder to monitor.
    """
    event_handler = DirectoryMonitorHandler(event_queue)
    observer = Observer()
    observer.schedule(event_handler, path=folder, recursive=False)
    observer.start()
    print(f"Monitoring folder: {folder}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:        
        observer.stop()
        print("Keyboard interrupt received, stopping the observer.")
        
    observer.join()
    

def process_folder(folder_path):
    try:
        folder_name = os.path.basename(folder_path)
        print(f"Processing files in : {folder_name}")
        """
        # Display the folder name and its contents in the Streamlit app
        with col_casename:
            st.write(f"{folder_name}")
        """
        fileList = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                print(f"Processing file: {file_path}")
                
                if file.lower().endswith('.pdf') or file.lower().endswith('.txt') or file.lower().endswith('.json') or file.lower().endswith('.csv') or file.lower().endswith('.docx'):                
                    fileList.append(file_path)       
        
        print(f"Files to analyze: {fileList}")                         
        #openai_response = analyze_documents(fileList,error_folder)  
        openai_response = analyze_documents_without_upload(fileList,error_folder)        
        if openai_response.output_text:
            with open(os.path.join(folder_path, "analysis_report.txt"), "w") as report_file:
                report_file.write(openai_response.output_text)
    except Exception as e:
        print(f"Error processing  '{folder_path}': {e}")
        traceback.print_exc()
 

if __name__ == "__main__":

    #Cleanup openai uploads
    #delete_uploads()

    # Define the folders
    monitored_folder = r"E:\Projects\aidrugalayzer\monitored"
    extracted_folder = r"E:\Projects\aidrugalayzer\extracted"
    error_folder = r"E:\Projects\aidrugalayzer\error"
    base_folder = r"E:\Projects\aidrugalayzer"

    # Ensure the folder exists
    os.makedirs(extracted_folder, exist_ok=True)

    #process_folder(None, extracted_folder)
    
    # Create a queue for communication between threads
    event_queue = Queue()

    # Start the watchdog monitoring in a separate thread
    monitor_thread = Thread(target=monitor_folder, args=(monitored_folder, event_queue), daemon=True)
    monitor_thread.start()

    # Main thread: Process events from the queue
    while True:
        try:
            # Check for new events in the queue
            event = event_queue.get(timeout=1)  # Wait for up to 1 second
            print(f"Processing event: {event}")
            if not event.is_directory:
                file_path = event.src_path
                file_name = os.path.basename(file_path)

                print(f"New file detected: {file_name}")
                # Check if the file is a ZIP file
                if file_name.endswith('.zip'):
                    try:
                        # Create a folder for extraction
                        extraction_path = os.path.join(extracted_folder, os.path.splitext(file_name)[0])
                        print(f"Extraction path: {extraction_path}")
                        os.makedirs(extraction_path, exist_ok=True)

                        # Extract the ZIP file
                        with zipfile.ZipFile(file_path, 'r') as zip_ref:
                            zip_ref.extractall(extraction_path)

                        print(f"Extracted '{file_name}' to '{extraction_path}'.")
                        process_folder(extraction_path)                      

                    except zipfile.BadZipFile:
                        print(f"Error: '{file_name}' is not a valid ZIP file.")
                        traceback.print_exc()
                    except Exception as e:
                        print(f"An error occurred while extracting '{file_name}': {e}")
                        traceback.print_exc()
                else:
                    print(f"File '{file_name}' is not a ZIP file, skipping extraction.")            
                         
        except Exception:            
            pass  # Continue if the queue is empty


            
 

