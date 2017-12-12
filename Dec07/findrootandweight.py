class dagtree:
    def __init__(self, adjd, key):
        self.nodename = key
        # Weight of each node by itself is given by first element of list
        self.ownweight = adjd[key][0]
        self.childnodes = []
        self.sumweight = adjd[key][0]
        for ii in range(1, len(adjd[key])):
            # Create child nodes recursively. The name of each child node is
            # given by the 1st through nth nodes of the list corresponding to
            # each dictionary key
            self.childnodes.append(dagtree(adjd, adjd[key][ii]))
            self.sumweight += self.childnodes[-1].sumweight
    def getcorrectweight(self):
    	# Desired return value
        correctweight = None
        # List of child nodes (will be reassigned as we descend through each
        # tree level)
        children = self.childnodes
        # Weight of previous parent node, one level prior.  When we finally
        # get to the bottom (which equates to finding a perfectly balanced
        # list of nodes) this is the number which will require correcting
        parentweight = self.ownweight
        done = False
        while not done:
        	# This is effectively a histogram, with the sumweights of
        	# the children assigned as keys, and the number of children
        	# corresponding to each weight assigned as values.  Most of the
        	# time, for n children, there will be 2 keys, and one of the
        	# keys will have a value of 1, while the other key has a value
        	# of (n-1).  (On the final descent iteration, there will be only
        	# a single key, with a value of n.)
            weightdist = {}
            for c in children:
                if c.sumweight in weightdist:
                    weightdist[c.sumweight] += 1
                else:
                    weightdist[c.sumweight] = 1
            # We're done--calculate the final correct weight by taking the
            # ownweight of the parent node one level above the current
            # position within the tree, and correcting for the difference
            # in sumweights observed at that level.
            if len(weightdist) == 1:
                done = True
                correctweight = parentweight - (uniqueweight - commonweight)
            # Not done yet, so reassign parents, children, and correction
            # factors, then return to the top of the loop and descend one
            # more level in the tree.
            else:
                for k in weightdist:
                	if weightdist[k] == 1:
                		uniqueweight = k
                	if weightdist[k] > 1:
                		commonweight = k
                for c in children:
                    if c.sumweight == uniqueweight:
                        newparent = c
                        break
                children = newparent.childnodes
                parentweight = newparent.ownweight

        return correctweight

filename = 'input.txt'

# This set will include all nodes in the DAG tree
allnodes = set()
# This set includes only nodes which have a parent node above them in the
# DAG tree (abd the difference between the two gives us root nodes)
nonroot = set()
# This dictionary will hold lists of weights (0th element) and child nodes
# (1st through nth elements)
adjdct = {}

with open(filename) as f:
    # Loop through each line of input
    for line in f:
        # Split into individual words, using white space as the default 
        # separator
        items = line.split()
        # The leftmost word is always a node name; add it to the first set
        allnodes.add(items[0])
        # Initialize adjacency dictionary to hold node weight as 0th element
        # in a new list
        adjdct[items[0]] = [int(items[1].lstrip('(').rstrip(')'))]
        n = len(items)
        # Items 2 and 3, if they exist, give a weight and an arrow.  Items
        # 4 and above give node names which are guaranteed to have a parent
        if n >= 4:
            for ii in range(3,n):
                # Add each node to the right of an arrow to the set of nodes
                # which have parents (removing a trailing comma if necessary)
                nonroot.add(items[ii].rstrip(','))
                adjdct[items[0]].append(items[ii].rstrip(','))

rootnodes = allnodes - nonroot
root = rootnodes.pop()
print(root)

dag = dagtree(adjdct, root)
print(dag.getcorrectweight())
