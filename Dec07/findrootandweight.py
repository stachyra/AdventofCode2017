# Holds nodes in a tree-shaped directed acyclic graph
class dagtree:
    # Build the DAG, based upon the data in the adjacency dictionary
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
    # Find the incorrectly weighted child node, and return its correct weight
    def getcorrectweight(self):
        # If the children of this node in the dagtree are properly weight
        # balanced, then this dictionary will end up having a single key, and
        # the value will be a list of all n children of the current node.
        # OTOH if the children are not weight balanced, then the dictionary
        # will end up having two keys.  One key will correspond to the weight
        # of the (n-1) properly balanced children (and the value associated
        # with the key will be a list of length (n-1), consisting of all the
        # correctly balanced children), while the other key will give the
        # weight of the node with an incorrectly weighted descendent (and
        # its value will be a list of length 1, containing the node with
        # a badly weighted descendent).
        weightdist = {}
        for c in self.childnodes:
            if c.sumweight in weightdist:
                weightdist[c.sumweight].append(c)
            else:
                weightdist[c.sumweight] = [c]
        # If the weights of the children are all equal value, then it means
        # that we've reached the bottom of the recursion tree, and the parent
        # node on the next level above this is the one with the incorrect
        # weighting, so we return a special None value as an indicator
        if len(weightdist) == 1:
            return None
        else:
            for w in weightdist:
                # This weight doesn't match the others, and indicates the
                # node that has a descendent node with an incorrect weight 
                if len(weightdist[w]) == 1:
                    uniqueweight = w
                # The correct or expected weight for all child nodes at this
                # level of the tree
                if len(weightdist[w]) > 1:
                    commonweight = w
            # Call the method recursively, upon the child node which has
            # the unique (i.e., incorrect) weight
            retval = weightdist[uniqueweight][0].getcorrectweight()
            # Catch the indicator which tells us the level below the child
            # was correctly balanced, and that the child node itself was
            # therefore the incorrectly weighted node
            if retval is None:
                correction = uniqueweight - commonweight
                return weightdist[uniqueweight][0].ownweight - correction
            # Once we've found the correct weight, pass it up the call stack
            # until we get back to the top
            else:
                return retval


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
# Print solution to part a
print(root)

# Create a DAG tree graph from data in the adjacency list
dag = dagtree(adjdct, root)
# Print the solution to part b
print(dag.getcorrectweight())
