import time
import hashlib


class Block(object):

    def __init__(self, index, hash, previous_hash, transactions, nonce=0, timestamp=None):
        self.index = index
        self.nonce = nonce
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = timestamp or time.time()
        self.hash = hash

    @property
    def get_block_hash(self):
        block_string = "{}{}{}{}{}".format(self.index, self.nonce, self.previous_hash, self.transactions, self.timestamp)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def __repr__(self):
        return "{} - {} - {} - {} - {} - {}".format(self.index, self.hash, self.nonce, self.previous_hash, self.transactions, self.timestamp)

    def mine_block(self, difficulty):
        while self.hash[:difficulty] != ''.join(['0']*difficulty):
            self.nonce += 1
            self.hash = self.get_block_hash

class BlockChain(object):

    def __init__(self):
        self.chain = []
        self.current_node_transactions = []
        self.nodes = set()
        self.create_genesis_block()

    @property
    def get_serialized_chain(self):
        return [vars(block) for block in self.chain]

    @property
    def get_serialized_nodes(self):
        return list(self.nodes)

    def create_genesis_block(self):
        self.create_new_block(hash=0, previous_hash=0)

    def create_new_block(self, hash, previous_hash):
        block = Block(
            index=len(self.chain),
            hash=hash,
            previous_hash=previous_hash,
            transactions=self.current_node_transactions
        )
        self.current_node_transactions = []  # Reset the transaction list

        self.chain.append(block)

        return block

    @staticmethod
    def is_valid_block(block, previous_block):
        if previous_block.index + 1 != block.index:
            return False

        elif previous_block.get_block_hash != block.previous_hash:
            return False

        #elif not BlockChain.is_valid_proof(block.proof, previous_block.proof):
        #    return False

        elif block.timestamp <= previous_block.timestamp:
            return False

        return True

    def create_new_transaction(self, sender, recipient, data):
        self.current_node_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'data': data
        })
        return True

    @staticmethod
    def is_valid_transaction():
        # Not Implemented
        pass


    @property
    def get_last_block(self):
        return self.chain[-1]

    def is_valid_chain(self):
        """
        Check if given blockchain is valid
        """
        previous_block = self.chain[0]
        current_index = 1

        while current_index < len(self.chain):

            block = self.chain[current_index]

            if not self.is_valid_block(block, previous_block):
                return False

            previous_block = block
            current_index += 1

        return True

    def mine_block(self, miner_address):
        # Sender "0" means that this node has mined a new block
        # For mining the Block(or finding the proof), we must be awarded with some amount(in our case this is 1)


        last_block = self.get_last_block
        block = self.create_new_block(0,last_block.hash)
        block.hash = block.get_block_hash
        block.mine_block(5)

        return vars(block)  # Return a native Dict type object

    def create_node(self, address):
        self.nodes.add(address)
        return True

    @staticmethod
    def get_block_object_from_block_data(block_data):
        return Block(
            block_data['index'],
            block_data['hash'],
            block_data['previous_hash'],
            block_data['transactions'],
            nonce=block_data['nonce'],
            timestamp=block_data['timestamp']
        )