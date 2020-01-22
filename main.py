## No Threading
import re
import time
from time import sleep
import csv
from operator import itemgetter, attrgetter
print('\n')
def printJobStatus(job, start_time):
    print('------\n[x] {0}\n\tTime consuming:{0}\n\tTime Finished: {1}'.format(job, round(time.time() - start_time,4), time.strftime("%c")))    
def run(queue):
    query = "^([A-z]\w{1,3}  \d \d\d:\d\d:\d\d) ([0-z]*\w) (\S*): (.*)"
    for line in queue:
        m = re.match(query, line)
        if bool(m):
            output.append(m.groups())
log = "log.log"
queue = []; 
output = []
start_time = time.time()
file = open(log, "r", encoding='utf8')
for line in file:
    queue.append(line)    
printJobStatus("Opening Log", start_time)
start_time = time.time()
run(queue)
printJobStatus("REGEX Operation", start_time)
##ProcessLogs Object
start_time = time.time()
processLogs = {}
for row in output:
    if not row[2] in processLogs:
        processLogs.update({row[2] : 1})
    else:
        processLogs[row[2]] += 1
sortedProcessLogs = sorted(processLogs.items(), key = itemgetter(1), reverse=True)
printJobStatus("ProcessLogs Complete", start_time)
##Hostnames Object
start_time = time.time()
hostnames = {}
for row in output:
    if not row[1] in hostnames:
        hostnames.update({row[1] : 1})
    else:
        hostnames[row[1]] += 1
sortedhostnames = sorted(hostnames.items(), key = itemgetter(1), reverse=True)
printJobStatus("Hostnames Complete", start_time)

##Excel Spreadsheet
start_time = time.time()
with open('_Log-Output.csv', 'w', encoding='utf8') as csvfile:
  fieldnames = ['timestamp', 'hostname', 'processname', 'log']
  writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator = '\n')
  writer.writeheader()
  for row in output:
    writer.writerow({'timestamp': row[0], 'hostname': row[1], 'processname': row[2], 'log': row[3]})
printJobStatus("Finished Excel Output", start_time)

##Excel Spreadsheet Hostnames
start_time = time.time()
with open('_HostnameCount-Output.csv', 'w', encoding='utf8') as csvfile:
  fieldnames = ['Hostname', 'COUNT']
  writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator = '\n')
  writer.writeheader()
  for row in sortedhostnames:
    writer.writerow({'Hostname': row[0], 'COUNT': row[1]})
printJobStatus("Finished Excel Output", start_time)

##Excel Spreadsheet Processes
start_time = time.time()
with open('_ProcessCount-Output.csv', 'w', encoding='utf8') as csvfile:
  fieldnames = ['Process', 'COUNT']
  writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator = '\n')
  writer.writeheader()
  for row in sortedProcessLogs:
    writer.writerow({'Process': row[0], 'COUNT': row[1]})
printJobStatus("Finished Excel Output", start_time)
print('------')
