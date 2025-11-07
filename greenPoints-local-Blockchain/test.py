#!/usr/bin/env python3
"""
Test script to verify the Green Points Blockchain implementation
"""

def test_blockchain_core():
    """Test basic blockchain functionality"""
    print("Testing blockchain core...")
    from blockchain import Blockchain, Block
    
    # Create blockchain
    bc = Blockchain(difficulty=2)
    assert len(bc.chain) == 1, "Genesis block should exist"
    assert bc.chain[0].index == 0, "Genesis block index should be 0"
    
    # Add transaction
    tx = {"from": "Alice", "to": "Bob", "amount": 50}
    bc.add_transaction(tx)
    assert len(bc.pending_transactions) == 1, "Transaction should be pending"
    
    # Mine block
    bc.mine_pending_transactions("Miner")
    assert len(bc.chain) == 2, "New block should be mined"
    assert len(bc.pending_transactions) == 0, "Pending should be cleared"
    
    # Validate chain
    assert bc.is_chain_valid(), "Chain should be valid"
    
    print("✓ Blockchain core tests passed")


def test_wallet_system():
    """Test wallet and user management"""
    print("Testing wallet system...")
    from wallet import UserManager, Wallet
    
    # Create user manager
    um = UserManager()
    
    # Create wallets
    alice = um.create_wallet("alice", "alice@test.com")
    bob = um.create_wallet("bob")
    
    assert alice is not None, "Alice's wallet should be created"
    assert bob is not None, "Bob's wallet should be created"
    assert um.get_user_count() == 2, "Should have 2 users"
    
    # Test retrieval
    alice_wallet = um.get_wallet_by_username("alice")
    assert alice_wallet.username == "alice", "Should retrieve Alice"
    
    # Test duplicate prevention
    duplicate = um.create_wallet("alice")
    assert duplicate is None, "Duplicate username should be rejected"
    
    print("✓ Wallet system tests passed")


def test_transaction_system():
    """Test transaction creation and validation"""
    print("Testing transaction system...")
    from transaction import Transaction, TransactionPool
    
    # Create transaction
    tx = Transaction("Alice", "Bob", 100, "transfer")
    assert tx.amount == 100, "Amount should be 100"
    assert tx.is_valid(), "Transaction should be valid"
    
    # Test invalid transaction
    invalid_tx = Transaction("Alice", "Bob", -50, "transfer")
    assert not invalid_tx.is_valid(), "Negative amount should be invalid"
    
    # Test transaction pool
    pool = TransactionPool()
    pool.add_transaction(tx)
    assert pool.get_count() == 1, "Pool should have 1 transaction"
    
    print("✓ Transaction system tests passed")


def test_task_system():
    """Test task management"""
    print("Testing task system...")
    from tasks import TaskManager, Task, TaskCategory
    
    # Create task manager
    tm = TaskManager()
    initial_count = len(tm.get_all_tasks())
    assert initial_count > 0, "Should have default tasks"
    
    # Create and add new task
    new_task = Task(
        "Test Task",
        "This is a test",
        25,
        TaskCategory.OTHER,
        "easy"
    )
    tm.add_task(new_task)
    assert len(tm.get_all_tasks()) == initial_count + 1, "Task should be added"
    
    # Complete task
    completion = tm.complete_task(new_task.task_id, "user_address", "evidence")
    assert completion is not None, "Completion should be created"
    
    print("✓ Task system tests passed")


def test_integration():
    """Test full integration workflow"""
    print("Testing integration workflow...")
    from blockchain import Blockchain
    from wallet import UserManager
    from tasks import TaskManager
    from transaction import Transaction
    
    # Initialize
    bc = Blockchain(difficulty=2)
    um = UserManager()
    tm = TaskManager()
    
    # Create users
    alice = um.create_wallet("alice")
    bob = um.create_wallet("bob")
    
    # Alice completes a task
    tasks = tm.get_all_tasks()
    task = tasks[0]
    completion = tm.complete_task(task.task_id, alice.address, "Done!")
    
    # Create reward transaction
    if completion.status.value == "verified":
        tx = Transaction(
            "SYSTEM",
            alice.address,
            task.reward_points,
            "task_reward",
            task.task_id,
            task.name
        )
        bc.add_transaction(tx.to_dict())
    
    # Mine block
    bc.mine_pending_transactions(bob.address)
    
    # Verify balances
    alice_balance = bc.get_balance(alice.address)
    bob_balance = bc.get_balance(bob.address)
    
    assert alice_balance == task.reward_points, "Alice should have task reward"
    assert bob_balance == bc.mining_reward, "Bob should have mining reward"
    
    # Verify chain
    assert bc.is_chain_valid(), "Chain should be valid"
    
    print("✓ Integration tests passed")


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*80)
    print("🧪 RUNNING GREEN POINTS BLOCKCHAIN TESTS")
    print("="*80 + "\n")
    
    tests = [
        test_blockchain_core,
        test_wallet_system,
        test_transaction_system,
        test_task_system,
        test_integration
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ Test failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ Test error: {e}")
            failed += 1
    
    print("\n" + "="*80)
    print(f"TEST RESULTS: {passed} passed, {failed} failed")
    print("="*80)
    
    if failed == 0:
        print("\n🎉 All tests passed! The blockchain is working correctly! 🎉\n")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the errors above.\n")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(run_all_tests())
