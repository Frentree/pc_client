import threading
import os.path
import lib.api.er_api as api
import lib.fileIO.trie as trie


def line_formatter(line):
    line = line.replace("\n", "")
    line = line.replace("\\\\", "\\")
    line = list(line.split("\\"))
    return line


def remove_header(line):
    line = line.split(": ", 1)[1]

    return line


def readFile():

    if not os.path.isfile("./pc_log.txt"):
        f = open("./pc_log.txt", 'w')
        f.close()

    f = open("./pc_log.txt", 'r+')
    lines = f.readlines()
    f.truncate(0)
    f.close()
    t = trie.Trie()

    # remove is impossible since observer has locked log file
    # so the f.truncate(0) method is applicable
    # os.remove("D:\DEV\drive_watcher\erpy\prj\pc_log.txt")

    if lines:
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

    # f = open("D:\DEV\drive_watcher\erpy\prj\query_result.txt", 'a+')
    # print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    # result = str(t.query()).split(", ")
    # for path in result:
    #     f.write(path)
    #     f.write("\n")
    # print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")


    # print("test")
    # f = open("D:\DEV\drive_watcher\erpy\prj\pc_log_test.txt", 'a+')
    #
    # for i in range(1, 11):
    #     data = "%d line\n" % i
    #     f.write(data)
    # f.close()

    paths = t.query()

    if paths:
        for i in range(len(paths)):
            paths[i] = paths[i].replace("\\\\", "", 1)
            paths[i] = paths[i].replace(":\\", ":\\\\", 1)
    api.er_api(paths)

    threading.Timer(600, readFile).start()




