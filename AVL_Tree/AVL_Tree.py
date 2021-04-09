import sys
import random

class Node:
    def __init__(self, element, height):
        self.element = element
        self.height = height
        self.left = None
        self.right = None

class AVL_Tree:
    def __init__(self):
        self.node = None

    def height(self, t):
        if t == None:
            return -1
        else:
            return t.height
    
    def LLrotation(self, t):
        tmp = t.left
        t.left = tmp.right
        tmp.right = t

        t.height = max(self.height(t.left), self.height(t.right)) + 1
        tmp.height = max(self.height(tmp.left), self.height(tmp.right)) + 1
        
        return tmp

    def RRrotation(self, t):
        tmp = t.right
        t.right = tmp.left
        tmp.left = t

        t.height = max(self.height(t.left), self.height(t.right)) + 1
        tmp.height = max(self.height(tmp.left), self.height(tmp.right)) + 1
        
        return tmp

    def LRrotation(self, t):
        t.left = self.RRrotation(t.left)
        t = self.LLrotation(t)

        return t

    def RLrotation(self, t):
        t.right = self.LLrotation(t.right)
        t = self.RRrotation(t)

        return t

    def insert(self, element):
        self.node = self.insert_element(element, self.node)

    def insert_element(self, element, t):
        if t == None:
            t = Node(element, 0)
        else:
            if element < t.element:
                t.left = self.insert_element(element, t.left)
            elif element > t.element:
                t.right = self.insert_element(element, t.right)
            else:
                print("<Error> Constraint : Unique element")
                return

        t.height = max(self.height(t.left), self.height(t.right)) + 1
        t = self.balance(t)
        return t

    def balance(self, t):
        if t == None:
            return
        else:
            #left
            if self.height(t.left) - self.height(t.right) > 1: #balace factor
                #left - left
                if self.height(t.left.left) > self.height(t.left.right):
                    t = self.LLrotation(t)
                #left - right
                else:
                    t = self.LRrotation(t)
            #right
            if self.height(t.right) - self.height(t.left) > 1: #balace factor
                #right - right
                if self.height(t.right.right) > self.height(t.right.left):
                    t = self.RRrotation(t)
                #right - left
                else:
                    t = self.RLrotation(t)        
            return t

    def delete(self, element):
        self.node = self.delete_element(element, self.node)

    def delete_element(self, element, t):
        if t == None:
            return
        else:
            #Find node
            if element == t.element:
                #No child(left node)
                if t.left == None and t.right == None:
                    #print("Delete {}".format(t.element))
                    t = None
                    return t
                #One child
                elif t.left == None:
                    #print("Delete {}".format(t.element))
                    t = t.right
                    return t
                elif t.right == None:
                    #print("Delete {}".format(t.element))
                    t = t.left
                    return t
                #Two child
                else:
                    #print("Delete {}".format(t.element))
                    tmp = t
                    t = self.find_max(tmp.left) #Left max element -> root
                    t.left = self.delete_max(tmp.left) #Delete left max element
                    t.right = tmp.right

            elif element < t.element:
                t.left = self.delete_element(element, t.left)
            elif element > t.element:
                t.right = self.delete_element(element, t.right)

            t.height = max(self.height(t.left), self.height(t.right)) + 1
            t = self.balance(t)

            return t

    def find_max(self, t):
        if t.right == None:
            return t
        else:
            return self.find_max(t.right)

    def delete_max(self, t):
        if t.right == None:
            return t.left
        else:
            t.right = self.delete_max(t.right)
            t.height = max(self.height(t.left), self.height(t.right)) + 1
            t = self.balance(t)
            return t    

    def search(self, element):
        res = self.search_check(element, self.node)
        return res
    
    def search_check(self, element, t):
        if t == None:
            #print("Element {} is not in the AVL_Tree\n".format(element))
            return -1
        else:
            if element < t.element:
                return self.search_check(element, t.left)
            elif element > t.element:
                return self.search_check(element, t.right)
            else:
                #print("Element {} is in the AVL_Tree\n".format(element))
                return 1
               
    def display(self, t):
        if t == None:
            return
        print("(", end = '')
        if t.left:
            self.display(t.left)
        print("{} [{}]".format(t.element, t.height), end = '')
        if t.right:
            self.display(t.right)
        print(")", end = '')  

#Test 10 data with inorder graph
#Graph format : (element [height])
def test1():
    sys.setrecursionlimit(10**8)
    insert_fail = 0
    delete_fail = 0
    cnt = 0
    
    a = AVL_Tree()

    #Test data
    lst = [500, 200, 400, 700, 100, 900, 800, 50, 250, 450]
    print("Insert list : {}\n".format(lst))
    lst_delete = [400, 800, 900, 250, 450]
    print("Delete list : {}\n".format(lst_delete))
    lst_res = list(set(lst) - set(lst_delete))

    #Insert
    print("<Start insert...>\n")
    for i in lst:
        a.insert(i)
    print("Insert complete")
    #Insert testing
    for i in lst:
        if a.search(i) == -1:
            insert_fail += 1
    print("Insert fail : {}".format(insert_fail))
    #Graph
    print("\n<Graph>\n")
    a.display(a.node)
    print()
    #Delete
    print("\n<Start delete...>\n")
    for i in lst_delete:
        a.delete(i)
    print("Delete complete")
    #Delete testing
    for i in lst_delete:
        if a.search(i) == 1:
            delete_fail += 1
    print("Delete fail : {}".format(delete_fail))
    #Result data testing
    for i in lst_res:
        if a.search(i) == -1:
            cnt += 1
    #Graph
    print("\n<Graph>\n")
    a.display(a.node)
    print()
    print("\nRemaining element test result : {}\n".format(cnt))

#Test 100 data with inorder graph
#Graph format : (element [height])
def test2():
    sys.setrecursionlimit(10**8)
    insert_fail = 0
    delete_fail = 0
    cnt = 0
    
    a = AVL_Tree()

    #Test data
    lst = random.sample(range(0, 1001), 100)
    print("Insert list : {}\n".format(lst))
    lst_delete = random.sample(lst, 50)
    print("Delete list : {}\n".format(lst_delete))
    lst_res = list(set(lst) - set(lst_delete))

    #Insert
    print("<Start insert...>\n")
    for i in lst:
        a.insert(i)
    print("Insert complete")
    #Insert testing
    for i in lst:
        if a.search(i) == -1:
            insert_fail += 1
    print("Insert fail : {}".format(insert_fail))
    #Graph
    print("\n<Graph>\n")
    a.display(a.node)
    print()
    #Delete
    print("\n<Start delete...>\n")
    for i in lst_delete:
        a.delete(i)
    print("Delete complete")
    #Delete testing
    for i in lst_delete:
        if a.search(i) == 1:
            delete_fail += 1
    print("Delete fail : {}".format(delete_fail))
    #Result data testing
    for i in lst_res:
        if a.search(i) == -1:
            cnt += 1
    #Graph
    print("\n<Graph>\n")
    a.display(a.node)
    print()
    print("\nRemaining element test result : {}\n".format(cnt))
    
#Test 1000000 data
def test3():
    sys.setrecursionlimit(10**8)
    insert_fail = 0
    delete_fail = 0
    cnt = 0
    
    a = AVL_Tree()

    #Test data
    lst = random.sample(range(0, 10000001), 1000000)
    lst_delete = random.sample(lst, 500000)
    lst_res = list(set(lst) - set(lst_delete))

    #Insert
    print("<Start insert...>\n")
    for i in lst:
        a.insert(i)
    print("Insert complete")
    #Insert testing
    for i in lst:
        if a.search(i) == -1:
            insert_fail += 1
    print("Insert fail : {}".format(insert_fail))
    #Delete
    print("\n<Start delete...>\n")
    for i in lst_delete:
        a.delete(i)
    print("Delete complete")
    #Delete testing
    for i in lst_delete:
        if a.search(i) == 1:
            delete_fail += 1
    print("Delete fail : {}".format(delete_fail))
    #Result data testing
    for i in lst_res:
        if a.search(i) == -1:
            cnt += 1
    print("\nRemaining element test result : {}\n".format(cnt))
    
if __name__ == "__main__":
    #Test 10 data with list and graph
    test1()
    print("\n-----------------------------------------------\n")
    #Test 100 data with list and graph
    test2()
    print("\n-----------------------------------------------\n")
    #Test 1000000 data with out list and graph 
    test3()
  

