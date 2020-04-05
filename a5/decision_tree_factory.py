from node import DTreeNode
from decision_tree import DecisionTree
import numpy as np

class DecisionTreeFactory:
    """
    A decision tree making class

    Args:
        data (np.matrix): training data from which to build tree
        labels (np.matrix): labels for training data
    """

    def __init__(self, data, labels):
        self.data = data
        self.labels = labels

    def build_tree(self):
        """
        Builds a tree from data and labels
        """

        root = DTreeNode(range(self.data.shape[0]))

        self._build_tree_rec(root)

        return DecisionTree(root)

    def _build_tree_rec(self, node):
        """
        Recursively builds tree out from input node

        Args:
            node (DTreeNode): the node from which to continue building out our tree.
        """

        # If we have pure data at this node, we can stop
        if node.should_stop(self.data):
            node.leaf = True
            return node
        # Otherwise it's time to find where to split
        children = []

        # generate a split at each attribute (if possible)
        for attr in range(self.data.shape[1]):
            attr_pos_idxs = []
            attr_neg_idxs = []

            for idx in node.get_idxs():
                if self.data[idx, attr] == 1:
                    attr_pos_idxs.append(idx)
                else:
                    attr_neg_idxs.append(idx)

            try:
                children.append((node, [DTreeNode(attr_pos_idxs),DTreeNode(attr_neg_idxs)],attr))
            except:
                pass

        # hopefully we could split somewhere
        assert children != []

        # rank the possible splits by information gain
        scores = sorted(zip(map(lambda child: self._calc_information_gain(child[0], child[1]), children),
                            map(lambda x: x[1], children),
                            map(lambda x: x[2],children)),
                         key=lambda x: x[0])

        # get the DTreeNode for the best children
        best_child = scores[0][1][0]
        other_child = scores[0][1][1]

        # set class for each child
        u,c = np.unique(self.labels[best_child.get_idxs()], return_counts=True)
        best_child.set_class(u,c)
        u,c = np.unique(self.labels[other_child.get_idxs()], return_counts=True)
        other_child.set_class(u,c)

        node.attr = scores[0][2]

        # Build out tree!
        node.children[1] = self._build_tree_rec(best_child)
        node.children[0] = self._build_tree_rec(other_child)

        return node

    ################
    ##### TODO #####
    ################
    def _calc_information_gain(self, parent_node, children_nodes):
        """
        Calculates the information gain going from parent node to some child nodes.
        Information gain can be calculated by finding the difference between the entropy
        at the parent node, and sum of the entropy of each child node normalized by the
        proportion of datapoints in that child node.

        Args:
            parent_node (DTreeNode): The node from which we are generating the split
            children_nodes (List<DTreeNode>): The child nodes for this potential split

        Returns:
            (float): the information gain from splitting with given attributes

        References:
            [1]: https://en.wikipedia.org/wiki/Information_gain_in_decision_trees
        """

        pEntropy = parent_node.get_entropy(self.labels[parent_node.get_idxs()])

        parentSize = float(len(parent_node.get_idxs()))

        averageChildEntropy = 0.0

        for node in children_nodes:
            curEntropy = node.get_entropy(self.labels[node.get_idxs()])
            averageChildEntropy += curEntropy*float(len(node.get_idxs()))/parentSize

        return pEntropy - averageChildEntropy



