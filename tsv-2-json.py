import os

# these don't need to be global but it makes me feel better :)
# columns that should be arrays
arrayCols = ["primaryProfession", "knownForTitles", "genres", "characters"]


def tsvToJson(filename):
    global arrayCols
    
    print("processing file " + filename + "...")

    dataFile = open(filename, "r", encoding="utf-8")
    jsonFile = open(filename.rstrip("tsv") + "json", "w", encoding="utf-8")
    
    # first line dictates what fields are
    fields = dataFile.readline().strip().split("\t")
    # reduce checking array columns to true/false, so python isn't checking strings 1000s of times
    isArrayCol = []
    for field in fields:
        if field in arrayCols:
            isArrayCol.append(True)
        else:
            isArrayCol.append(False)
    
    jsonFile.write("[\n")
    
    # dirty way of not leaving a hanging comma at eof lol
    shouldComma = False
    
    # sequentially process every document
    for line in dataFile:
        doc = line.strip().split("\t")
        writeStr = ""
        if shouldComma:
            writeStr = writeStr + ",\n" # only "required" newline, so to speak
        else:
            shouldComma = True
        writeStr = writeStr + "{" # optional newline after
        
        # do every field
        for i in range(len(fields)):

            if isArrayCol[i]: # if field should be an array
                if "[" in doc[i] or "]" in doc[i]: # imdb randomly decides to use [] to denote arrays in principals
                    pass
                else:
                    doc[i] = doc[i].split(",").__repr__().replace("\'", "\"")
                
            elif doc[i].isdigit(): # if field is a number
                # get rid of pesky trailing 0s
                while doc[i][0] == "0" and len(doc[i]) > 1:
                    doc[i] = doc[i][1:]
                
            elif doc[i] == "\\N":
                doc[i] = "null"
                
            else:
                # because for some reason imdb thinks putting " in names is funny
                doc[i] = doc[i].replace("\"", "\'")
                doc[i] = "\"" + doc[i] + "\""
                
            writeStr = writeStr + fields[i].__repr__().replace("\'", "\"") + ": " + doc[i] + "," # optional newline after
        
        # cleanup writeStr
        writeStr = writeStr.rstrip(",") # remove trailing comma, optional newline after
        # writeStr = writeStr.replace("\'", "\"") # replace single quote with double quote for json; this messes up names
        # writeStr = writeStr.replace("\"\\\\N\"", "null") # replace \N with null for json
        writeStr = writeStr + "}" # add closing bracket, comma, optional newline BEFORE
        jsonFile.write(writeStr)

    jsonFile.write("\n]\n") # closing bracket
    
    dataFile.close()
    jsonFile.close()
    
    
def main():
    fileNames = ["name.basics.tsv", "title.basics.tsv", "title.principals.tsv", "title.ratings.tsv"]
    
    for name in fileNames:
        tsvToJson(name)
    
    print("done!")
    
    
if __name__ == "__main__":
    main()