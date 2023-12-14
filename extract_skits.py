import sys, os
from classes.cvm import Cvm
from classes.iso import Iso
from classes.fps3 import Fps3
from classes.sb7 import Sb7
from compression.complib import decode

ROOT_EXTRACTED_DIRECTORYNAME = 'patch_files'
SKITS_CVM_FILENAME = 'TO7SE.CVM;1'
SKITS_SB7_FILENAME = 'CHTSC.SB7'

def getFileBytes(fileName):
    with open(fileName, "rb") as f:
        return f.read(-1)

def writeFileText(fileName, text):
    with open(fileName, "w") as f:
        f.write(text)

def makeDir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def getSkitFileNames(cvm):
    names = []
    for fileName in cvm.iso.rootFileNames:
        if fileName.endswith('SKT;1'):
            names.append(fileName)
    return names

def getFps3File(cvm, fileName):
    compressedFileData = cvm.iso.get_file_bytes(fileName)
    data = decode(compressedFileData)
    return Fps3(data)

def getReformattedSkitText(skitLinesBytes):
    result = []
    for line in skitLinesBytes:
        decodedLine = line.decode('utf-8', errors="replace")
        decodedLine = decodedLine.replace('\n', '')
        result.append(decodedLine)
    result = '\n'.join(result)
    return result

def run(inputFile):
    baseIso = Iso(getFileBytes(inputFile))

    skitsCvm = Cvm(baseIso.get_file_bytes(SKITS_CVM_FILENAME))
    skitFileNames = getSkitFileNames(skitsCvm)

    fps3FileDict = {}
    for skitFileName in skitFileNames:
        fps3FileDict[skitFileName] = getFps3File(skitsCvm, skitFileName)

    for fps3FileName, fps3File in fps3FileDict.items():
        sb7File = Sb7(fps3File.getFile(SKITS_SB7_FILENAME))
        skitLinesBytes = sb7File.textSets[len(sb7File.textSets)-1]
        reformattedSkitText = getReformattedSkitText(skitLinesBytes)

        dirName = ROOT_EXTRACTED_DIRECTORYNAME + '/' + SKITS_CVM_FILENAME
        makeDir(dirName)
        newFileName = fps3FileName + '.' + SKITS_SB7_FILENAME + ".txt"
        filePath = dirName + '/' + newFileName
        writeFileText(filePath, reformattedSkitText)
        print("Wrote " + newFileName)

    print("Done")

#start
if len(sys.argv) != 2:
    print("Usage: python t.py <input-file>")
else:
    run(sys.argv[1])
