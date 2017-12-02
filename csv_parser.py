import csv
import fileinput
import sys
from tabulate import tabulate

debug = True

def main():
    try:
        if len(sys.argv) == 1:
            #filename = "test.csv"
            filename = input("CSV file name = ")
        elif len(sys.argv) == 2:
            filename = str(sys.argv[1])
        elif len(sys.argv) > 2:
            print ("Specify just one CSV file as command line argument")
            return

        ### MENU
        printMenu()

        while(True):
            menu = input("\nChoose operation number: ")
            if menu == '0':
                ### necessary if delimiter is ";" instead of ','
                searchExp = ";"
                replaceExp = ","
                replaceAll(filename,searchExp,replaceExp)

            elif menu == '1':
                ### print column titles
                columnList = getColumnTitles(filename)
                print("\nColumn list:")
                i=0
                for col in columnList:
                    i += 1
                    print("col"+str(i)+": "+col)

            elif menu == '2':
                colIndex = input('column index list (from 1, separated by comma): ') 
                keywords = input('keyword(s): ')
                if colIndex == '':
                    ### find rows by keyword list:
                    findRowByKeywordList(filename, keywords)
                else:
                    ### find rows by column index and keyword list:
                    findRowByColumnAndKeywordList(filename, colIndex, keywords)

            elif menu == '3':
                colIndex = input('column index list (from 1, separated by comma): ')
                keywords = input('keyword(s): ')
                if colIndex == '':
                    ### find rows by keyword list:
                    findRowByKeywordList_subs(filename, keywords)
                else:
                    ### find rows by column index and keyword list:
                    findRowByColumnAndKeywordList_subs(filename, colIndex, keywords)
                
            elif menu == '4':
                ### print a table from the CSV file
                printTable(filename)

            elif menu == '5':
                print ("Not yet implemented")

            elif menu == '6':
                print ("Not yet implemented")

            elif menu == '7':
                print ("Not yet implemented")

            elif menu == '8':
                print ("Not yet implemented")

            elif menu == '9':
                print ("Not yet implemented")

            elif menu == 'm':
                printMenu()

            else:
                print ("Unknown choice")
                return  
        
    except KeyboardInterrupt:
        ### to intercept CRTL+C interrupt 		
        print ("\nQuitting...")
    except Exception as e:
        print("Exception: " + repr(e))
        
    

def getColumnTitles(filename):
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        firstRow = next(reader)
        columnList = firstRow.keys()
        return columnList

def findRowByKeywordList(filename, keywords):
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        keywordList = keywords.split(",")
        keywordListUp = [kw.strip().upper() for kw in keywordList if kw is not None] #list uppercase
        print ("searching for: ", keywordListUp)
        firstRow = True
        for row in reader:
            if firstRow:
                firstRow = False
                columnTitles = row.keys()
                print (columnTitles)
            row_keys = row.keys()
            row_keys = [k.strip().upper() for k in row_keys if k is not None]
            row_values = row.values()
            row_values = [v.strip().upper() for v in row_values if v is not None]
            for kw in keywordListUp:
                if kw in row_values:
                    print (row.values())

def findRowByColumnAndKeywordList(filename, colIndexList, keywords):
    colIndexList = colIndexList.split(",")
    colIndexList = [int(c)-1 for c in colIndexList if c is not None]
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        keywordList = keywords.split(",")
        keywordListUp = [kw.strip().upper() for kw in keywordList if kw is not None] #list uppercase
        print ("searching for: ", keywordListUp)
        firstRow = True
        for row in reader:
            if firstRow:
                firstRow = False
                columnTitles = row.keys()
                if max(colIndexList) > len(columnTitles):
                    raise ValueError('Wrong index value specified')
                print (columnTitles)
            row_keys = row.keys()
            row_keys = [k.strip().upper() for k in row_keys if k is not None]
            row_values = row.values()
            row_values = [v.strip().upper() for v in row_values if v is not None]
            for kw in keywordListUp:
                for colIndex in colIndexList:
                    if kw == row_values[colIndex]:
                        print (row.values())

def findRowByKeywordList_subs(filename, keywords):
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        keywordList = keywords.split(",")
        keywordListUp = [kw.strip().upper() for kw in keywordList if kw is not None] #list uppercase
        print ("searching for: ", keywordListUp)
        firstRow = True
        for row in reader:
            if firstRow:
                firstRow = False
                columnTitles = row.keys()
                print (columnTitles)
            row_keys = row.keys()
            row_keys = [k.strip().upper() for k in row_keys if k is not None]
            row_values = row.values()
            row_values = [v.strip().upper() for v in row_values if v is not None]
            for kw in keywordListUp:
                for v in row_values:
                    if kw in v:
                        print (row.values())

def findRowByColumnAndKeywordList_subs(filename, colIndexList, keywords):
    colIndexList = colIndexList.split(",")
    colIndexList = [int(c)-1 for c in colIndexList if c is not None]
    print(colIndexList)
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        keywordList = keywords.split(",")
        keywordListUp = [kw.strip().upper() for kw in keywordList if kw is not None] #list uppercase
        print ("searching for: ", keywordListUp)
        firstRow = True
        for row in reader:
            if firstRow:
                firstRow = False
                columnTitles = row.keys()
                if max(colIndexList) > len(columnTitles):
                    raise ValueError('Wrong index value specified')
                print (columnTitles)
            row_keys = row.keys()
            row_keys = [k.strip().upper() for k in row_keys if k is not None]
            row_values = row.values()
            row_values = [v.strip().upper() for v in row_values if v is not None]
            for kw in keywordListUp:
                for colIndex in colIndexList:
                    if colIndex >= len(row_values):
                        break
                    elif kw in row_values[colIndex]:
                        print (row.values())

def printTable(filename):
    columnTitles = getColumnTitles(filename)
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        row_list = []
        for row in reader:
            element_list = []
            for element in row.values():
                element_list.append(element)
            row_list.append(element_list)
        print (tabulate(row_list, headers=columnTitles))
        

def listToArray(inputList):
    outputArray = [len(inputList)]
    i = 0
    for element in inputList:
        outputArray.append(element)
        i = i + 1
    debugPrint (outputArray)
    return outputArray

def replaceAll(file,searchExp,replaceExp):
    for line in fileinput.input(file, inplace=1):
        if searchExp in line:
            line = line.replace(searchExp,replaceExp)
        sys.stdout.write(line)

def printMenu():
    menu = """\n**********MENU**********
1) print column titles
2) search list of keywords
3) search list of keywords considering substrings
4) print table from CSV
5) 
6)
7)
8)
9)
0) replace ';' with ','
m) print menu"""
    print (menu)

def debugPrint(x):
    if debug:
        print (x)


if __name__ == "__main__":
	main()
