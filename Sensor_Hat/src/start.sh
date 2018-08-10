#!/bin/bash

# Start sshd if we don't use the init system
if [ "$INITSYSTEM" != "on" ]; then
  /usr/sbin/sshd -p 22 &
fi

python "/usr/src/app/src/thread_sense.py"

echo "This is where your application would start..."
while : ; do
  echo "waiting"
  sleep 60
done
