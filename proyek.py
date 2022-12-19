from copy import copy
class NodeFolder:
    def __init__(self, name):
        self.name= name
        self.child= DoubleLinkedList()
        self.next= None
        self.prev= None
    def rename(self, newName):
        self.name= newName
    def getDetail(self):
        print("Folder Name:", self.name)


class NodeDrive:
    def __init__(self, name):
        if (len(name) > 2 or (ord(name[0]) < 65 and ord(name[0]) > 90)):
            print('failed disk name invalid')
            self.status= False
            return
        self.name= name
        self.next= None
        self.prev= None
        self.status= True
    

class NodeZip:
    def __init__(self, name, listOfChild):
        self.name= name
        self.type= "zip"
        self.child= DoubleLinkedList()
        self.next= None
        self.prev= None
        # listOfChild isinya node
        for i in listOfChild:
            self.child.addWithSort(i)
    def rename(self, newName):
        self.name= newName
    def getDetail(self):
        print("Name:", self.name)
        print("Type:", self.type)
    

class NodeFile:
    def __init__(self,name):
        self.name= name
        indexType= searchTypeOfFile(self.name)
        self.type=self.name[indexType:]
        self.next= None
        self.prev= None
    def rename(self, newName):
        self.name=newName
        indexType= searchTypeOfFile(self.name)
        self.type= self.name[indexType:]
    def getDetail(self):
        print("File Name:", self.name)
        print("File Type:", self.type)


def searchTypeOfFile(fileName):
    indexType=0
    for i in fileName[::-1]:
        if i == ".":
            break
        indexType += 1
    return len(fileName)-indexType

class DoubleLinkedList:
    def __init__(self):
        self.head= None
        self.tail= None
        self.size=0

    def getNode(self, name):
        iter= self.head
        for i in range(self.size):
            if iter.name.lower() == name.lower():
                return iter
            iter= iter.next
        print("Tidak ditemukan")
        return 0
    def renameThenSort(self, node: NodeFolder or NodeFile or NodeZip, newName):
        iter= self.head
        for i in range(self.size):
            if iter.name== node.name:
                break
            iter= iter.next
        if iter== self.head:
            self.head= iter.next
            self.head.prev= None
            iter.next= None
            iter.prev= None
        elif iter== self.tail:
            self.tail= iter.prev
            self.tail.next= None
            iter.next= None
            iter.prev= None
        else:
            iter.prev.next= iter.next
            iter.next.prev= iter.prev
            iter.next= None
            iter.prev= None

        iter.rename(newName)
        self.size-=1
        self.addWithSort(iter)

    def addWithSort(self, node: NodeFolder or NodeFile or NodeZip):
        iter= self.head
        canAdd= True
        for i in range(self.size):
            if iter.name.lower()== node.name.lower():
                canAdd= False
                break
            iter= iter.next

        if canAdd:
            if self.size==0:
                self.head= node
                self.tail= node
            elif self.size==1:
                if self.head.name.lower() > node.name.lower():
                    node.next = self.head
                    self.head.prev = node
                    self.head = node
                else:
                    node.prev = self.head
                    self.head.next = node
                    self.tail = node
            else:
                iter= self.head
                loop=0
                while loop<self.size:
                    if iter.name.lower() > node.name.lower():
                        break
                    loop+=1
                    iter= iter.next
                if loop==0:
                    node.next= self.head
                    self.head.prev= node
                    self.head= node
                elif loop== self.size:
                    node.prev= self.tail
                    self.tail.next= node
                    self.tail= node
                else:
                    iter.prev.next= node
                    node.next= iter
                    node.prev= iter.prev
                    iter.prev = node
            self.size += 1
        else:
            print("Ada data yang sama")

    def deleteByName(self, name):
        iter = self.head
        if self.size == 0:
            print("kosong")
        else:
            for i in range(self.size):
                if iter.name.lower() == name.lower():
                    if self.head == self.tail:
                        self.head = self.tail = None
                    elif iter == self.head:
                        self.head = self.head.next
                        self.head.prev = None
                    elif iter == self.tail:
                        self.tail= self.tail.prev
                        self.tail.next = None
                    else:
                        iter.prev = temp
                        temp.next = iter.next
                    self.size-=1
                temp = iter
                iter = iter.next

    def printAsc(self):
        iter= self.head
        for i in range(self.size):
            print(iter.name)
            iter= iter.next
    def printDesc(self):
        iter= self.tail
        for i in range(self.size):
            print(iter.name)
            iter= iter.prev
    def sortByType(self):
        arrFolder= []
        arrFile= []
        iter= self.head
        for i in range(self.size):
            if type(iter) is NodeFolder:
                arrFolder.append(iter)
            else:
                index=0
                for i in range(len(arrFile)):
                    if iter.type < arrFile[i].type:
                        break
                    index+=1
                arrFile.insert(index,iter)
            iter= iter.next
        for i in arrFolder:
            print(i.name)
        for i in arrFile:
            print(i.name)
    
    def getNode(self, name):
        iter= self.head
        for i in range(self.size):
            if iter.name==name:
                return iter
            iter= iter.next

    def viewByType(self, types):
        print("VIEW", types)
        if types=="Folder" or types=="folder":
            iter= self.head
            for i in range(self.size):
                if type(iter) is NodeFolder:
                    print(iter.name)
                iter= iter.next
        else:
            iter= self.head
            for i in range(self.size):
                if type(iter) is NodeFile:
                    if iter.type == types:
                        print(iter.name)
                iter= iter.next

    def viewOnlyZip(self):
        iter= self.head
        for i in range(self.size):
            if type(iter) is NodeZip:
                print(iter.name)
            iter= iter.next
        print()

    def groupBy(self):
        #Folder first
        adaFolder= False
        iter= self.head
        for i in range(self.size):
            if type(iter) is NodeFolder:
                adaFolder= True
                break

        if adaFolder:
            print("======== FOLDER ========")
            iter= self.head
            for i in range(self.size):
                if type(iter) is NodeFolder:
                    print(iter.name)
                iter= iter.next
        #File
        visitedType=[]
        iter= self.head
        for i in range(self.size):
            if type(iter) is NodeFile or type(iter) is NodeZip:
                if iter.type not in visitedType:
                    visitedType.append(iter.type)
                    print("========", iter.type.upper() , "========")
                    iter2= self.head
                    for j in range(self.size):
                        if type(iter2) is NodeFile or type(iter2) is NodeZip:
                            if iter2.type == iter.type:
                                print(iter2.name)
                        iter2= iter2.next
            iter=iter.next




class Tree:
    def __init__(self,root = NodeFolder("My Computer")):
        self.root = root
    
    def findAll(self,node,name):
        path = self.getPath(node)
        self.findAllUtil(name,node,path)
    
    def findAllUtil(self,name,node : NodeFolder,path):
        queue = []
        temp = node.child.head
        while temp is not None:
            queue.append(temp)
            temp = temp.next
        while len(queue) > 0:
            akses = queue.pop(0)
            if type(akses) == NodeFile:
                if akses.name.__contains__(name):
                    for i in path :
                        print(i,end="\\")
                    print(akses.name)
                continue
            elif type(akses) == NodeFolder:
                if akses.name.__contains__(name):
                    for i in path :
                        print(i,end="\\")
                    print(akses.name)
                    path.append(akses.name)
                self.findAllUtil(name,akses,path)
        path.pop(len(path)-1)

    def getPath(self,node:NodeFolder or NodeFile or NodeZip):
        return self.getPathUtil(self.root,node,[])
    
    def getDetail(self, node: NodeFolder or NodeFile or NodeZip):
        node.getDetail()
        print("Path: ", end="")
        self.printPath(node)
        print()

    def printPath(self,node:NodeFolder or NodeFile or NodeZip):
        for i in self.getPath(node):
            print(i,end="\\")

    def getPathUtil(self,node,search,path):
        path.append(node.name)     
        queue = []
        temp = node.child.head
        while temp is not None:
            queue.append(temp)
            temp = temp.next
        while len(queue) > 0:
            akses = queue.pop(0)
            if type(akses) == NodeFile:
                if akses == search:
                    path.append(akses.name)
                    return path
                
            if type(akses) == NodeFolder:
                if akses == search:
                    path.append(akses.name)
                    return path
                else:
                    hasil = self.getPathUtil(akses,search,path)
                    if(type(hasil) == list):
                        return hasil
        path.pop(len(path)-1)
        return

    def move(self,nodeParent: NodeFolder,nodePindah: NodeFolder or NodeFile or NodeZip, nodeParentTujuan: NodeFolder):
        temp= nodePindah
        nodeParent.child.deleteByName(nodePindah.name)
        nodeParentTujuan.child.addWithSort(temp)
    
    def copypaste(self, nodeCopy: NodeFolder or NodeFile or NodeZip, nodeParentDest: NodeFolder):
        newNode= copy(nodeCopy)
        nodeParentDest.child.addWithSort(newNode)

    def deleteFolderOnly(self, nodeParentOfFolder: NodeFolder, nodeDeleted: NodeFolder):
        llDelete= nodeDeleted.child
        nodeParentOfFolder.child.deleteByName(nodeDeleted.name)
        iter= llDelete.head
        for i in range(llDelete.size):
            nodeParentOfFolder.child.addWithSort(iter)
            iter= iter.next
    def deleteFolderAll(self, nodeParent: NodeFolder, nodeDelete: NodeFolder):
        nodeParent.child.deleteByName(nodeDelete.name)
    
    def unzip(self, zipInput: NodeZip, NodeTujuan: NodeFolder):
        newFolderName= zipInput.name
        newFolder= NodeFolder(newFolderName)
        NodeTujuan.child.addWithSort(newFolder)
        iter= zipInput.child.head
        for i in range(zipInput.child.size):
            newFolder.child.addWithSort(copy(iter))
            iter= iter.next
    def getNodeByPath(self, path):
        nodeHasil= self.root
        for i in path[1:]:
            nodeHasil= nodeHasil.child.getNode(i)
        return nodeHasil
        # if indexNow== len(path)-1:
        #     return 
        # else:
        #     indexNow+=1
        #     nodeAwal= nodeAwal.child.getNode(path[indexNow])
        #     self.getNodeByPath(path, indexNow, nodeAwal)
# t = Tree()
# t.root.child.addWithSort(NodeFolder('ayam bakar'))
# t.root.child.addWithSort(NodeFile('ayam.txt'))
# t.root.child.addWithSort(NodeFolder('boba tea'))
# t.root.child.addWithSort(NodeFile('Boba milk tea.txt'))
# t.root.child.head.child.addWithSort(NodeFile('ayam.txt'))
# t.root.child.head.child.addWithSort(NodeFolder('Bangsat'))
# t.root.child.head.child.head.next.child.addWithSort(NodeFolder('Bangsat kau sid'))
# def print_structure(node:NodeFolder or NodeDrive,lvl = 1):
#     print('>'+node.name)
#     temp = node.child.head
#     if temp != None:
#         while temp != None:
#             for i in range(lvl):
#                 print('    ',end="")
#             if type(temp) == NodeFile:
#                 print('-'+temp.name)
#             else:
#                 print_structure(temp,lvl+1)
#             temp = temp.next

# print_structure(t.root)
# t.printPath(t.root.child.head.child.head)