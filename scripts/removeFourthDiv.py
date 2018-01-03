spaceList = []
with open("spanless.jade") as file:
    lineList = file.readlines()
    for i in range(len(lineList)):
        line = lineList[i]
        firstChar = line.strip()[0]
        firstChar_position = line.find(firstChar)
        #print firstChar_position, line
        if firstChar == "d" and line.strip() != "div" and firstChar_position > 6:
            print firstChar_position, line
            spaceList.append(firstChar_position)

print min(spaceList)
print max(spaceList)
