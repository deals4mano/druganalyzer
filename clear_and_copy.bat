@echo off

:: Define folder paths
set EXTRACTED_FOLDER=E:\Projects\aidrugalayzer\extracted
set MONITORED_FOLDER=E:\Projects\aidrugalayzer\monitored
set ERROR_FOLDER=E:\Projects\aidrugalayzer\error
set TEST_FOLDER=E:\Projects\aidrugalayzer\test
::set FILE_TO_COPY=MRN123456.zip
set FILE_TO_COPY=SamplePatientData.zip

:: Check if a parameter is provided
if "%1"=="" (
    echo Error: No parameter provided. Use "clear" or "copy".
    goto :end
)

:: Handle the "clear" operation
if /i "%1"=="clear" (
    echo Clearing the extracted and monitored folders...

    :: Clear the extracted folder
    if exist "%EXTRACTED_FOLDER%" (
        rmdir /s /q "%EXTRACTED_FOLDER%"
        mkdir "%EXTRACTED_FOLDER%"
    ) else (
        mkdir "%EXTRACTED_FOLDER%"
    )

    :: Clear the monitored folder
    if exist "%MONITORED_FOLDER%" (
        rmdir /s /q "%MONITORED_FOLDER%"
        mkdir "%MONITORED_FOLDER%"
    ) else (
        mkdir "%MONITORED_FOLDER%"
    )

    :: Clear the error folder
    if exist "%ERROR_FOLDER%" (
        rmdir /s /q "%ERROR_FOLDER%"
        mkdir "%ERROR_FOLDER%"
    ) else (
        mkdir "%ERROR_FOLDER%"
    )    

    echo Folders cleared successfully.
    goto :end
)

:: Handle the "copy" operation
if /i "%1"=="copy" (
    echo Copying %FILE_TO_COPY% from test folder to monitored folder...

    if exist "%TEST_FOLDER%\%FILE_TO_COPY%" (
        copy /y "%TEST_FOLDER%\%FILE_TO_COPY%" "%MONITORED_FOLDER%"
        echo File copied successfully.
    ) else (
        echo Error: %FILE_TO_COPY% does not exist in the test folder.
    )

    goto :end
)

:: Handle invalid parameters
echo Error: Invalid parameter. Use "clear" or "copy".

:end
