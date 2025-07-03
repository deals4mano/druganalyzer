# AI Drug Analyzer

AI Drug Analyzer is a Python-based application that uses OpenAI's API to analyze patient charts, lab results, and other medical documents. It provides insights such as drug compatibility, risk assessments, and monitoring recommendations.

## Features

- **File Monitoring**: Automatically monitors a folder for new files (e.g., PDFs, text files, etc.).
- **File Analysis**: Analyzes uploaded files using OpenAI's API.
- **Dynamic JSON Request Creation**: Dynamically constructs JSON requests for OpenAI's `responses.create` API.
- **Error Handling**: Handles file upload errors and moves problematic files to an error folder.
- **Report Generation**: Generates analysis reports and saves them as text files.
- **File Cleanup**: Deletes uploaded files from OpenAI after processing.

## Requirements

The project requires Python 3.8 or higher. Install the dependencies listed in the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### Key Dependencies
OpenAI: For interacting with OpenAI's API.  
Watchdog: For monitoring file system changes.  

```
.
├── main.py                                              # Entry point for the application
├── druganalyzer.py                                      # Handles file uploads and OpenAI API interactions
├── fileloader.py                                        # Encodes files (e.g., PDFs) to Base64
├── requirements.txt                                     # List of dependencies
├── README.md                                            # Project documentation
├── monitored/                                           # Folder to monitor for new files
├── extracted/                                           # Folder where extracted files are stored
├── error/                                               # Folder for problematic files
```
Usage
Set Up OpenAI API Key:

Add your OpenAI API key to the environment variable OPENAI_API_KEY or directly in the code (not recommended for production).
Run the Application: Start the application by running the main.py file:

```bash
python main.py
```

Monitor Folder: Place files (e.g., PDFs, text files) in the monitored folder. The application will automatically process them.  

View Reports: Processed files will generate analysis reports saved in the corresponding folder.  

**Example Workflow**  
Place a file (e.g., PatientChart.pdf) in the monitored folder.  
The application detects the file, uploads it to OpenAI, and processes the response.  
The analysis report is saved as analysis_report.txt in the same folder.    

**JSON Request Example**  
The application dynamically generates JSON requests for OpenAI's API. Below is an example of a generated request:
```
{
    "role": "user",
    "content": [
        {
            "type": "input_text",
            "text": "Analyze the attached patient charts and provide a detailed report."
        },
        {
            "type": "input_file",
            "filename": "PatientChart.pdf",
            "file_data": "data:application/pdf;base64,JVBERi0xLjQKJ..."
        }
    ]
}
```
**Error Handling**  
Files that fail to upload or process are moved to the error folder for review.
Detailed error logs are printed to the console for debugging
