from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

import csv

def main(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()


    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
#    txtfile = open(path + "Phase0","w")    #write raw text to file for checking
#    txtfile.write(text)
#    txtfile.close()
    
    rundate = ''
    row = []
    NameMode = False
    AfterEmptyRow = False
    EmployeeIDMode = False
    
    AmountMode4 = False
    AmountMode3 = False
    AmountMode2 = False
    AmountMode = False
    AmountMode0 = False
    path = path.replace('pdf', 'csv') #replacing file name extension
    
    f = open(path, 'wb') #writig to csv logic
    
    EmployeeIDs = []
    Names = []
    SocSecNums = []
    CurrentAmounts = []
    
    try:
        lines = text.split("\n")
        for idx, line in enumerate(lines):
            if line[:9] == 'RUN DATE:':
                rundate = line[10:] #this date might be usefull
                continue
                
            if len(line) == 9 and line.isdigit():
                EmployeeIDs.append(line.strip())
                EmployeeIDMode = True
                continue
            
            if line[:7] == '***-**-':
                SocSecNums.append(line.strip())
                continue
            
            if line[:4] == 'Goal':
                AmountMode4 = True
                
            if AmountMode4 and len(line) == 0:
                AmountMode3 = True
                
            if AmountMode3 and line[:6] == 'Amount':
                AmountMode2 = True
                
            if AmountMode2 and len(line) == 0:
                AmountMode = True
                
            if AmountMode and len(line) != 0:
                CurrentAmounts.append(line.strip())
                AmountMode0 = True
                
            if AmountMode0 and len(line) == 0:
                    AmountMode4 = False
                    AmountMode3 = False
                    AmountMode2 = False
                    AmountMode = False
                    AmountMode0 = False
                
 
            if EmployeeIDMode and AfterEmptyRow:
                NameMode = True
                AfterEmptyRow = False
                EmployeeIDMode = False

            if len(line) == 0:
                AfterEmptyRow = True
                continue
            else:
                AfterEmptyRow = False
                
            if line == 'Ben':
                NameMode = False
                continue
                
            if NameMode and line[:11] != 'Note - an *':
                Names.append(line.strip())
                continue
 
            
        #write names in csv format
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        #header = ['Employee ID', 'Name', 'Soc Sec Num', 'Ben Rcd', 'Current Amount', 'Refund Amount', 'Amt. From Arrears', 'Amount Not Taken', 'Reason Not Taken', 'Month To-Date', 'Quarter To-Date', 'Year To-Date', 'Goal Amount']
        header = ['Employee ID', 'Name', 'Soc Sec Num', 'Current Amount']
        writer.writerow(header)
        for idx, EmployeeID in enumerate(EmployeeIDs):
            row.append(EmployeeID)
            row.append(Names[idx])
            row.append(SocSecNums[idx])
            row.append(CurrentAmounts[idx])
            writer.writerow((row))
            row = []
    finally:
        f.close()

#    print EmployeeIDs
#    print Names
#    print SocSecNums
#    print CurrentAmounts
    #Validation code
    if len(EmployeeIDs) == len(Names) and len(Names) == len(SocSecNums) and len(SocSecNums) == len(CurrentAmounts):
        print 'Export successful'
    else:
        print 'Something went wrong'
    
    return #text