from openpyxl import Workbook
import os
import re
from csvHandling import csvData

#given a list of data, appends data to the end of the active sheet in the workbook
def expAppend(workbook: Workbook, listData: list[csvData]) -> None:
    for data in listData:
        workbook.active.append(data.exportList())

#returns True if workbook exists, False otherwise
def expCheck(name: str) -> bool:
    splitted = name.split(".")
    return os.path.exists(splitted[0])

#Saves the Workbook with the given name returning True, if it can't, return False
def expSave(workbook: Workbook, name: str) -> bool:
    WINDOWS_FILENAME_REGEX = re.compile(r'^(?!^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])$)'  # Disallow reserved names
                                        r'[^<>:"/\\|?*\x00-\x1F]+'  # Ensure no invalid characters
                                        r'(?:\.xlsx)?$' ) # Allow only .xlsx extension or no extension at all
    if not bool(WINDOWS_FILENAME_REGEX.match(name)) or len(name) >= 255:
        return False

    result = 2 if name.endswith(".xlsx") else 1

    if result==1:
        workbook.save(name+".xlsx")
    elif result==2:
        workbook.save(name)
    
    return result>0

