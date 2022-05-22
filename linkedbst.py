"""
File: linkedbst.py
Author: Ken Lambert
"""

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from math import log
import random
import time
import sys 
sys.setrecursionlimit(10**6)

class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        self.nodes =0
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            strin = ""
            if node != None:
                strin += recurse(node.right, level + 1)
                strin += "| " * level
                strin += str(node.data) + "\n"
                strin += recurse(node.left, level + 1)
            return strin

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        
        def postorder1(node, list1):
            if node.left is not None:
                postorder1(node.left, list1)
            list1.append(node.data)
            if node.right is not None:
                postorder1(node.right, list1)
    
        list1 = list()
        postorder1(self._root, list1)
        return list1

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0


    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left == None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_totop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentNode = top.left
            while not currentNode.right == None:
                parent = currentNode
                currentNode = currentNode.right
            top.data = currentNode.data
            if parent == top:
                top.left = currentNode.left
            else:
                parent.right = currentNode.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        itemRemoved = None
        preRoot = BSTNode(None)
        preRoot.left = self._root
        parent = preRoot
        direction = 'L'
        currentNode = self._root
        while not currentNode == None:
            if currentNode.data == item:
                itemRemoved = currentNode.data
                break
            parent = currentNode
            if currentNode.data > item:
                direction = 'L'
                currentNode = currentNode.left
            else:
                direction = 'R'
                currentNode = currentNode.right

        # Return None if the item is absent
        if itemRemoved == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentNode.left == None \
                and not currentNode.right == None:
            lift_totop(currentNode)
        else:

            # Case 2: The node has no left child
            if currentNode.left == None:
                newChild = currentNode.right

                # Case 3: The node has no right child
            else:
                newChild = currentNode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newChild
            else:
                parent.right = newChild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preRoot.left
        return itemRemoved

    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                oldData = probe.data
                probe.data = newItem
                return oldData
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        '''
        def height1(top):
            '''
            Helper function
            '''
            if top is None:
                return 0
            return max(height1(top.left),\
                 height1(top.right)) +1
        return height1(self._root) - 1

    def is_balanced(self):
        """return bool balanced"""
        balance = (2*log(self._size + 1) - 1)
        return self.height()<balance

    def range_find(self, low, high):
        """return list of items between low and high"""
        nodes = self.postorder()
        down, top = 0, len(nodes)
        while nodes[down] < low:
            down+=1
        while nodes[top-1] > high:
            top -=1
        if down<=top:
            return nodes[down:top]
        return

    def add_mid(self, list1):
        """recursive function for rebalancing"""
        if len(list1) == 0:
            return
        index = len(list1)
        self.add(list1[index//2])
        list1.pop(index//2)
        self.add_mid(list1[:(index//2)]) #left branch
        self.add_mid(list1[(index//2):]) #right branch

    def rebalance(self):
        """rebalances the tree"""
        nodes = self.postorder()
        self.clear()
        self.add_mid(nodes)

    def successor(self, item):
        """return None or the smallest among lager than item"""
        nodes, index = self.postorder(), 0
        try:
            while nodes[index] < item:
                index += 1
        except:
            return

        if nodes[index] == item:
            if index+1 < len(nodes):
                return nodes[index+1]
            return
        else:
            return nodes[index]

    def predecessor(self, item):
        """return None or the largest among smaller than item
        """
        nodes = self.postorder()
        index = len(nodes) - 1
        try:
            while nodes[index] > item:
                index -= 1
        except:
            return

        if nodes[index] == item:
            if index>0:
                return nodes[index-1]
            return
        else:
            return nodes[index]

    def find_words(self, path):
        list1 = []
        with open(path, "r", encoding='utf-8') as file:
            for line in file:
                line = line.replace("\n", "")
                list1.append(line)
        num_list = random.sample(range(0, len(list1)), 10000)
        list_of_words = []
        for i in num_list:
            list_of_words.append(list1[i])
        return list_of_words, list1


    def demo_bst(self,path):
        """returns efficiency"""
        words, big_list = self.find_words(path)
        alp_words= sorted(words)
        print("go")

        # start_time = time.time()
        # for word in alp_words:
        #     big_list.index(word)
        # #час пошуку у впорядкованому за абеткою словнику - 13c
        # first = time.time() - start_time

        
        tree1 = LinkedBST()
        for word in big_list:
            tree1.add(word)
        print("tree built")

        # tree2 = LinkedBST()
        # for word in words:
        #     tree2.add(word)
        
        print("going...")
        start_time = time.time()
        for word in words:
            tree1.find(word)
        # Бінарне дерево пошуку будується на основі словника, який впорядкований за абеткою.
        print("finishing...")
        second = time.time() - start_time
        print(second)

        # start_time = time.time()
        # for word in words:
        #     tree2.find(word)
        # # Бінарне дерево пошуку будується на основі словника який не впорядкований за абеткою
        # third = time.time() - start_time

        
        # start_time = time.time()
        # tree2.rebalance()
        # for word in words:
        #     tree2.find(word)
        # #бінарнe деревo пошуку після його балансування.
        # forth = time.time() - start_time
        
        # print(first, second, third, forth)
        # print(first)
        
        # print(third)
        # print(forth)
link = LinkedBST()
print(link.demo_bst("words.txt"))
