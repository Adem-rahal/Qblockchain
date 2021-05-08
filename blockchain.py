#! / usr / bin / env python3
# codage: utf-8
# Fabriqué par Sandro CAZZANIGA - 20191222

from datetime import datetime
from hashlib import sha256
import qiskit

def calculateHash(block):

    bloc = str(block.index) + str(block.previousHash) + str(block.timestamp) + str(block.data) + str(block.nonce)
    return (sha256(bloc.encode('utf-8')).hexdigest())


def repeat(string, length):
    return (string * (int(length / len(string)) + 1))[:length]


class Block(object):
    def __init__(self, index, previousHash, timestamp, data):
        self.index = index
        self.previousHash = previousHash
        self.timestamp = timestamp
        self.data = data
        self.nonce = 0
        self.hash = calculateHash(self)

    def mineBlock(self, difficulty):
        zeros = repeat("0", difficulty)
        self.nonce = 0
        while self.hash[0:difficulty] != zeros:
            self.nonce += 1
            self.hash = calculateHash(self)


class Blockchain(object):
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.blocks = []

        genesisBlock = Block(0, None, datetime.now(), "Genesis block")
        genesisBlock.mineBlock(self.difficulty)
        self.blocks.append(genesisBlock)

    def newBlock(self, data):
        latestBlock = self.blocks[-1]
        return (Block(latestBlock.index + 1, latestBlock.hash, datetime.now(), data))

    def addBlock(self, block):
        block.mineBlock(self.difficulty)
        self.blocks.append(block)

    def isFirstBlockValid(self):
        firstBlock = self.blocks[0]

        if firstBlock.index != 0:
            return False

        if firstBlock.previousHash is not None:
            return False

        if (firstBlock.hash is None or calculateHash(firstBlock) != firstBlock.hash):
            return False

        return True

    def isValidBlock(self, block, previousBlock):
        if previousBlock.index + 1 != block.index:
            return False

        if (block.previousHash is None or block.previousHash != previousBlock.hash):
            return False

        if (block.hash is None or calculateHash(block) != block.hash):
            return False

        return True

    def isBlockchainValid(self):
        if not self.isFirstBlockValid():
            return False

        for i in range(1, len(self.blocks)):
            previousBlock = self.blocks[i - 1]
            block = self.blocks[i]
            if not self.isValidBlock(block, previousBlock):
                return False

        return True

    def display(self):
        for block in self.blocks:
            chain = "Block #" + str(block.index) + " [" + "\n\tindex: " + str(
                block.index) + "\n\tprevious hash: " + str(block.previousHash) + "\n\ttimestamp: " + str(
                block.timestamp) + "\n\tdata: " + str(block.data) + "\n\thash: " + str(
                block.hash) + "\n\tnonce: " + str(block.nonce) + "\n]\n"
            print(str(chain))


if __name__ == '__main__':
    bchain = Blockchain(4)

    blockn1 = bchain.newBlock("Second Block")
    bchain.addBlock(blockn1)

    blockn2 = bchain.newBlock("Third Block")
    bchain.addBlock(blockn2)

    blockn3 = bchain.newBlock("Fourth Block")
    bchain.addBlock(blockn3)

    print("Blockchain validity:", bchain.isBlockchainValid())

    bchain.display()