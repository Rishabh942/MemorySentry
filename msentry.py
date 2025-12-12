import psutil
import time
import subprocess
from collections import deque

CHECK_INTERVAL = 5       
HISTORY_LEN = 24         
LEAK_CONFIRM_MB = 100    

HELPER_KEYWORDS = ["Helper", "Renderer", "GPU", "Content", "Web Content"]
HELPER_LIMIT_MB = 500    
STRIKE_LIMIT = 3         

analyzers = {}

class ProcessAnalyzer:
    def __init__(self, name, start_mem):
        self.name = name
        self.history = deque(maxlen=HISTORY_LEN)
        self.history.append(start_mem)
        self.strikes = 0   
        self.alerted = False

    def add_sample(self, mem_mb):
        self.history.append(mem_mb)

    def is_helper_process(self):
        return any(k in self.name for k in HELPER_KEYWORDS)

    def analyze(self):
        if len(self.history) < 12: return False, 0

        mid = len(self.history) // 2
        floor_old = min(list(self.history)[:mid])
        floor_new = min(list(self.history)[mid:])
        drift = floor_new - floor_old

        limit = HELPER_LIMIT_MB if self.is_helper_process() else LEAK_CONFIRM_MB

        if drift > limit:
            recent = list(self.history)[mid:]
            slope = (recent[-1] - recent[0]) / len(recent)
            
            if slope > 1.0:
                if self.alerted:
                    print(f"  [🛑 Ongoing] {self.name} (+{drift:.0f} MB)")
                    return False, 0
                
                self.strikes += 1
                display_strikes = min(self.strikes, STRIKE_LIMIT)
                print(f"  [⚠️ Suspicious] {self.name} ({display_strikes}/{STRIKE_LIMIT}) - Drift +{drift:.0f}MB")
                
                if self.strikes >= STRIKE_LIMIT:
                    self.alerted = True
                    return True, drift
            else:
                self.strikes = 0
        else:
            self.strikes = 0
            if drift < 10: self.alerted = False
        
        return False, 0

def send_popup_alert(title, message):

    script = f'display alert "🛑 {title}" message "{message}" as critical buttons {{"OK"}}'
    subprocess.Popen(["osascript", "-e", script])

def scan_processes():
    global analyzers
    current_pids = set(psutil.pids())
    
    for pid in set(analyzers.keys()) - current_pids:
        del analyzers[pid]

    for pid in current_pids:
        if pid == 0: continue
        try:
            proc = psutil.Process(pid)
            mem_mb = proc.memory_info().rss / 1024 / 1024
            if mem_mb < 50: continue 

            if pid not in analyzers:
                try: name = proc.name()
                except: name = "Unknown"
                analyzers[pid] = ProcessAnalyzer(name, mem_mb)
            else:
                analyzer = analyzers[pid]
                analyzer.add_sample(mem_mb)
                
                is_leaking, drift = analyzer.analyze()
                
                if is_leaking:
                    print(f"🛑 LEAK CONFIRMED: {analyzer.name}")
                    send_popup_alert(
                        "MEMORY LEAK DETECTED", 
                        f"{analyzer.name} is leaking.\nBaseline grew by +{drift:.0f} MB."
                    )
                    
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

def main():
    print(r"""
▗▖  ▗▖▗▄▄▄▖▗▖  ▗▖ ▗▄▖ ▗▄▄▖▗▖  ▗▖     ▗▄▄▖▗▄▄▄▖▗▖  ▗▖▗▄▄▄▖▗▄▄▖▗▖  ▗▖
▐▛▚▞▜▌▐▌   ▐▛▚▞▜▌▐▌ ▐▌▐▌ ▐▌▝▚▞▘     ▐▌   ▐▌   ▐▛▚▖▐▌  █  ▐▌ ▐▌▝▚▞▘ 
▐▌  ▐▌▐▛▀▀▘▐▌  ▐▌▐▌ ▐▌▐▛▀▚▖ ▐▌       ▝▀▚▖▐▛▀▀▘▐▌ ▝▜▌  █  ▐▛▀▚▖ ▐▌  
▐▌  ▐▌▐▙▄▄▖▐▌  ▐▌▝▚▄▞▘▐▌ ▐▌ ▐▌      ▗▄▄▞▘▐▙▄▄▖▐▌  ▐▌  █  ▐▌ ▐▌ ▐▌  
    """)
    print("3 Strike mode on.")
    print("Running...")
    
    try:
        while True:
            scan_processes()
            time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        print("Stopping.")

if __name__ == "__main__":
    main()