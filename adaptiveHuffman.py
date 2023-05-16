import bisect
import queue
from tqdm import tqdm
import os

class Node:
    def __init__(self, symbol=None, weight=0):
        self.symbol = symbol
        self.weight = weight
        self.parent = None
        self.left_child = None
        self.right_child = None

    def is_leaf(self):
        return self.left_child is None and self.right_child is None
    
def bisect(li,start,end,target):
    if start==end:
        return start
    mid=(start+end)//2
    if li[mid].weight>target:
        return bisect(li,start,mid,target)
    else:
        return bisect(li,mid+1,end,target)

class AdaptiveHuffman:
    def __init__(self):
        self.symbol_length = 8
        self.tree = Node("NYT",0)
        self.nodes = [self.tree]
        self.table = {}
        self.table["NYT"] = self.tree
    def _swap_nodes(self, node1, node2):# only non-root nodes will be swapped
        originNode1_Left=node1.parent.left_child
        originNode2_Left=node2.parent.left_child
        if originNode1_Left == node1:
            node1.parent.left_child = node2
        else:
            node1.parent.right_child = node2
        if originNode2_Left == node2:
            node2.parent.left_child = node1
        else:
            node2.parent.right_child = node1

        node1.parent,node2.parent = node2.parent,node1.parent
    def _update_weights(self, node,order):
        if node.parent is None:
            node.weight+=1
            return
        index=bisect(order,0,len(order),node.weight)-1
        while order[index].weight == node.weight:
            if order[index]==node.parent:
                index-=1
            elif order[index]==node:#don't need to swap
                node.weight+=1
                self._update_weights(node.parent,order[index+1:])
                return
            else:
                node.weight+=1
                self._swap_nodes(node,order[index])
                self._update_weights(node.parent,order[index+1:])
                return
    
    def _find_order(self, node):
        order=[]
        q=queue.Queue()
        q.put(self.tree)
        while not q.empty():
            now=q.get()
            order.append(now)
            if(now==node):
                return order[::-1]
            if now.is_leaf():
                continue
            q.put(now.right_child)
            q.put(now.left_child)
            
    
    def _update_tree(self, symbol):
        if symbol in self.table:
            node = self.table[symbol]
            self._update_weights(node,self._find_order(node))
        else:
            original_nyt = self.table["NYT"]
            new_node = Node(symbol,1)
            new_nyt = Node("NYT",0)
            new_nyt.parent = original_nyt
            new_node.parent = original_nyt
            original_nyt.left_child = new_nyt
            original_nyt.right_child = new_node
            original_nyt.symbol = None
            self.table["NYT"] = new_nyt
            self.table[symbol] = new_node
            self.nodes.append(new_node)
            self.nodes.append(new_nyt)
            self._update_weights(original_nyt,self._find_order(original_nyt))
    
    def _get_code(self, symbol):
        code = ""
        node=None
        if symbol in self.table:
            node = self.table[symbol]
        else:
            node = self.table["NYT"]
        while node.parent is not None:
                if node.parent.left_child == node:
                    code += "0"
                else:
                    code += "1"
                node = node.parent
        code=code[::-1]
        if symbol in self.table:
            return code
        else:
            return code+symbol
    def _toBinary(self,input,output):
        with open(input,"rb") as fin:
            with open(output,"w") as fout:
                byte=fin.read(1)
                while byte:
                    bits = "{0:b}".format(ord(byte)).zfill(8)
                    fout.write(bits)
                    byte=fin.read(1)
            
    def compress(self, input, output):
        buffer=""
        size = os.path.getsize(input)
        progress = tqdm(total=size)
        with open(input,"rb") as fin:
            with open(output,"wb") as fout:
                byte=fin.read(1)
                while byte:
                    progress.update(1)
                    bits = "{0:b}".format(ord(byte)).zfill(8)
                    buffer+= self._get_code(bits)
                    self._update_tree(bits)
                    byte=fin.read(1)

                    while len(buffer)>=8:
                        fout.write(bytes([int(buffer[:8],2)]))
                        buffer=buffer[8:]
                if len(buffer)>0:
                    buffer+=self._get_code("NYT")
                    buffer+="00000000" #padding
                 
                    fout.write(bytes([int(buffer[:8],2)]))
        progress.close()
        self._toBinary(output,"CompressionBinary.txt")
        print("Encode Done.")

    def expand(self, input,output):
        buffer=""
        times=int(len(input)/8)
        with open(output,"wb") as fout:
                now=self.tree
                for _ in tqdm(range(times)):
                    byte=input[:8]
                    input=input[8:]
                    buffer+=byte
                    while len(buffer)>0:
                        if now.is_leaf():
                            if now.symbol=="NYT":
                                byte=input[:8]
                                input=input[8:]
                                if len(byte)!=0:            
                                    buffer+=byte

                                if len(buffer)>=self.symbol_length:
                                    symbol=buffer[:self.symbol_length]
                                    buffer=buffer[self.symbol_length:]
                                    self._update_tree(symbol)
                                    fout.write(bytes([int(symbol,2)]))
                                    now=self.tree
                            else:
                                symbol=now.symbol
                                self._update_tree(symbol)
                                fout.write(bytes([int(symbol,2)]))
                            now=self.tree
                        else:
                            if buffer[0]=="0":
                                now=now.left_child
                            else:
                                now=now.right_child
                            buffer=buffer[1:]
        print("Decode Done.")
   
if __name__ == '__main__':
    Encoder=AdaptiveHuffman()
    Encoder.compress("fileplain.txt","code.txt")


    Decoder=AdaptiveHuffman()
    Decoder.expand("code.txt","recover.txt")



