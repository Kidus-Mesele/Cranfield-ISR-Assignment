import re
import subprocess
import sys

# Run PageRank.py and capture output
result = subprocess.run([sys.executable, "PageRank.py"], 
                        capture_output=True, 
                        text=True)

output = result.stdout + result.stderr

# Extract Sink Nodes
sink_match = re.search(r"Sink Nodes:\s*(\d+)", output)
if sink_match:
    sink_nodes = sink_match.group(1)
    print(f"Sink Nodes: {sink_nodes}")
else:
    print("Sink Nodes: Not found")

# Extract Number of rounds
rounds_match = re.search(r"Number of rounds:\s*(\d+)", output)
if rounds_match:
    rounds = rounds_match.group(1)
    print(f"Number of rounds: {rounds}")

# Extract Time (format: hours:minutes:seconds)
time_match = re.search(r"(\d+):(\d+):(\d+)", output)
if time_match:
    hours = time_match.group(1)
    minutes = time_match.group(2)
    seconds = time_match.group(3)
    print(f"Runtime: {hours}h {minutes}m {seconds}s")
else:
    print("Runtime: Not found")

# Also save full output to a file for reference
with open("pagerank_output.txt", "w") as f:
    f.write(output)
print("\nFull output saved to pagerank_output.txt")