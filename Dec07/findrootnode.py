filename = 'input.txt'

# This set will include all nodes in the DAG tree
allnodes = set()
# This set includes only nodes which have a parent node above them in the
# DAG tree (abd the difference between the two gives us root nodes)
nonroot = set()

with open(filename) as f:
    # Loop through each
    for line in f:
        # Split into individual words, using white space as the default 
        # separator
        items = line.split()
        # The leftmost word is always a node name; add it to the first set
        allnodes.add(items[0])
        n = len(items)
        # Items 2 and 3, if they exist, give a weight and an arrow.  Items
        # 4 and above give node names which are guaranteed to have a parent
        if n >= 4:
            for ii in range(3,n):
                # Add each node to the right of an arrow to the set of nodes
                # which have parents (removing a trailing comma if necessary)
                nonroot.add(items[ii].rstrip(','))

rootnodes = allnodes - nonroot
print(rootnodes)

