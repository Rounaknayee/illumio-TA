import sys
from IANA import IANA_LOOKUP

# The idea here is to load lookup table as this is going to be a finite count 
# (MAX: ports * protocols), helpful for future O(1) search for
# port-protocol combination while encountering flow logs
def load_lookup(filename):
    lookup_dict = {}
    try: 
        with open(filename, "r") as f:
            for line in f:
                cols = line.strip().split(",")
                dstport = int(cols[0])
                protocol = str(cols[1]).lower()
                tag = cols[2]
                if dstport not in lookup_dict:
                    lookup_dict[dstport] = {}
                lookup_dict[dstport][protocol] = tag
        return lookup_dict
    except Exception as e:
        print("Error accessing lookup file %s", str(e))
        sys.exit(1)

def solve(flow_file, lookup_file):
    tag_count = {}
    port_protocol_count = {}

    try: 
        lookup_dictionary = load_lookup(lookup_file)
        with open(flow_file, "r") as f:
            for line in f:
                cols = line.strip().split()

                # According to flowlogs v2, when 0-indexed, column 6: dst_port, col 7: protocol_number 
                dst_port =  int(cols[6])
                protocol_number =  int(cols[7])

                # checking because our IANA lookup has limited values, can be extended to full 256 IANA mapping
                protocol = IANA_LOOKUP.get(protocol_number,"missing")

                if protocol != "missing":
                    tag = lookup_dictionary.get(dst_port,{}).get(protocol, "Untagged")
                    tag_count[tag] = tag_count.get(tag,0) + 1
                    if dst_port in port_protocol_count:
                        port_protocol_count[dst_port][protocol] = port_protocol_count[dst_port].get(protocol,0)+1
                    else:
                        port_protocol_count[dst_port] = { protocol:1 }

        # saving tag counts output_tagCount.txt and combination counts to output_combinationCount.txt

        with open("output_tagCount.txt", "w") as ot:
            ot.write("Tag,Count\n")
            for tag, count in tag_count.items():
                ot.write(f"{tag},{count}\n")


        with open("output_combinationCount.txt", "w") as oc:
            oc.write("Port,Protocol,Count\n")
            for port, protocols in port_protocol_count.items():
                for protocol, count in sorted(protocols.items()):
                    oc.write(f"{port},{protocol},{count}\n")
    
    except Exception as e:
        print("Error running solve method: %s", str(e))
        sys.exit(1)

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Try: python3 main.py <flow_file_name> <lookup_file_name>")
        sys.exit(1)

    # Get file names from CLI
    flow_file_name = sys.argv[1]
    lookup_file_name = sys.argv[2]

    #solve
    solve(flow_file_name, lookup_file_name)
