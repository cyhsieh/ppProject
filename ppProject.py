import threading, queue, time, sys
import sqlite3
from snownlp import SnowNLP

total_score = 0

class Worker(threading.Thread):
    def __init__(self, thid, queue):
        threading.Thread.__init__(self)
        self.thid = thid
        self.queue = queue
        self.datalen = queue.qsize()
        self.TmpFile = ""
        self.url= ""
        self.context = ""
        self.index = ""
        self.score = 0
        # self.score = total_score

    def run(self):
        # self.score += 1
        global total_score 
        while self.queue.qsize() > 0:
            self.score += 1
            # 取得新的資料
            data = self.queue.get()
            # self.TmpFile = data['TmpFile']
            self.url= data['url']
            print("thread {} processing url:{}".format(self.thid, self.url))
            context = data['post_content']
            self.score += SnowNLP(context).sentiments
            # self.index = data['index']
            # print("{}\n worker {} job {} {}/{} processing".format(self.url, self.thid))
            # totalscore = ck_senti(self.context, self.TmpFile)
            # if totalscore == 999:
            #     print("worker {} job {} existed, continue...".format(self.num, self.TmpFile))
            #     continue
            continue
        total_score += self.score



if len(sys.argv) != 2:
    print("usage: python ppProject.py <thread_num>")
    sys.exit()
if not sys.argv[1].isdigit():
    print("usage: python ppProject.py <thread_num>")
    sys.exit()

thread_num = int(sys.argv[1])

print(thread_num)
th_list = []
conn = sqlite3.connect('./pttfood_pp.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()
cur.execute('select * from pttfood;')
# print(cur.description)
result = cur.fetchall()
q = queue.Queue()
for r in result:
    q.put(r)

for i in range(thread_num):
    print("init thread {}".format(i))
    worker = Worker(i, q)
    th_list.append(worker)

starttime = time.time()
for i in range(thread_num):
    th_list[i].start()

for i in range(thread_num):
    th_list[i].join()
endtime = time.time()

print("Done. score is {}".format(total_score))
print("total threads: {}, elapsed time: {}s".format(thread_num, (endtime-starttime)))
exit()