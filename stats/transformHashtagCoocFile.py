import logging
import sys

if __name__ == '__main__':
    logger = logging.getLogger("transformHashtagCoocFile.py")
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s;%(levelname)s;%(message)s")

    if len(sys.argv) != 3:
        print "You need to pass the following 2 params: <inputFile> <outputFile>"
        sys.exit(-1)
    inputFile = sys.argv[1]
    outputFile = sys.argv[2]

    output = open(outputFile, "w")

    # line example
    # #truth  22      Neutral:19 Pro:3        #refugees,#refugeescrisis,#refugeesnotpawns,#syrianrefugees     34783
    for line in open(inputFile):
        lineData = line.split('\t')
        partialFreq = lineData[2].split(' ')
        pos = '0'
        neg = '0'
        neu = '0'
        for item in partialFreq:
            if "Pro" in item:
                pos = item.split(':')[1]
            if "Anti" in item:
                neg = item.split(':')[1]
            if "Neutral" in item:
                neu = item.split(':')[1]
        lineData[2] = pos + '\t' + neg + '\t' + neu
        lineData[3] = lineData[4]
        output.write('\t'.join(lineData[:4]))

    output.close()
    logger.info('Finished transforming the file')
