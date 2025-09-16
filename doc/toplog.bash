# This script created a log of the memory consumption of nodered.

while true; date; do top -b -n1 -em -p$(pgrep -d, node-red); sleep 60; done >> memory.txt
# After execution, for cleaning the file:
#  - grep <pid> memory_ansy.txt > memory_<pid>.txt
