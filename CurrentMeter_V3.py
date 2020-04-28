import time
import serial
import random

# 搜尋可用com port
import serial.tools.list_ports

class CurrentOperate:
    def __init__(self):
        self.refVoltage = 3.3
        self.ADCresolution = 10
        self.voltageScale = self.refVoltage / (2**self.ADCresolution)
        self.sampleResistor = 10    #ohm
        self.currentTable = []
        self.tatalmAmS = 0
        self.totalmAH = 0

    def get_mA(self, adcValue):
        _voltage = round(adcValue * self.voltageScale, 6)
        _current = round(_voltage / self.sampleResistor, 6)
        _current = round(_current * 1000, 6)                  #change unit from A to mA
        return _current

    def get_TotalmAmS(self, currentTable):
        self.currentTable = currentTable
        _tatalmAmS = 0
        # _mS = 1 / (343 / 1000)
        _mS = (343/1000) / 1    # 每一個 sample time佔 1ms的多少
        maxCurrent = (self.refVoltage / self.sampleResistor) * 1000     # mA
        for _current in self.currentTable:
            data = _current.split(", ")
            _current = float(data[3].replace(" mA", ""))
            if _current < maxCurrent:
                # mAmS = _current / _mS
                mAmS = _current * _mS   # 此次 sample current乘上取樣時間在 1ms的佔比, 即為每 1ms的電流
                _tatalmAmS += mAmS
        self.tatalmAmS = round(_tatalmAmS, 6)
        return self.tatalmAmS

    def get_TotalmAH(self, tatalmAmS):
        _totalmAH = (tatalmAmS / 1000) / 3600   # 先將 mAmS轉換為 mAS, 再轉換為 mAH
        self.totalmAH = format(_totalmAH, '.10f')
        return self.totalmAH

    def writeToFile(self, fileName):
        passFirstData = True
        _date = self.currentTable[0].split(', ')[0]
        _time = self.currentTable[0].split(', ')[1]
        f = open(filename, 'a+')
        f.write(self.currentTable[0] + "\n")
        for currentData in self.currentTable:
            currentData = currentData.split(", ")
            current = float(currentData[3].replace(" mA", ""))
            if current < 330:
                if passFirstData:
                    passFirstData = False
                else:
                    writeData = '-, -, ' + currentData[2] + ', ' + currentData[3]
                    f.write(writeData + "\n")

        writeData = _date + ", " + _time + ", 0 mS, 0 mA, " + str(self.tatalmAmS) + ' mAmS, ' + str(self.totalmAH) + ' mAH'
        f.write(writeData + "\n")
        f.close()


class TimeCtrl:
    def __init__(self):
        self.sampleEveryMicroSecond = 343
        self.tag = 0
        self.count = 0
        self.timeOut = 0.3

    def getCount(self):
        _tmp = self.count
        self.count += 1
        return _tmp

    def clrTag(self):
        self.count = 0
        self.tag = 0

    def updateTag(self):
        self.tag = str(round(((self.getCount() * self.sampleEveryMicroSecond) / 1000), 6))
        return self.tag

    def getTime(self):
        return time.strftime("%Y/%m/%d, %H:%M:%S", time.localtime())


coms = serial.tools.list_ports.comports()
for a in coms:
    print(a)

ser = serial.Serial('COM27', 115200, timeout=1)
ser.flushInput()
ser.set_buffer_size(rx_size=1000000)
ser.isOpen()

adcValue = 0
currentLevel = 2  # mA

# timeTag = 0
# dataCount = 0
# count = 0
# voltageSum = 0
# sampleCount = 1
# showCurrent = 0
# voltage = 0
tStart = time.time()
currentTable = []
# lastlocalTime = ""
# newDataFlag = True
# zeroCount = 0
# timeShow = False
# oldTimeTag = 0
# tStart0 = time.time()
# pEND1 = time.time()
# continueTime = 0
# state = 0
# exeOnlyOneTime = True

print('===========================================')
print('===========================================')
print('===========================================')
current = CurrentOperate()
timeCtrl = TimeCtrl()
ser.flushInput()
filename = "CurrentV4_" + time.strftime("%Y%m%d%H%M", time.localtime()) + ".txt"
# filename = "CurrentV4.txt"
f = open(filename, 'w')
f.close()

try:
    while True:
        # if state == 0:
        #     continueTime = 1 * 60 * 60
        #     #continueTime = 30
        #     pEND = time.time()
        #     if exeOnlyOneTime:
        #         exeOnlyOneTime = False
        #         filename = "Current_" + time.strftime("%Y%m%d%H%M", time.localtime()) + "_T3.txt"
        #         f = open(filename, 'w')
        #         f.close()
        #         print(filename)
        #     if (pEND - tStart0) > continueTime:
        #         #pEND1 = time.time()
        #         #state = 4
        #         #exeOnlyOneTime = True
        #         break
        """elif state == 1:
            continueTime = (23 * 60 * 60) + (55 * 60)
            # continueTime = 5*60
            while ((pEND1 - pEND) < continueTime):
                pEND1 = time.time()
                print("Wait-- " + str(time.strftime("%H:%M:%S", time.localtime())))
                time.sleep(60)
            pEND1 = time.time()
            state = 2

        elif state == 2:
            continueTime = 48 * 60 * 60
            pEND = time.time()
            if exeOnlyOneTime:
                exeOnlyOneTime = False
                filename = "Current_" + time.strftime("%Y%m%d%H%M", time.localtime()) + "_T1T2.txt"
                f = open(filename, 'w')
                f.close()
                print(filename)
            if (pEND - tStart1) > continueTime:
                pEND1 = time.time()
                state = 3
                exeOnlyOneTime = True

        elif state == 3:
            continueTime = 72 * 60 * 60
            pEND = time.time()
            if exeOnlyOneTime:
                exeOnlyOneTime = False
                filename = "Current_" + time.strftime("%Y%m%d%H%M", time.localtime()) + "_T3.txt"
                f = open(filename, 'w')
                f.close()
                print(filename)
            if (pEND - tStart1) > continueTime:
                pEND1 = time.time()
                state = 4
                exeOnlyOneTime = True
                break

        elif state == 4:
            break"""

        if ser.in_waiting:
            goodADCvalue = True
            rawData = ser.readline()
            try:
                adcValue = (rawData[0] * 256) + rawData[1]
            except:
                goodADCvalue = False
                print('Try again')

            if goodADCvalue:
                newCurrent = current.get_mA(adcValue)
                localTime = timeCtrl.getTime()
                if newCurrent > currentLevel:
                    # print(newCurrent)
                    tStart = time.time()

                    #
                    # if newDataFlag == True:
                    #     localTime = time.strftime("%Y/%m/%d, %H:%M:%S", time.localtime())
                    #     lastTime = localTime.split(", ")
                    #     lastTime = lastTime[1]
                    #     newDataFlag = False
                    # else:
                    #     localTime = "-, -"
                    #
                    # if timeShow == True:
                    #     localTime = time.strftime("%Y/%m/%d, %H:%M:%S", time.localtime())
                    #     lastTime = localTime.split(", ")
                    #     lastTime = lastTime[1]
                    #     timeShow = False
                    # else:
                    #     if (float(timeTag) - oldTimeTag) >= 1000:
                    #         timeShow = True
                    #         oldTimeTag = float(timeTag)
                    #
                    timeCtrl.updateTag()
                    showData = localTime + ", " + str(timeCtrl.tag) + " mS, " + str(newCurrent) + " mA"
                    currentTable.append(showData)
                    #
                    # # print(showData)
                    #

                    # if dataCount > 291550:
                    #     tatalmAmS = 0
                    #     f = open(filename, 'a+')
                    #     for i in currentTable:
                    #         data = i.split(", ")
                    #         current = float(data[3].replace(" mA", ""))
                    #         if current < 330:
                    #             mAmS = current / (1 / (sampleEveryMicroSecond / 1000))
                    #             tatalmAmS += mAmS
                    #             f.write(i + "\n")
                    #
                    #     tatalmAmS = round(tatalmAmS, 6)
                    #     totalmAH = (tatalmAmS / 1000) / 3600
                    #     totalmAH = format(totalmAH, '.10f')
                    #
                    #     f.write(data[0] + ", " + lastTime + ", " + timeTag + " mS, 0 mA, " + str(
                    #         tatalmAmS) + " mA/mS, " + str(totalmAH) + " mAH")
                    #     f.write("\n")
                    #
                    #     f.close()
                    #     currentTable.clear()
                    #     newDataFlag = True
                    #     ser.flushInput()
                    #
                    #     print("Time= " + time.strftime("%Y/%m/%d, %H:%M:%S", time.localtime()))
                    #     print("dataCount= " + str(round(((dataCount * sampleEveryMicroSecond) / 1000), 6)) + "ms")
                    #     dataCount = 0
                    #     print(str(tatalmAmS) + " mA/mS")
                    #     print(str(totalmAH) + " mAH")
                    #     print("Write to File")
                    #     print("")
                    #
                    # zeroCount = 0
                else:
                    tEnd = time.time()
                #     tatalmAmS = 0
                #     zeroCount += 1
                #     # if (tEnd - tStart) > timeOut or zeroCount > int((timeOut * 1000) / (sampleEveryMicroSecond / 1000)):
                    if (tEnd - tStart) > timeCtrl.timeOut and len(currentTable) > 0:
                        tStart = time.time()
                #         zeroCount = 0
                #         print(currentTable)
                        print("Time= " + localTime)
                        print("Data Length= " + str(timeCtrl.tag) + "ms")
                        timeCtrl.clrTag()
                        totalmAmS = current.get_TotalmAmS(currentTable)
                        totalmAH = current.get_TotalmAH(totalmAmS)
                        print(str(totalmAmS) + " mA/mS")
                        print(str(totalmAH) + " mAH")
                        print("Write to File")
                        print("")
                        current.writeToFile(filename)
                        currentTable.clear()

                #             f = open(filename, 'a+')
                #             for i in currentTable:
                #                 data = i.split(", ")
                #                 current = float(data[3].replace(" mA", ""))
                #                 if current < 330:
                #                     mAmS = current / (1 / (sampleEveryMicroSecond / 1000))
                #                     tatalmAmS += mAmS
                #                     f.write(i + "\n")
                #
                #             tatalmAmS = round(tatalmAmS, 6)
                #             totalmAH = (tatalmAmS / 1000) / 3600
                #             totalmAH = format(totalmAH, '.10f')
                #
                #             if timeTag!='0.0':
                #                  f.write(data[0] + ", " + lastTime + ", " + timeTag + " mS, 0 mA, " + str(
                #                      tatalmAmS) + " mA/mS, " + str(totalmAH) + " mAH")
                #                  f.write("\n")
                #
                #
                #                  currentTable.clear()
                #                  newDataFlag = True
                #                  ser.flushInput()
                #
                #                  print("Time= " + time.strftime("%Y/%m/%d, %H:%M:%S", time.localtime()))
                #                  print("dataCount= " + str(round(((dataCount * sampleEveryMicroSecond) / 1000), 6)) + "ms")
                #                  dataCount = 0
                #                  print(str(tatalmAmS) + " mA/mS")
                #                  print(str(totalmAH) + " mAH")
                #                  print("Write to File X")
                #                  print("")
                #             f.close()
                # count = 0
                # voltageSum = 0



except KeyboardInterrupt:
    ser.close()  # 清除序列通訊物件
    print('再見！')

ser.close()  # 清除序列通訊物件
print('再見！')
