# Import necessary libraries
from pymarc import MARCReader, MARCWriter, Field, Subfield
import tkinter as tk, filedialog, Button, Label
from tkinter import simpledialog
from tkinter.filedialog import askopenfilename
import sys
import os
import re

def extract_subfields(record):
    subfields_array = []
    for field in record.get_fields('853'):
        for code, value in field.subfields:
            if code not in subfields_array:
                subfields_array.append(code)
    subfields_array.append('8')
    return subfields_array

def generate_description_field(record, subfields_array):
    existing_853 = {}
    for field in record.get_fields('853'):
        tag = field.tag
        if tag not in existing_853:
            existing_853[tag] = []
        existing_853[tag].append(field)
            
    existing_863 = {}
    for field in record.get_fields('863'):
        tag = field.tag
        if tag not in existing_863:
            existing_863[tag] = []
        existing_863[tag].append(field)
        
    description_fields = []
    description = ""
    b = ['(' , '[' , '{' , '}' , ']' , ')']
    month_abbreviations = {'01': 'Jan.','1': 'Jan.', 
                           '02': 'Feb.','2': 'Feb.', 
                           '03': 'Mar.','3': 'Mar.',
                           '04': 'Apr.','4': 'Apr.',
                           '05': 'May','5': 'May',
                           '06': 'Jun.','6': 'Jun.',
                           '07': 'Jul.','7': 'Jul.',
                           '08': 'Aug.','8': 'Aug.',
                           '09': 'Sep.','9': 'Sep.',
                           '10': 'Oct.','11': 'Nov.','12': 'Dec.',
                           '21':'spring', '22':'summer', '23':'autumn', '24':'winter'}
    seasons = {'21':'spring', '22':'summer', '23':'autumn', '24':'winter'}

    sub853 = {}                   
    for tag, fields in existing_853.items():
        for f in fields: 
            for c, v in f.subfields:
                if c in subfields_array:
                    sub853[c] = v.strip()
    
    field8 = ""
    ind = ""
    for tag, fields in existing_863.items():
        for field in fields: 
            ind += field.indicator1+field.indicator2
            if ind == "40":
                indicators = ["3", "1"]
            else:
                indicators = [field.indicator1, field.indicator2]
            ind = ""
            
            sub863 = {} #intializing sub863
            range_tracker = {}
            last_code_with_range = None
            
            for code, value in field.subfields:
                if code == '8':
                        continue
                else:
                    if "-" in value:
                        range_tracker[code] = 1
                        last_code_with_range = code
                    else:
                        range_tracker[code] = 0
            
            for code, value in field.subfields:
                str = ""
                if code in subfields_array:
                    if code == '8':
                        field8 = value.strip()
                        continue
                    else:
                        str = sub853[code].strip()
                        if any(ch in str for ch in b):
                            if "v" in str and "." not in str:
                                sub863[code] = sub853[code]+"."+value.strip()

                            if "year" in str and "-" in value: # range_tracker[code] == 1:
                                if code == last_code_with_range:
                                    sub863[code] = value.strip()
                                    description = range_parser(sub863, value.strip(), False)+":"
                                else:
                                    sub863[code] = value.strip()
                            elif "year" in str:
                                sub863[code] = value.strip()
                                description = description+f"{sub863[code]}:"
                                    
                            if "month" in str and "-" in value:
                                if code == last_code_with_range:
                                    # print(f"value: {value.strip()} in month_abbs? {value.strip() in month_abbreviations}")
                                        
                                    if bool(re.search(r"^\d{2}-\d{2}$", value.strip())): #encoded with range
                                        sub863[code] = value.strip()
                                        description = range_parser(sub863, value.strip(), False)+":"
                                    elif value.strip() in month_abbreviations: # incase only encoded with no range
                                        value = month_abbreviations[value.strip()]  
                                        sub863[code] = value.strip() #str[:1] + value.strip() + str[-1]
                                        description = description+f"{sub863[code]}:"
                                    elif "-" in value: # incase month names are already written
                                        sub863[code] = value.strip()
                                        description = range_parser(sub863, value.strip(), True)+":"
                                else:
                                    if value.strip() in month_abbreviations and "-" in value: #encoded with range
                                        sub863[code]  = month_abbreviations[value.strip()]   
                                        description = description+f"{sub863[code]}:"
                                    elif value.strip() in month_abbreviations: # incase only encoded with no range
                                        sub863[code] = month_abbreviations[value.strip()] #str[:1] + value.strip() + str[-1]
                                        description = description+f"{sub863[code]}:" 
                                    elif "-" in value: # incase month names are already written
                                        sub863[code]  = value.strip()
                                        description = description+f"{sub863[code]}:" 
                            elif "month" in str:
                                # print("NOT a range!!!")
                                # print(f"value: {value.strip()} in month_abbs? {value.strip() in month_abbreviations}")
                                     
                                if value.strip() in month_abbreviations: # incase only encoded with no range
                                        sub863[code] = month_abbreviations[value.strip()]
                                        # print(f"month_abbs[{value.strip()}] = {sub863[code]}")
                                        description = description+f"{sub863[code]}:" 
                                        # print(f"description: {description}")
                                else:
                                    sub863[code] = value.strip()
                                    description = description+f"{sub863[code]}:"
                                                                       
                            if "season" in str and "-" in value:
                                if code == last_code_with_range:
                                    if bool(re.search(r"^\d{2}-\d{2}$", value)): #encoded with range
                                        sub863[code] = value.strip()
                                        description = range_parser(sub863, value.strip(), False)+":"
                                    elif value.strip() in seasons: # incase only encoded with no range
                                        value = seasons[value.strip()]  
                                        sub863[code] = value.strip() #str[:1] + value.strip() + str[-1]
                                        description = description+f"{sub863[code]}:"                                     
                                else:
                                    if value.strip() in seasons and "-" in value: #encoded with range
                                        sub863[code] = seasons[value.strip()]  
                                    elif value in seasons: # incase only encoded with no range  
                                        sub863[code] = seasons[value].strip() #str[:1] + value.strip() + str[-1]   
                                    elif "-" in value: # incase season names are already written
                                        sub863[code] = value.strip()     
                            elif "season" in str:
                                if value.strip() in seasons:
                                    sub863[code] = seasons[value.strip()]
                                    description = description+f"{sub863[code]}:"   
                                else:
                                    sub863[code] = value.strip()
                                    description = description+f"{sub863[code]}:"     

                            if "date" in str and "-" in value:
                                if code == last_code_with_range:
                                    if "-" in value :
                                        sub863[code] = value.strip()
                                        description = range_parser(sub863, value.strip(), False)+":"
                                    else:
                                        sub863[code] = value.strip() #str[:1] + value.strip() + str[-1]
                                        description = description+f"{sub863[code]}:"
                                else:
                                    sub863[code] = value
                            elif "date" in str:
                                sub863[code] = value.strip()
                                description = description+f"{sub863[code]}:"

                        else:
                            if "v" in str and "." not in str:
                                sub863[code] = sub853[code]+"."+value.strip()
                                description = description+f"{sub863[code]}:"
                            else:
                                sub863[code] = sub853[code]+value.strip()
                                description = description+f"{sub863[code]}:"

            description_fields.append(Field(tag='866', indicators=indicators, subfields=[Subfield('a', description[:-1]), Subfield('8', field8)]))
            description = ""
            # print(f" description_fields: { description_fields}")
    return description_fields

def range_parser(sub863, val, tag):
    
    month_abbreviations = {'01': 'Jan.','1': 'Jan.', 
                           '02': 'Feb.','2': 'Feb.', 
                           '03': 'Mar.','3': 'Mar.',
                           '04': 'Apr.','4': 'Apr.',
                           '05': 'May','5': 'May',
                           '06': 'Jun.','6': 'Jun.',
                           '07': 'Jul.','7': 'Jul.',
                           '08': 'Aug.','8': 'Aug.',
                           '09': 'Sep.','9': 'Sep.',
                           '10': 'Oct.','11': 'Nov.','12': 'Dec.',
                           '21':'spring', '22':'summer', '23':'autumn', '24':'winter'}
    seasons = {'21':'spring', '22':'summer', '23':'autumn', '24':'winter'}
    
    desc = ""
    range_parts = val.split('-')
    start_date = range_parts[0].strip()
    end_date = range_parts[1].strip()
    start_y, start_no, start_v, r1, end_y, end_no, end_v, r2 = "", "", "", "", "", "", "", ""
    for c, v in sub863.items():
        if bool(re.search(r"^\d{4}-\d{4}$", v)): #checks if string has more than 4 digits (then it's a year)
            ysplit = v.split('-')
            start_y = ysplit[0].strip()
            end_y = ysplit[1].strip()
            v = start_y
        
        if "no." in v and "-" in v:

            nsplit = v.split('-')
            start_no = nsplit[0].strip()
            end_no = nsplit[1].strip()
            v = start_no
        
        if "v." in v and "-" in v:
            vsplit = v.split('-')
            start_v = vsplit[0].strip()
            end_v = vsplit[1].strip()
            v = start_v
        
        if bool(re.search(r"^\d{2}-\d{2}$", v)) or (tag == True and "-" in v):
            split = v.split('-')
            r1 = split[0].strip()
            r2 = split[1].strip()
            if r1 in seasons and r2 in seasons:
                v = seasons[r1]
                r2 = seasons[r2]
            elif r1 in month_abbreviations and r2 in month_abbreviations:
                v = month_abbreviations[r1]
                r2 = month_abbreviations[r2]
            if tag:
                v = r1
         
        if bool(re.search(r'/', v)) and bool(re.search(r'/', val)):
            v = range_parts[0]

        desc += v+":"
    desc = desc[:-1] 
    desc+= "-" #start_date + "-" 
    
    for c, v in sub863.items():
        if bool(re.search(r"^\d{4}-\d{4}$", v)): #checks if string has more than 4 digits (then it's a year)
            desc += end_y+":"
            continue

        if "no." in v and "-" in v:
            desc += "no."+end_no+":"
            continue
        
        if "v." in v and "-" in v:
            desc += "v."+end_v+":"
            continue

        if bool(re.search(r"^\d{2}-\d{2}$", v)) or (tag == True and "-" in v):
            desc += r2+":"
            continue

        if bool(re.search(r'/', v)) and bool(re.search(r'/', val)):
            desc += range_parts[1]+":"
            continue

        desc += v+":"
    return desc[:-1]
                        
def process_mrk_file(input_file, txt_op, mrc_op, skip_op):
    fix = 0
    rcount = 0
    count853, count863, count866 = 0, 0, 0
    with open(input_file, 'rb') as file:
        reader = MARCReader(file)
        with open(txt_op, 'w', encoding='utf-8') as txt_op, open(mrc_op, 'wb') as mrc_op, open(skip_op, 'wb') as skip_op:
            mwriter = MARCWriter(mrc_op)
            swriter = MARCWriter(skip_op)
            
            for record in reader:
                rcount +=1
                print(f"\n##################### Processing Record No. {rcount} ##################### ")
                
                all_853 = record.get_fields('853')
                if len(all_853) > 1:   
                    lesser_subfields_853 = all_853[0]
                    for field in all_853[1:]:
                        if len(field.subfields) < len(lesser_subfields_853.subfields):
                            lesser_subfields_853 = field
                    # Remove the 853 field with fewer subfields
                    record.remove_field(lesser_subfields_853)

                if record.get_fields('853') and record.get_fields('863'):                        
                    # Check if record already contains $866 fields
                    if record.get_fields('866'):
                        count866 +=1
                        # Remove existing 866 fields from the record
                        for f in record.get_fields('866'):
                            record.remove_field(f)

                    # Extract subfields from each $853 field
                    subfields_array = extract_subfields(record)
                    # Generate $866 fields based on existing $853 and $863 fields
                    description_fields = generate_description_field(record, subfields_array)
                    print(f"Generating 866 fields...\n")
                    # Collect all 863 fields with their index in the record fields list
                    last_863_index = -1
                    for idx, field in enumerate(record):
                        if field.tag == '863':
                            last_863_index = idx
                    # Insert 866 fields after the last 863 field if found
                    if last_863_index != -1:
                        # record.add_fields(description_fields, prepend=False)
                        for idx, field in enumerate(description_fields):
                            record.fields.insert(last_863_index + 1 + idx, field)

                    # Write modified record to output file
                    txt_op.write(str(record) + '\n')
                    mwriter.write(record)
                else:
                    if record.get_fields('853'):
                        count863 +=1
                        print(f"Record has missing 863 fields  :(\n")
                    else:
                        count863 +=1
                        count853 +=1
                        print(f"Record has missing 853 & 863 fields  :(\n")
                    # Write the record as it is if it does not have 853 or 863 fields
                    fix +=1 
                    txt_op.write(str(record) + '\n')
                    mwriter.write(record)
                    swriter.write(record)
                    continue
    print("\n### TASK COMPLETED ###\n")
    print(f"\nTotal Records Processed: {rcount}")
    print(f"\nRecords with missing 853: {count853}")
    print(f"\nRecords with missing 863: {count863}")
    print(f"\n!!! NOTE: Total {fix} records had missing fields !!!")
                
if __name__ == "__main__":
    try:
        print("~~~ Welcome to MarcGenie! ~~~\n")
        filepath = sys.argv[1]
        # filepath = askopenfilename()
        # filename = os.path.basename(filepath)
        print(f"Your chosen file: {filename}\n")

        outputfile = sys.argv[2]
        # root = tk.Tk()
        # root.withdraw()
        # outputfile = simpledialog.askstring("User Input", "Please name your output file: ")
        print(f"You entered: {outputfile}")
        txt_op = outputfile+'.txt'
        mrc_op = outputfile+'.mrc'
        skip_op = outputfile+'SkippedRecords.mrc'
        print(f"Text file: {txt_op}, Marc file: {mrc_op} Created.")
        process_mrk_file(filepath, txt_op, mrc_op, skip_op)
        print(f"\n(Find the skipped records in file '{skip_op}')")
        print(f"\n(Results have been generated in files '{txt_op}' & '{mrc_op}')")
    except Exception as e:
        raise e
    finally:
        print("\n~~~ Thank you for using MarcGenie! ~~~")
