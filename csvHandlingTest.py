from csvHandling import *
assert(csvINIT())
myData = csvData("1", "2", "3", "4", "5", "6", "7", "8", "9")

assert(type(myData) == csvData)
assert(myData.exportList()==["1", "2", "3", "4", "5", "6", "7", "8", "9"])

csvInsert(myData)

csvRemove(myData)