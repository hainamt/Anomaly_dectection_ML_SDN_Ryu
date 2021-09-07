#!/bin/bash
inotifywait -m -r -q -e create --format %w%f /home/natrie/Topology/OutputPCAP | while read FILE
do
  ./CICFlowMeter-4.0/bin/cfm $FILE /home/natrie/Topology/OutputCSV
  echo "$FILE has been converted to CSV by CICFlowmeter"  
done
