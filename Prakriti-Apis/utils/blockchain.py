import json
import hashlib
import os
from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId  # <-- ✅ import this

LEDGER_FILE = os.path.join(os.getcwd(), "blockchain_ledger.json")


class Blockchain:
    def __init__(self, mongo_uri="mongodb://localhost:27017", mongo_db="PrakritiAi", collection="blockchain"):
        self.chain = []
        self.mongo_client = MongoClient(mongo_uri)
        self.mongo_db = self.mongo_client[mongo_db]
        self.mongo_col = self.mongo_db[collection]
        self.load_chain()

    def load_chain(self):
        if os.path.exists(LEDGER_FILE):
            try:
                with open(LEDGER_FILE, "r") as f:
                    self.chain = json.load(f)
            except Exception:
                self.chain = []
        else:
            self.chain = []
            self.create_genesis_block()

    def create_genesis_block(self):
        if not self.chain:
            genesis_data = "Genesis Block"
            previous_hash = "0" * 64
            hash_val = self.compute_hash(genesis_data, previous_hash)
            genesis_block = {
                "index": 0,
                "timestamp": str(datetime.utcnow()),
                "data": genesis_data,
                "previous_hash": previous_hash,
                "hash": hash_val
            }
            self.chain.append(genesis_block)
            # save to MongoDB
            self.mongo_col.insert_one(genesis_block)
            self.save_chain()

    def compute_hash(self, data, previous_hash):
        block_string = f"{data}{previous_hash}{datetime.utcnow().isoformat()}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def add_block(self, data: dict):
        last_block = self.chain[-1] if self.chain else None
        previous_hash = last_block["hash"] if last_block else "0" * 64
        data_str = json.dumps(data, sort_keys=True)
        new_hash = self.compute_hash(data_str, previous_hash)

        block = {
            "index": len(self.chain),
            "timestamp": str(datetime.utcnow()),
            "data": data,
            "previous_hash": previous_hash,
            "hash": new_hash
        }

        # ✅ Insert into MongoDB
        inserted = self.mongo_col.insert_one(block)
        block["_id"] = str(inserted.inserted_id)  # convert ObjectId to string

        # ✅ Append to local chain (safe for JSON)
        self.chain.append(self._clean_block(block))
        self.save_chain()

        return new_hash

    def _clean_block(self, block):
        """Convert ObjectIds and other non-serializable objects to strings"""
        clean_block = {}
        for k, v in block.items():
            if isinstance(v, ObjectId):
                clean_block[k] = str(v)
            elif isinstance(v, dict):
                clean_block[k] = self._clean_block(v)
            else:
                clean_block[k] = v
        return clean_block

    def save_chain(self):
        # ✅ always clean blocks before writing
        cleaned_chain = [self._clean_block(b) for b in self.chain]
        with open(LEDGER_FILE, "w") as f:
            json.dump(cleaned_chain, f, indent=4)


# ✅ Singleton
blockchain = Blockchain()
