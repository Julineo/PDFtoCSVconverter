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
    pagenos=set()

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
    rowscount = 0
    totalemployees = 0  #variable for validation
    namesmode = False
    even = False
    path = path.replace('pdf', 'csv') #replacing file name extension
    
    f = open(path, 'wb') #writig to csv logic
    try:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        header = ['EMPLOYEE NAME', 'DEPARTMENT NAME', 'POSITION CODE', 'POSITION DESCRIPTION', 'DATE', 'YEARS', 'JOB STAT', 'SCH HRS', 'SHIFT', 'PAY RATE', 'XSSN', 'addressLine1', 'addressLine2', 'city', 'state', 'zipCode']
        writer.writerow(header)        
        
        lines = text.split("\n")
        for idx, line in enumerate(lines):
            if len(line) == 0:
                continue
            if line[:9] == 'RUN DATE:':
                rundate = line[10:] #this date might be usefull
            if line[:9] == '*********': #beginning of a block of a names chank
                namesmode = True
                even = True
                continue
           
            if line[:1] == 'B' and len(line) == 1:
                namesmode = False
                continue
            if line[:15] == 'TOTAL EMPLOYEES':
                namesmode = False
                totalemployees = int(line[34:])
                break
    
            #write names in csv format
#            templine = "         XXX-XX-8073                 191 EASTERN AVE                                         BREWER, ME  04412-1300"
#            print templine[-5:-4]
            if namesmode and even:
                row.append(line[:33].strip())
                row.append(line[33:64].strip())
                row.append(line[64:77].strip())
                row.append(line[77:105].strip())
                row.append(line[105:117].strip())
                row.append(line[117:130].strip())
                row.append(line[130:134].strip())
                row.append(line[134:139].strip())
                row.append(line[139:143].strip())
                row.append(line[143:].strip())
            if namesmode and not(even):
                row.append(line[5:33].strip())
                row.append(line[33:61].strip())
                row.append(line[61:89].strip())
#                if line[-5:-4] == '-':
#                    row.append(line[89:-14].strip())
#                    row.append(line[-14:-12].strip())
#                    row.append(line[-10:].strip())
#                else:
#                    row.append(line[89:-11].strip())
#                    row.append(line[-9:-7].strip())
#                    row.append(line[-5:].strip())
                commaindex = line[89:].index(",")
                row.append(line[89:89+commaindex].strip())
                row.append(line[89+commaindex+1:89+commaindex+1+3].strip())
                row.append(line[89+commaindex+1+4:].strip())
                writer.writerow((row))
                rowscount += 1
                row = []
                           
            even = not(even)        
         
    finally:
        f.close()

    #Validation code
    if totalemployees > 0 and rowscount == totalemployees:
        print 'Export successful'
    else:
        print 'Something went wrong'
    
    return #text