# PDF Renaming Project

## Setup Instructions

1. Ensure Python 3.7 or higher is installed on your machine.

2. Clone or download the project files to your local machine.

3. Open a terminal/command prompt in the project root directory.

4. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   ```

5. Activate the virtual environment:
   - On Windows:
     ```
     venv\\Scripts\\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

6. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

7. Run the PDF renaming script:
   ```
   python src/main.py
   ```

8. Follow the on-screen prompts to provide the path to your PDF files or directory.

## Notes

- The renamed files will be saved in a randomly named Roman numeral subfolder within the same directory.

- Original files are not modified or deleted.

- Ensure you have read/write permissions for the directories involved.

## Contact

For any issues or questions, please contact the project maintainer.
