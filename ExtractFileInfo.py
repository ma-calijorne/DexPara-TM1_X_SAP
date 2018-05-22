import csv

TM1List = []
SAPList = []

class TM1Regs:

    PEP=""
    Descricao=""
    Fornecedor=""

class SAPRegs:

    Descricao=""

def ExtractTM1Info():

    with open('Dados/ArquivoTM1.csv', 'rb') as csvfile:

        TM1File = csv.reader(csvfile, delimiter=',', quotechar='|')
        bTitle = True
        for eachRow in TM1File:
            if bTitle == True:
                bTitle = False
            else:
                TM1Obj = TM1Regs()
                TM1Obj.PEP = eachRow[0].decode("cp1252").upper()
                TM1Obj.Descricao = eachRow[1].decode("cp1252").upper()
                TM1Obj.Fornecedor = eachRow[2].decode("cp1252").upper()
                TM1List.append(TM1Obj)

    csvfile.close()
    return TM1List

def ExtractSAPInfo(arValuesWithoutMatch):
    bTitle = True
    for eachSAPItem2 in arValuesWithoutMatch:
        if bTitle == True:
            bTitle = False
        else:
            if len(eachSAPItem2.sSAPLine) > 0:
                SAPObj = SAPRegs()
                SAPObj.Descricao = eachSAPItem2.sSAPLine
                SAPList.append(SAPObj)

    return SAPList
