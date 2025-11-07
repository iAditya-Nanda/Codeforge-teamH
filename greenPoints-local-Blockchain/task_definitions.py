"""
Task Management System for Green Points Blockchain - User App Version
Focuses on waste disposal and litter reporting tasks
"""

import time
import hashlib
from typing import Dict, List, Optional
from enum import Enum


class TaskType(Enum):
    """Types of tasks users can complete"""
    WASTE_DISPOSAL = "waste_disposal"  # Properly disposing waste in correct bins
    LITTER_REPORT = "litter_report"  # Reporting littered spots
    QR_SCAN = "qr_scan"  # Scanning QR at eco-businesses
    
    # Optional additional tasks
    RECYCLING = "recycling"
    ENERGY_SAVING = "energy_saving"
    TRANSPORTATION = "transportation"
    TREE_PLANTING = "tree_planting"
    COMMUNITY = "community"


class TaskDefinition:
    """Defines a task type and its reward"""
    
    def __init__(self, task_type: TaskType, name: str, description: str,
                 base_reward: float, requires_verification: bool = True,
                 verification_criteria: Optional[str] = None):
        self.task_type = task_type
        self.name = name
        self.description = description
        self.base_reward = base_reward
        self.requires_verification = requires_verification
        self.verification_criteria = verification_criteria or ""
        self.metadata = {}
    
    def to_dict(self) -> Dict:
        return {
            "task_type": self.task_type.value,
            "name": self.name,
            "description": self.description,
            "base_reward": self.base_reward,
            "requires_verification": self.requires_verification,
            "verification_criteria": self.verification_criteria
        }


class TaskManager:
    """Manages task definitions and completions"""
    
    def __init__(self):
        self.task_definitions: Dict[TaskType, TaskDefinition] = {}
        self.initialize_default_tasks()
    
    def initialize_default_tasks(self):
        """Create default task definitions"""
        
        # Main tasks for the app
        self.task_definitions[TaskType.WASTE_DISPOSAL] = TaskDefinition(
            TaskType.WASTE_DISPOSAL,
            "Proper Waste Disposal",
            "Dispose waste in the correct bin (recyclable, organic, or general waste)",
            base_reward=20.0,
            requires_verification=True,
            verification_criteria="Photo showing waste being disposed in correct bin with visible bin label"
        )
        
        self.task_definitions[TaskType.LITTER_REPORT] = TaskDefinition(
            TaskType.LITTER_REPORT,
            "Report Littered Spot",
            "Report a littered location for cleanup",
            base_reward=30.0,
            requires_verification=True,
            verification_criteria="Photo of littered area with visible location/landmark"
        )
        
        self.task_definitions[TaskType.QR_SCAN] = TaskDefinition(
            TaskType.QR_SCAN,
            "Eco-Business Visit",
            "Visit and support an eco-registered business",
            base_reward=0.0,  # Reward set by business
            requires_verification=False,
            verification_criteria="Valid QR code from registered business"
        )
        
        # Optional additional tasks
        self.task_definitions[TaskType.RECYCLING] = TaskDefinition(
            TaskType.RECYCLING,
            "Recycling Achievement",
            "Recycle at least 5kg of materials",
            base_reward=50.0,
            requires_verification=True,
            verification_criteria="Photo of recycling with visible weight/quantity"
        )
        
        self.task_definitions[TaskType.TREE_PLANTING] = TaskDefinition(
            TaskType.TREE_PLANTING,
            "Plant a Tree",
            "Plant a tree in your community",
            base_reward=100.0,
            requires_verification=True,
            verification_criteria="Photo of planted tree with visible sapling"
        )
        
        self.task_definitions[TaskType.COMMUNITY] = TaskDefinition(
            TaskType.COMMUNITY,
            "Community Cleanup",
            "Participate in community cleanup event",
            base_reward=80.0,
            requires_verification=True,
            verification_criteria="Photo from cleanup event showing participation"
        )
    
    def get_task(self, task_type: TaskType) -> Optional[TaskDefinition]:
        """Get task definition by type"""
        return self.task_definitions.get(task_type)
    
    def get_all_tasks(self) -> List[TaskDefinition]:
        """Get all task definitions"""
        return list(self.task_definitions.values())
    
    def get_tasks_for_frontend(self) -> List[Dict]:
        """Get all tasks in JSON format for frontend"""
        return [task.to_dict() for task in self.get_all_tasks()]
    
    def calculate_reward(self, task_type: TaskType, **kwargs) -> float:
        """
        Calculate reward for a task (can be customized based on parameters)
        
        Args:
            task_type: Type of task
            **kwargs: Additional parameters (e.g., weight for recycling)
        
        Returns:
            Reward amount in GP
        """
        task = self.get_task(task_type)
        if not task:
            return 0.0
        
        reward = task.base_reward
        
        # Custom reward calculation for specific tasks
        if task_type == TaskType.RECYCLING:
            weight = kwargs.get('weight', 5)  # kg
            reward = min(weight * 10, 150)  # 10 GP per kg, max 150 GP
        
        elif task_type == TaskType.LITTER_REPORT:
            severity = kwargs.get('severity', 'medium')  # low, medium, high
            severity_multiplier = {
                'low': 1.0,
                'medium': 1.2,
                'high': 1.5
            }
            reward = task.base_reward * severity_multiplier.get(severity, 1.0)
        
        return round(reward, 2)
    
    def create_task_summary(self, task_type: TaskType, user_id: int,
                           evidence: str, **kwargs) -> Dict:
        """
        Create a task completion summary
        
        Returns:
            Dictionary with task details for submission
        """
        task = self.get_task(task_type)
        if not task:
            return {}
        
        reward = self.calculate_reward(task_type, **kwargs)
        
        return {
            "task_type": task_type.value,
            "task_name": task.name,
            "user_id": user_id,
            "evidence": evidence,
            "reward_amount": reward,
            "requires_verification": task.requires_verification,
            "timestamp": time.time(),
            "metadata": kwargs
        }


def get_waste_disposal_task_info() -> Dict:
    """Get detailed info for waste disposal task (for frontend)"""
    return {
        "task_type": "waste_disposal",
        "name": "Proper Waste Disposal",
        "description": "Dispose waste in the correct bin",
        "reward": 20,
        "instructions": [
            "Identify your waste type (recyclable, organic, or general)",
            "Find the appropriate bin",
            "Take a photo showing the waste and bin label",
            "Dispose the waste properly",
            "Submit the photo for verification"
        ],
        "verification_time": "Usually within 24 hours",
        "tips": [
            "Make sure the bin label is clearly visible in the photo",
            "Photo should show the waste being disposed",
            "One submission per waste disposal instance"
        ]
    }


def get_litter_report_task_info() -> Dict:
    """Get detailed info for litter reporting task (for frontend)"""
    return {
        "task_type": "litter_report",
        "name": "Report Littered Spot",
        "description": "Help clean up the community by reporting littered locations",
        "reward": "30-45 GP (based on severity)",
        "instructions": [
            "Find a littered location",
            "Take a clear photo showing the litter",
            "Include visible landmarks for location identification",
            "Add location details (GPS coordinates auto-captured)",
            "Describe the type and amount of litter",
            "Submit for verification"
        ],
        "severity_levels": {
            "low": {"description": "Minor litter, few items", "reward": 30},
            "medium": {"description": "Moderate litter, multiple items", "reward": 36},
            "high": {"description": "Heavy litter, large area affected", "reward": 45}
        },
        "verification_time": "Usually within 24 hours",
        "tips": [
            "Clear photos help faster verification",
            "Include street name or landmark if possible",
            "Report responsibly - false reports may result in penalties"
        ]
    }


def get_business_visit_task_info() -> Dict:
    """Get detailed info for eco-business visit task (for frontend)"""
    return {
        "task_type": "qr_scan",
        "name": "Support Eco-Businesses",
        "description": "Earn rewards by visiting eco-registered businesses",
        "reward": "Varies by business (typically 10-50 GP)",
        "instructions": [
            "Visit an eco-registered business",
            "Make a purchase or use their service",
            "Ask for the Green Points QR code",
            "Scan the QR code with the app",
            "Rewards are instant (no verification needed)"
        ],
        "benefits": [
            "Support sustainable businesses",
            "Instant GP rewards",
            "Discover eco-friendly services",
            "Exclusive business offers"
        ],
        "tips": [
            "Look for businesses with 'Eco-Registered' badge",
            "QR codes are one-time use only",
            "Some QR codes may have expiration times"
        ]
    }
