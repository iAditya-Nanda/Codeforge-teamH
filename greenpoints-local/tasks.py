"""
Task Management System for Green Points Blockchain
"""

import time
import hashlib
import json
from typing import Dict, List, Optional
from enum import Enum


class TaskCategory(Enum):
    """Categories of green tasks"""
    RECYCLING = "recycling"
    ENERGY_SAVING = "energy_saving"
    TRANSPORTATION = "transportation"
    WASTE_REDUCTION = "waste_reduction"
    TREE_PLANTING = "tree_planting"
    WATER_CONSERVATION = "water_conservation"
    EDUCATION = "education"
    COMMUNITY = "community"
    OTHER = "other"


class TaskStatus(Enum):
    """Status of a task"""
    PENDING = "pending"
    COMPLETED = "completed"
    VERIFIED = "verified"
    REWARDED = "rewarded"
    REJECTED = "rejected"


class Task:
    """Represents a green task that can earn points"""
    
    def __init__(self, name: str, description: str, reward_points: float,
                 category: TaskCategory, difficulty: str = "easy",
                 verification_required: bool = False):
        """
        Initialize a task
        
        Args:
            name: Task name
            description: Detailed description
            reward_points: Green points awarded for completion
            category: Task category
            difficulty: Difficulty level (easy, medium, hard)
            verification_required: Whether task needs verification
        """
        self.task_id = self.generate_task_id(name)
        self.name = name
        self.description = description
        self.reward_points = reward_points
        self.category = category
        self.difficulty = difficulty
        self.verification_required = verification_required
        self.created_at = time.time()
        self.metadata = {}
    
    def generate_task_id(self, name: str) -> str:
        """Generate unique task ID"""
        task_string = f"{name}_{time.time()}"
        return hashlib.sha256(task_string.encode()).hexdigest()[:12]
    
    def to_dict(self) -> Dict:
        """Convert task to dictionary"""
        return {
            "task_id": self.task_id,
            "name": self.name,
            "description": self.description,
            "reward_points": self.reward_points,
            "category": self.category.value,
            "difficulty": self.difficulty,
            "verification_required": self.verification_required,
            "created_at": self.created_at,
            "metadata": self.metadata
        }
    
    def __str__(self) -> str:
        return f"Task({self.name}, {self.reward_points} GP)"


class TaskCompletion:
    """Represents a user's completion of a task"""
    
    def __init__(self, task_id: str, user_address: str, 
                 evidence: Optional[str] = None):
        """
        Initialize a task completion
        
        Args:
            task_id: ID of completed task
            user_address: Address of user who completed task
            evidence: Optional evidence/proof of completion
        """
        self.completion_id = self.generate_completion_id()
        self.task_id = task_id
        self.user_address = user_address
        self.evidence = evidence
        self.status = TaskStatus.PENDING
        self.completed_at = time.time()
        self.verified_at = None
        self.transaction_id = None
    
    def generate_completion_id(self) -> str:
        """Generate unique completion ID"""
        completion_string = f"{time.time()}_{hashlib.sha256(str(time.time()).encode()).hexdigest()}"
        return hashlib.sha256(completion_string.encode()).hexdigest()[:12]
    
    def verify(self) -> None:
        """Mark completion as verified"""
        self.status = TaskStatus.VERIFIED
        self.verified_at = time.time()
    
    def reject(self) -> None:
        """Mark completion as rejected"""
        self.status = TaskStatus.REJECTED
    
    def mark_rewarded(self, transaction_id: str) -> None:
        """Mark as rewarded with transaction ID"""
        self.status = TaskStatus.REWARDED
        self.transaction_id = transaction_id
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "completion_id": self.completion_id,
            "task_id": self.task_id,
            "user_address": self.user_address,
            "evidence": self.evidence,
            "status": self.status.value,
            "completed_at": self.completed_at,
            "verified_at": self.verified_at,
            "transaction_id": self.transaction_id
        }


class TaskManager:
    """Manages all tasks and task completions"""
    
    def __init__(self):
        self.tasks: Dict[str, Task] = {}  # task_id -> Task
        self.completions: List[TaskCompletion] = []
        self.initialize_default_tasks()
    
    def initialize_default_tasks(self) -> None:
        """Create some default green tasks"""
        default_tasks = [
            Task("Recycle Paper", "Recycle at least 5kg of paper", 50, 
                 TaskCategory.RECYCLING, "easy"),
            Task("Recycle Plastic", "Recycle at least 3kg of plastic bottles", 45,
                 TaskCategory.RECYCLING, "easy"),
            Task("Plant a Tree", "Plant a tree in your community", 100,
                 TaskCategory.TREE_PLANTING, "medium", True),
            Task("Use Public Transport", "Use public transport for a week", 75,
                 TaskCategory.TRANSPORTATION, "medium"),
            Task("Bike to Work", "Commute by bicycle for 5 days", 80,
                 TaskCategory.TRANSPORTATION, "medium"),
            Task("Save Electricity", "Reduce electricity usage by 20% this month", 120,
                 TaskCategory.ENERGY_SAVING, "hard", True),
            Task("LED Bulb Installation", "Replace 10 regular bulbs with LED", 60,
                 TaskCategory.ENERGY_SAVING, "easy"),
            Task("Composting", "Start composting kitchen waste for a month", 90,
                 TaskCategory.WASTE_REDUCTION, "medium"),
            Task("Zero Waste Shopping", "Shop without plastic packaging for a week", 70,
                 TaskCategory.WASTE_REDUCTION, "medium"),
            Task("Water Conservation", "Install water-saving devices", 55,
                 TaskCategory.WATER_CONSERVATION, "easy"),
            Task("Community Cleanup", "Organize or participate in community cleanup", 85,
                 TaskCategory.COMMUNITY, "medium", True),
            Task("Environmental Workshop", "Attend environmental education workshop", 40,
                 TaskCategory.EDUCATION, "easy"),
        ]
        
        for task in default_tasks:
            self.tasks[task.task_id] = task
    
    def add_task(self, task: Task) -> bool:
        """Add a new task"""
        if task.task_id in self.tasks:
            print(f"Task ID {task.task_id} already exists")
            return False
        
        self.tasks[task.task_id] = task
        print(f"✓ Task added: {task.name} ({task.reward_points} GP)")
        return True
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get task by ID"""
        return self.tasks.get(task_id)
    
    def get_all_tasks(self) -> List[Task]:
        """Get all available tasks"""
        return list(self.tasks.values())
    
    def get_tasks_by_category(self, category: TaskCategory) -> List[Task]:
        """Get tasks by category"""
        return [task for task in self.tasks.values() if task.category == category]
    
    def complete_task(self, task_id: str, user_address: str,
                      evidence: Optional[str] = None) -> Optional[TaskCompletion]:
        """
        Mark a task as completed by a user
        
        Args:
            task_id: ID of task to complete
            user_address: Address of user completing task
            evidence: Optional evidence of completion
        
        Returns:
            TaskCompletion object or None if task doesn't exist
        """
        task = self.get_task(task_id)
        if not task:
            print(f"Task {task_id} not found")
            return None
        
        completion = TaskCompletion(task_id, user_address, evidence)
        
        # Auto-verify if verification not required
        if not task.verification_required:
            completion.verify()
        
        self.completions.append(completion)
        print(f"✓ Task completed: {task.name}")
        
        if completion.status == TaskStatus.VERIFIED:
            print(f"  Auto-verified, ready for reward")
        else:
            print(f"  Pending verification")
        
        return completion
    
    def verify_completion(self, completion_id: str) -> bool:
        """Verify a task completion"""
        for completion in self.completions:
            if completion.completion_id == completion_id:
                completion.verify()
                print(f"✓ Completion verified: {completion_id}")
                return True
        return False
    
    def get_verified_completions(self, rewarded: bool = False) -> List[TaskCompletion]:
        """
        Get verified completions
        
        Args:
            rewarded: If True, get already rewarded; if False, get unrewarded
        
        Returns:
            List of task completions
        """
        if rewarded:
            return [c for c in self.completions if c.status == TaskStatus.REWARDED]
        else:
            return [c for c in self.completions if c.status == TaskStatus.VERIFIED]
    
    def get_user_completions(self, user_address: str) -> List[TaskCompletion]:
        """Get all completions by a user"""
        return [c for c in self.completions if c.user_address == user_address]
    
    def display_all_tasks(self) -> None:
        """Display all available tasks"""
        print("\n" + "="*80)
        print("AVAILABLE GREEN TASKS")
        print("="*80)
        print(f"Total Tasks: {len(self.tasks)}\n")
        
        # Group by category
        categories = {}
        for task in self.tasks.values():
            if task.category not in categories:
                categories[task.category] = []
            categories[task.category].append(task)
        
        for category, tasks in categories.items():
            print(f"\n📋 {category.value.upper().replace('_', ' ')}")
            print("-" * 80)
            for task in tasks:
                print(f"  ID: {task.task_id}")
                print(f"  Name: {task.name}")
                print(f"  Description: {task.description}")
                print(f"  Reward: {task.reward_points} GP")
                print(f"  Difficulty: {task.difficulty}")
                if task.verification_required:
                    print(f"  ⚠️  Verification Required")
                print()
    
    def display_leaderboard(self, blockchain) -> None:
        """Display user leaderboard by completed tasks"""
        print("\n" + "="*80)
        print("GREEN POINTS LEADERBOARD")
        print("="*80)
        
        user_stats = {}
        for completion in self.completions:
            if completion.status == TaskStatus.REWARDED:
                addr = completion.user_address
                if addr not in user_stats:
                    user_stats[addr] = {
                        "tasks_completed": 0,
                        "total_points": 0
                    }
                user_stats[addr]["tasks_completed"] += 1
                task = self.get_task(completion.task_id)
                if task:
                    user_stats[addr]["total_points"] += task.reward_points
        
        # Sort by total points
        sorted_users = sorted(user_stats.items(), 
                            key=lambda x: x[1]["total_points"], 
                            reverse=True)
        
        for i, (address, stats) in enumerate(sorted_users, 1):
            balance = blockchain.get_balance(address)
            print(f"{i}. Address: {address}")
            print(f"   Tasks Completed: {stats['tasks_completed']}")
            print(f"   Task Points Earned: {stats['total_points']} GP")
            print(f"   Current Balance: {balance} GP")
            print("-" * 80)
