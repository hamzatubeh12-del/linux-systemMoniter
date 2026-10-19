import csv
import os 
import time
log_file= "log.csv"
interval=2

# information on "proc" https://docs.kernel.org/filesystems/proc.html
def read_uptime():
    with open("/proc/uptime") as f:# /proc this is system info from kernel
        return float(f.read().split()[0])//3600 # we take first number becuase it is time since pc boot 

def read_memory():
    info={}
    with open("/proc/meminfo") as f:
        for line in f:
            key,value = line.split(":")
            info[key]= int(value.split()[0])
        total= info["MemTotal"] 
        using=total - info["MemAvailable"] 
        return using // 1024, total //1024 

def cpu_time():
    with open("/proc/stat") as f:
        part=f.readline().split()
    value = [int(i) for i in part[1:]]
    idle=value[3]+value[4]
    total = sum(value[:8])
    return idle, total

def cpu_percent(prev , cur):
    idle= cur[0]-prev[0]
    total = cur[1]-prev[1]
    if total ==0 :
        return 0
    return round(100*(1-idle/total),1)

def main():
    file= not os.path.exists(log_file)
    cpu_collact=[]
    with open(log_file,"a") as f:
        writer=csv.writer(f)
        if file:
            writer.writerow([
            "time", "cpu_percent", "mem_used",
            "mem_total", "uptime"
            ])
        prev = cpu_time()
        print("press ctrl+c to stopf ")
        try:
            while True:
                time.sleep(interval)
                cur=cpu_time()
                cpu= cpu_percent(prev,cur)
                cpu_collact.append(cpu)

                prev=cur
                used,total = read_memory()
                row = [time.strftime("%Y-%m-%d %H:%M:%S"),f"{cpu:1f} %",
                       used, total, round(read_uptime())]                     
                writer.writerow(row)
                f.flush()  # force write to disk
                print(row)
        except KeyboardInterrupt:
            print("Stop")
            if cpu_collact:
                average = sum(cpu_collact)/len(cpu_collact)
                maximum=max(cpu_collact)
            
                print(f"average = {average:1f}%")
                print(f"maximum = {maximum:1f}%")
main()
