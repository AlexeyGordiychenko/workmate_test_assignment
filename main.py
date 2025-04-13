from collections import defaultdict
from sys import argv

with open(argv[1], "r") as f:
    counts = defaultdict(lambda: defaultdict(int))
    for line in f:
        if "django.request" in line:
            parts = line.split(" ")
            level = parts[2]
            endpoint = next((x for x in parts if x.startswith("/")), None)
            counts[endpoint][level] += 1

for endpoint in sorted(counts.keys()):
    print(endpoint)
    for level in counts[endpoint]:
        print(f"  {level}: {counts[endpoint][level]}")
