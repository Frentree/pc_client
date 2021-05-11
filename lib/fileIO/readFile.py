import threading
import os.path
import lib.api.er_api as api
import lib.fileIO.trie as trie
import os
import sys

current_location = str(os.path.abspath(os.path.dirname(sys.argv[0])))


def line_formatter(line):
    line = line.replace("\n", "")
    line = line.replace("\\\\", "\\")
    line = list(line.split("\\"))
    return line


def remove_header(line):
    line = line.split(": ", 1)[1]

    return line


def readFile():

    if not os.path.isfile(current_location+'\\pc_log.txt'):
        f = open(current_location+'\\pc_log.txt', 'w')
        f.close()

    f = open(current_location+'\\pc_log.txt', 'r+')
    lines = f.readlines()
    f.truncate(0)
    f.close()
    t = trie.Trie()

    if lines: # 헤더에 따른 처리
        for line in lines:
            if line.startswith("Created file"):
                t.insert(line_formatter(remove_header(line)))
            elif line.startswith("Modified file"):
                t.insert(line_formatter(remove_header(line)))
            elif line.startswith("Moved file"):
                string = remove_header(line.replace("from ", "")).split(" to ")
                t.delete(line_formatter(string[0]))
                t.insert(line_formatter(string[1]))
            elif line.startswith("Deleted file"):
                t.delete(line_formatter(remove_header(line)))

    paths = t.query() # 검색 대상 경로 리스트 리턴

    if paths: # 검색 실행을 위해 검색 대상 경로 리스트를 스트링 처리
        for i in range(len(paths)):
            paths[i] = paths[i].replace("\\\\", "", 1)
            paths[i] = paths[i].replace(":\\", ":\\\\", 1)
    api.er_api(paths)

    threading.Timer(600, readFile).start() # 개별 스레드로 재실행
