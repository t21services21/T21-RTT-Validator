"""
APPROVAL & REQUEST SYSTEM
Handle all approval workflows in the platform

APPROVAL TYPES:
- Tier upgrade requests (Student: Tier 0 → Tier 1, 2, 3)
- Module access requests
- Staff account requests
- Special permissions
- Certificate requests
- Leave/extension requests
- Refund requests

WORKFLOW:
1. Student/user submits request
2. Notification sent to admin/staff
3. Admin reviews request
4. Admin approves/rejects
5. User notified of decision
6. If approved, access granted automatically

FEATURES:
- Auto-routing to correct approver
- Escalation (if not approved in X days)
- Request tracking
- Approval history
- Comments/notes
- Bulk approve
"""

from datetime import datetime, timedelta
import json
import os
from typing import List, Dict, Optional
import uuid


class ApprovalRequest:
    """Single approval request"""
    
    def __init__(self, request_data: dict):
        self.id = request_data.get('id', self._generate_id())
        self.request_type = request_data.get('request_type')  # tier_upgrade, module_access, etc.
        self.requester_email = request_data.get('requester_email')
        self.requester_name = request_data.get('requester_name')
        self.current_tier = request_data.get('current_tier')
        self.requested_tier = request_data.get('requested_tier')
        self.requested_item = request_data.get('requested_item')  # For module access, etc.
        self.reason = request_data.get('reason')
        self.additional_info = request_data.get('additional_info', {})
        self.status = request_data.get('status', 'pending')  # pending, approved, rejected, cancelled
        self.submitted_at = request_data.get('submitted_at', datetime.now().isoformat())
        self.reviewed_by = request_data.get('reviewed_by')
        self.reviewed_at = request_data.get('reviewed_at')
        self.reviewer_comment = request_data.get('reviewer_comment')
        self.priority = request_data.get('priority', 'normal')  # low, normal, high, urgent
        self.auto_approve = request_data.get('auto_approve', False)
    
    def _generate_id(self):
        return f"req_{uuid.uuid4().hex[:12]}"
    
    def to_dict(self):
        return {
            'id': self.id,
            'request_type': self.request_type,
            'requester_email': self.requester_email,
            'requester_name': self.requester_name,
            'current_tier': self.current_tier,
            'requested_tier': self.requested_tier,
            'requested_item': self.requested_item,
            'reason': self.reason,
            'additional_info': self.additional_info,
            'status': self.status,
            'submitted_at': self.submitted_at,
            'reviewed_by': self.reviewed_by,
            'reviewed_at': self.reviewed_at,
            'reviewer_comment': self.reviewer_comment,
            'priority': self.priority,
            'auto_approve': self.auto_approve
        }


# ============================================
# REQUEST SUBMISSION
# ============================================

def submit_tier_upgrade_request(requester_email: str, requester_name: str,
                                current_tier: str, requested_tier: str,
                                reason: str) -> ApprovalRequest:
    """
    Submit tier upgrade request
    
    Example: Student wants to upgrade from Tier 0 (trial) to Tier 1 (£499)
    """
    request_data = {
        'request_type': 'tier_upgrade',
        'requester_email': requester_email,
        'requester_name': requester_name,
        'current_tier': current_tier,
        'requested_tier': requested_tier,
        'reason': reason,
        'priority': 'high'  # Tier upgrades are important
    }
    
    request = ApprovalRequest(request_data)
    save_request(request)
    
    # Notify admins
    notify_approvers_new_request(request)
    
    # Notify requester
    notify_requester_submitted(request)
    
    return request


def submit_module_access_request(requester_email: str, requester_name: str,
                                 module_name: str, reason: str) -> ApprovalRequest:
    """Submit request for access to a specific module"""
    request_data = {
        'request_type': 'module_access',
        'requester_email': requester_email,
        'requester_name': requester_name,
        'requested_item': module_name,
        'reason': reason,
        'priority': 'normal'
    }
    
    request = ApprovalRequest(request_data)
    save_request(request)
    
    notify_approvers_new_request(request)
    notify_requester_submitted(request)
    
    return request


def submit_staff_account_request(requester_email: str, requester_name: str,
                                 requested_role: str, reason: str,
                                 additional_info: dict = None) -> ApprovalRequest:
    """Submit request for staff account"""
    request_data = {
        'request_type': 'staff_account',
        'requester_email': requester_email,
        'requester_name': requester_name,
        'requested_item': requested_role,
        'reason': reason,
        'additional_info': additional_info or {},
        'priority': 'high'
    }
    
    request = ApprovalRequest(request_data)
    save_request(request)
    
    notify_approvers_new_request(request)
    notify_requester_submitted(request)
    
    return request


# ============================================
# REQUEST MANAGEMENT
# ============================================

def save_request(request: ApprovalRequest):
    """Save request to database"""
    try:
        requests = load_all_requests()
        
        existing_index = None
        for i, req in enumerate(requests):
            if req['id'] == request.id:
                existing_index = i
                break
        
        if existing_index is not None:
            requests[existing_index] = request.to_dict()
        else:
            requests.append(request.to_dict())
        
        os.makedirs('data/approvals', exist_ok=True)
        with open('data/approvals/all_requests.json', 'w') as f:
            json.dump(requests, f, indent=2)
    
    except Exception as e:
        print(f"Error saving request: {e}")


def load_all_requests() -> List[dict]:
    """Load all requests"""
    try:
        with open('data/approvals/all_requests.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except Exception:
        return []


def get_pending_requests(request_type: str = None) -> List[ApprovalRequest]:
    """Get all pending requests, optionally filtered by type"""
    all_requests = load_all_requests()
    
    pending = [ApprovalRequest(r) for r in all_requests if r['status'] == 'pending']
    
    if request_type:
        pending = [r for r in pending if r.request_type == request_type]
    
    # Sort by priority and date
    priority_order = {'urgent': 1, 'high': 2, 'normal': 3, 'low': 4}
    pending.sort(key=lambda x: (priority_order.get(x.priority, 3), x.submitted_at))
    
    return pending


def get_user_requests(user_email: str) -> List[ApprovalRequest]:
    """Get all requests by a specific user"""
    all_requests = load_all_requests()
    
    user_requests = [ApprovalRequest(r) for r in all_requests 
                    if r['requester_email'] == user_email]
    
    # Sort by date (newest first)
    user_requests.sort(key=lambda x: x.submitted_at, reverse=True)
    
    return user_requests


def get_request_by_id(request_id: str) -> Optional[ApprovalRequest]:
    """Get specific request by ID"""
    all_requests = load_all_requests()
    
    for req in all_requests:
        if req['id'] == request_id:
            return ApprovalRequest(req)
    
    return None


# ============================================
# APPROVAL ACTIONS
# ============================================

def approve_request(request_id: str, approver_email: str, approver_name: str,
                   comment: str = "") -> bool:
    """
    Approve a request
    
    Returns:
        True if successful, False otherwise
    """
    request = get_request_by_id(request_id)
    if not request:
        return False
    
    # Update request
    request.status = 'approved'
    request.reviewed_by = approver_email
    request.reviewed_at = datetime.now().isoformat()
    request.reviewer_comment = comment
    
    save_request(request)
    
    # Take action based on request type
    execute_approval(request)
    
    # Notify requester
    notify_requester_approved(request)
    
    return True


def reject_request(request_id: str, approver_email: str, approver_name: str,
                  reason: str) -> bool:
    """Reject a request"""
    request = get_request_by_id(request_id)
    if not request:
        return False
    
    request.status = 'rejected'
    request.reviewed_by = approver_email
    request.reviewed_at = datetime.now().isoformat()
    request.reviewer_comment = reason
    
    save_request(request)
    
    # Notify requester
    notify_requester_rejected(request)
    
    return True


def execute_approval(request: ApprovalRequest):
    """Execute the approved action"""
    
    if request.request_type == 'tier_upgrade':
        # Upgrade user's tier
        upgrade_user_tier(request.requester_email, request.requested_tier)
    
    elif request.request_type == 'module_access':
        # Grant module access
        grant_module_access(request.requester_email, request.requested_item)
    
    elif request.request_type == 'staff_account':
        # Create staff account
        create_staff_account(request.requester_email, request.requested_item)


def upgrade_user_tier(user_email: str, new_tier: str):
    """Upgrade user to new tier"""
    # TODO: Integrate with your user management system
    print(f"Upgrading {user_email} to {new_tier}")


def grant_module_access(user_email: str, module_name: str):
    """Grant access to module"""
    # TODO: Integrate with module access system
    print(f"Granting {user_email} access to {module_name}")


def create_staff_account(user_email: str, role: str):
    """Create staff account"""
    # TODO: Integrate with user creation
    print(f"Creating {role} account for {user_email}")


# ============================================
# NOTIFICATIONS
# ============================================

def notify_approvers_new_request(request: ApprovalRequest):
    """Notify admins of new request"""
    try:
        from notification_system import create_notification, NotificationType, NotificationPriority
        
        # Get admin emails
        admin_emails = get_admin_emails()
        
        for admin_email in admin_emails:
            create_notification(
                user_email=admin_email,
                title=f"🔔 New {request.request_type.replace('_', ' ').title()} Request",
                message=f"{request.requester_name} has requested approval for {request.request_type.replace('_', ' ')}",
                notification_type=NotificationType.APPROVAL,
                priority=NotificationPriority.HIGH,
                action_url="/admin/approvals",
                action_label="Review Request",
                send_email=True,
                metadata={'request_id': request.id}
            )
    except Exception as e:
        print(f"Error notifying approvers: {e}")


def notify_requester_submitted(request: ApprovalRequest):
    """Notify requester that request was submitted"""
    try:
        from notification_system import create_notification, NotificationType, NotificationPriority
        
        create_notification(
            user_email=request.requester_email,
            title="✅ Request Submitted",
            message=f"Your {request.request_type.replace('_', ' ')} request has been submitted and is pending review.",
            notification_type=NotificationType.INFO,
            priority=NotificationPriority.MEDIUM,
            send_email=True,
            metadata={'request_id': request.id}
        )
    except Exception as e:
        print(f"Error notifying requester: {e}")


def notify_requester_approved(request: ApprovalRequest):
    """Notify requester that request was approved"""
    try:
        from notification_system import create_notification, NotificationType, NotificationPriority
        
        create_notification(
            user_email=request.requester_email,
            title="🎉 Request Approved!",
            message=f"Your {request.request_type.replace('_', ' ')} request has been approved! {request.reviewer_comment}",
            notification_type=NotificationType.SUCCESS,
            priority=NotificationPriority.HIGH,
            send_email=True,
            metadata={'request_id': request.id}
        )
    except Exception as e:
        print(f"Error notifying requester: {e}")


def notify_requester_rejected(request: ApprovalRequest):
    """Notify requester that request was rejected"""
    try:
        from notification_system import create_notification, NotificationType, NotificationPriority
        
        create_notification(
            user_email=request.requester_email,
            title="❌ Request Declined",
            message=f"Your {request.request_type.replace('_', ' ')} request has been declined. Reason: {request.reviewer_comment}",
            notification_type=NotificationType.WARNING,
            priority=NotificationPriority.MEDIUM,
            send_email=True,
            metadata={'request_id': request.id}
        )
    except Exception as e:
        print(f"Error notifying requester: {e}")


def get_admin_emails() -> List[str]:
    """Get list of admin emails who can approve requests"""
    # TODO: Get from your user database
    # For now, return a default list
    return ["admin@t21services.co.uk"]


# ============================================
# STATISTICS
# ============================================

def get_approval_statistics() -> dict:
    """Get statistics on approval requests"""
    all_requests = load_all_requests()
    
    total = len(all_requests)
    pending = len([r for r in all_requests if r['status'] == 'pending'])
    approved = len([r for r in all_requests if r['status'] == 'approved'])
    rejected = len([r for r in all_requests if r['status'] == 'rejected'])
    
    # Average time to approve
    approved_reqs = [r for r in all_requests if r['status'] == 'approved' and r.get('reviewed_at')]
    avg_hours = 0
    if approved_reqs:
        total_hours = 0
        for req in approved_reqs:
            submitted = datetime.fromisoformat(req['submitted_at'])
            reviewed = datetime.fromisoformat(req['reviewed_at'])
            hours = (reviewed - submitted).total_seconds() / 3600
            total_hours += hours
        avg_hours = total_hours / len(approved_reqs)
    
    return {
        'total': total,
        'pending': pending,
        'approved': approved,
        'rejected': rejected,
        'approval_rate': (approved / total * 100) if total > 0 else 0,
        'avg_approval_time_hours': round(avg_hours, 1)
    }


# Export
__all__ = [
    'ApprovalRequest',
    'submit_tier_upgrade_request',
    'submit_module_access_request',
    'submit_staff_account_request',
    'get_pending_requests',
    'get_user_requests',
    'get_request_by_id',
    'approve_request',
    'reject_request',
    'get_approval_statistics'
]
