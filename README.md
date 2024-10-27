# MarcGenie

**MarcGenie** is an automated tool designed to streamline and simplify the cleanup of serial holdings data in library systems post-migration, particularly within the Alma library management system. It automates the generation and standardization of MARC record fields, specifically $866 fields, reducing manual effort and improving data accessibility and consistency across large datasets.

## Features
- **Automated $866 Field Generation**: Extracts subfields from $853 and $863 fields to create standardized $866 summary fields.
- **Batch Processing**: Efficiently handles thousands of MARC records in a single run.
- **Error Logging**: Logs skipped records (e.g., missing necessary fields) for manual review, ensuring data completeness.
- **Customizable Templates**: Dynamically builds $866 fields from $853 fields, adjusting based on the unique structure of each record.

## Table of Contents
1. [Installation](#installation)
2. [Usage](#usage)
3. [Functionality](#functionality)
4. [Examples](#examples)
5. [Contributing](#contributing)
6. [License](#license)

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/marcgenie.git
   cd marcgenie
   ```
2. **Install Dependencies**:
  MarcGenie relies on Python and the PyMARC library. Install dependencies via:
  ```bash
  pip install -r requirements.txt
  ```
  Note: Python 3.7 or later is recommended.

## Usage

1.	**Open Command Prompt**:
    Start by navigating to the MarcGenie directory.
  	
2.	Run MarcGenie:
    Execute the tool by running:
    ```bash
    python auto.py
    ```
3.	**Input & Output**:
	•	A file selection window will pop up—select your .mrc MARC file.
	•	Enter a name for the output file when prompted.
	
4.	**Output Files**:
	•	*output.mrc*: MARC file ready for Alma with updated $866 fields.
	•	*output.txt*: Text file for human-readable review.
	•	*SkippedRecords.mrc*: Lists records missing fields, allowing for further investigation.

## Functionality

1. **Subfield Extraction** - MarcGenie uses a function to parse $853 fields, extracting subfield values like enumeration and chronology. These values form a customized template used in creating each $866 field.

2. **Range Parsing for $866 Field Generation** - MarcGenie is also optimized to interprets date and issue ranges from $863 fields, transforming them into clear, descriptive $866 fields (e.g., Jan.-Mar. 2022). This function applies standard mappings for months and seasons, ensuring uniformity.

3. **Error Handling and Logging** - MarcGenie logs records with missing $853 or $863 fields in SkippedRecords.mrc, allowing users to address these records manually. This ensures full control over the data quality.

## Examples
Here is an example of MarcGenie’s workflow:

1.	Input Record:
    ```plaintext
    853: $8 1 $a v. $i (year)
    863: $8 1 $i 2022 $j 01-03
    ```

2.	Generated $866 Field:
    ```plaintext
    866: $8 1 $a v. (2022) Jan.-Mar.
    ```

3.	Output:
    Processed and standardized MARC records are outputted as .mrc and .txt files for easy uploading and review.


## Contributing
Contributions are welcome! Please submit a pull request or reach out via issues for any bug reports or suggestions.

## License
MIT License

Copyright (c) 2024 Swachandrika Rudra

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
