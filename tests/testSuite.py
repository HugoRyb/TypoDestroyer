import os
import subprocess
from subprocess import Popen, PIPE

import time

COMP_BIN_PATH = '../TextMiningCompiler'
APP_BIN_PATH = '../TextMiningApp'

REF_COMP_BIN_PATH = '../ref/bin/linux64/TextMiningCompiler'
REF_APP_BIN_PATH = '../ref/bin/linux64/TextMiningApp'

DICT = '../ref/words.txt'
REF_DICT_BIN = '../ref/dict.bin'
DICT_BIN = 'dict.bin'

TESTS_DIR = './tests_files'

FNULL = open(os.devnull, 'w')


def okko(test):
    return '--> OK' if test else '--> KO'


def test_memory(process):
    ru = os.wait4(process.pid, 0)[2]
    if (ru.ru_maxrss / 1024) > 512:
        print(">> Maximum used memory: %d" % (ru.ru_maxrss / 1024), 'Mo', okko((ru.ru_maxrss / 1024) < 512))
    return ru.ru_maxrss / 1024

def test_comp():
    print('## COMPILER ##')
    start = time.time()
    p = Popen(['/usr/bin/time', '-v', COMP_BIN_PATH, DICT, DICT_BIN],  # ['/usr/bin/time', '-v', 'ls'],
                           stdout=PIPE, stderr=PIPE)
    test_memory(p)
    print(">> Took: " + str(round(time.time() - start, 3)) + "s")


def search(filename, bin, dict_bin):
    start = time.time()
    ps = subprocess.Popen(['cat', filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ps2 = subprocess.Popen([bin, dict_bin], stdin=ps.stdout, stdout=subprocess.PIPE, stderr=FNULL)
    ps.wait()
    memUsed = test_memory(ps2)
    timeUsed = round(time.time() - start, 3)
    _, err = ps.communicate()
    output, _ = ps2.communicate()
    # print(">> Took: " + str(timeUsed) + "s")
    return output.decode('utf-8'), timeUsed, memUsed


def test_search():
    print('## SEARCH ##')

    #Stats
    totalTest, passedTest, memoryGoodTest = 0, 0, 0

    refTimeSum, mineTimeSum, diffTimeSum, percentTimeSum = 0, 0, 0, 0

    files = [TESTS_DIR + f for f in os.listdir(TESTS_DIR) if os.path.isfile(os.path.join('./tests_files', f))]
    for filename in files:
        if filename[-4:] != '.txt':
            continue
        totalTest += 1
        print('# File: ', filename)

        outMine, timeMine, memUsed = search(filename, APP_BIN_PATH, DICT_BIN)
        if memUsed < 512:
            memoryGoodTest += 1

        outRef, timeRef, _ = search(filename, REF_APP_BIN_PATH, REF_DICT_BIN)
        # print(outRef)
        if outRef != outMine:
            print('!! Diff with ref: ', okko(outRef == outMine))
        else:
            passedTest += 1
        refTimeSum += timeRef
        mineTimeSum += timeMine
        diffTimeSum += round(timeMine - timeRef, 3)
        percentTimeSum += round(timeMine / timeRef, 2) * 100
        print('>> Time analysis: Ref', timeRef, 's | Ours', timeMine, 's | Difference',
              round(timeMine - timeRef, 3), 's | Percent perf', round(timeMine / timeRef, 2) * 100, '%')

    print('\n#########\n# RECAP #\n#########')
    print('>> Passed test:', passedTest, '/', totalTest, '(', 100 * passedTest // totalTest, '%)')
    print('>> Memory passed test:', memoryGoodTest, '/', totalTest, '(', 100 * memoryGoodTest // totalTest, '%)')
    print('>> Average Time analysis: Ref', round(refTimeSum / totalTest, 3), 's | Ours', round(mineTimeSum / totalTest, 3),
          's | Difference', round(diffTimeSum / totalTest, 3), 's | Percent perf', round(percentTimeSum / totalTest, 2), '%')

# test_comp()
test_search()