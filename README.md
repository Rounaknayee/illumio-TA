## ROUNAK NAYEE - ILLUMINO TAKE HOME 16 JANUARY, 2025

# Approach:

1. The lookup table is loaded into a 2D dictionary, allowing constant-time O(1) lookups for each (port, protocol) pair while further parsing the flow logs.
2. Each line in the flow log file is parsed to extract the destination port(column 7) and protocol number(column 8) according to flow log v2.
3. The protocol number is converted to its string equivalent using the IANA_LOOKUP dictionary constructed in IANA.py
4. The cuorresponding tag is retrieved from lookup dictioanry and either added to tag_count counter or labeled as "Untagged"
5. Similarly a seperate 2D - Dictionary stores our count of occurences for each dst_port-protocol combination.
6. At the end the ouputs from both dictionaries are written to seperate output files - output_tagCount.txt, output_combinationCount.txt
7. Desired ouputs stored in validate_tagCount.txt and validate_combinationCount.txt are tested by invoking test.py

# Assumptions:
1. Each pair for dst_port and protocol maps to exactly one tagin lookup table.
2. The flow logs do not contain NoData or Skipped records, duplicate rows and each line has correct columns following v2 version.
3. No header lines for both input files (i.e. flow_logs, lookup_table).
4. We use finite IANA_LOOKUP mapping for ports for now and assign undefined if not found, MAX can be extended to all 256 entries...
5. All port and protocol fields are valid integers, no lines are malformed or partial.
6. The output is divided into two individual files with respective headers(output_tagCount.txt and output_combinationCount.txt).
7. Considering the 10 MB limit for flow_log file(approx. 100,000 entries considering each line to be 100 bytes), we can fit the calculations in memory of a standard computer and write all data at once to output file.
8. The Input doesnot contain blank lines and Ouput doesn't require to be in sorted manner.
9. The program has been checked against python 3.12 on macOS Sonoma(14.5) with the default built-in modules.


# Time Complexity

O (len(flow_logs) + len(lookup_table))

# Space  

O(len(lookup_dictionary) + len(flow_logs))

- WORST CASE for lookup_dictionary: 65536 * 256 (Total ports(0–65535) * IANA Protocols(0-255))

# Usage:

Run main program:

```
python3 main.py flow_logs.txt lookup_table.txt
```
Run Test:
```
python3 test.py
```