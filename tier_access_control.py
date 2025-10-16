"""
TIER ACCESS CONTROL - Student Pricing Tiers
Matches pages/pricing.py pricing structure EXACTLY

CRITICAL: This defines what each tier can access
- £99 Taster: LIMITED access
- £499 Tier 1: FULL access (55+ modules) EXCEPT certification
- £1,299 Tier 2: FULL access + Certification
- £1,799 Tier 3: FULL access + Certification + Career Coach
"""

# ============================================
# STUDENT TIER DEFINITIONS
# ============================================

STUDENT_TIERS = {
    "taster": {
        "name": "Taster",
        "price": 99,
        "currency": "GBP",
        "duration_days": 30,
        "description": "Try the platform - limited access",
        "tier_level": 0,
        "modules_allowed": [
            # VERY LIMITED ACCESS
            "training_library_basic",  # Only 50 scenarios, not all 522
            "ai_tutor_limited",  # 10 questions per day limit
            "pathway_validator_basic",  # Basic validation only
            "interview_prep",
            "cv_builder",
            "learning_portal_basic"
        ],
        "modules_denied": [
            "information_governance",
            "partial_booking_list",
            "cancer_pathways",
            "mdt_coordination",
            "ptl_management",
            "advanced_booking",
            "certification_exam",
            "executive_dashboard",
            "clinical_workflows_advanced"
        ],
        "features": [
            "Try the platform",
            "Limited AI tutor (10 Q/day)",
            "Basic training modules (50 scenarios)",
            "NO certification",
            "NO advanced features"
        ],
        "restrictions": {
            "ai_tutor_daily_limit": 10,
            "scenarios_limit": 50,
            "no_certification": True,
            "no_advanced_clinical": True,
            "no_information_governance": True,
            "no_pbl": True
        }
    },
    
    "tier_1_practice": {
        "name": "Tier 1 Practice",
        "price": 499,
        "currency": "GBP",
        "duration_days": 180,  # 6 months
        "description": "Full platform access (55+ modules)",
        "tier_level": 1,
        "modules_allowed": [
            # FULL ACCESS TO EVERYTHING EXCEPT CERTIFICATION
            "patient_administration_hub",
            "learning_portal",
            "teaching_assessment",
            "clinical_workflows",
            "information_governance",  # INCLUDED!
            "partial_booking_list",  # INCLUDED!
            "task_management",
            "ai_automation",
            "reports_analytics",
            "training_certification_no_exam",
            "career_development",
            "administration",
            # All 522 scenarios
            "training_library_full",
            "ai_tutor_unlimited",
            "ptl_management",
            "cancer_pathways",
            "mdt_coordination",
            "advanced_booking",
            "clinical_letters",
            "dna_management",
            "cancellation_management",
            "patient_choice",
            "waiting_list_validator",
            "transfer_of_care",
            "executive_dashboard",
            "data_quality",
            "audit_compliance"
        ],
        "modules_denied": [
            "certification_exam",  # NO CERTIFICATION!
            "career_coach"  # NO CAREER COACH
        ],
        "features": [
            "Full platform access (55+ modules)",
            "AI Auto-Validator",
            "DNA Management",
            "Cancellation Management",
            "All 12 RTT core modules",
            "Information Governance (GDPR/Caldicott)",
            "Partial Booking List (PBL)",
            "522 training scenarios",
            "Unlimited AI tutor",
            "CV & interview prep",
            "NO certification"
        ],
        "restrictions": {
            "no_certification_exam": True,
            "no_career_coach": True
        }
    },
    
    "tier_2_certified": {
        "name": "Tier 2 Certified",
        "price": 1299,
        "currency": "GBP",
        "duration_days": 365,  # 12 months
        "description": "Everything in Tier 1 + Certification",
        "tier_level": 2,
        "modules_allowed": [
            # INHERIT ALL TIER 1 MODULES +
            "*tier_1_practice",
            # PLUS CERTIFICATION
            "certification_exam",
            "multi_tier_certification",
            "1000_question_bank",
            "exam_analytics",
            "job_application_support",
            "alumni_network",
            "certificate_verification"
        ],
        "modules_denied": [
            "career_coach"  # Still no career coach (that's Tier 3)
        ],
        "features": [
            "Everything in Tier 1",
            "Certified qualification (TQUK-endorsed)",
            "Multi-tier certification (Foundation/Practitioner/Expert)",
            "1000+ exam questions (unique per student)",
            "Job application support",
            "Alumni network (lifetime)",
            "10 months post-cert access"
        ],
        "restrictions": {
            "no_career_coach": True
        }
    },
    
    "tier_3_premium": {
        "name": "Tier 3 Premium",
        "price": 1799,
        "currency": "GBP",
        "duration_days": 365,  # 12 months
        "description": "Everything + Career Support",
        "tier_level": 3,
        "modules_allowed": [
            # INHERIT ALL TIER 2 MODULES +
            "*tier_2_certified",
            # PLUS CAREER COACHING
            "career_coach",
            "interview_scheduling",
            "application_monitoring",
            "cv_professional_review",
            "mock_interviews",
            "salary_negotiation",
            "job_search_support"
        ],
        "modules_denied": [],
        "features": [
            "Everything in Tier 2",
            "Job application support (CV, forms, monitoring)",
            "Dedicated career coach",
            "Interview preparation & scheduling",
            "Ongoing support (no employment guarantee)"
        ],
        "restrictions": {}
    }
}


# ============================================
# HELPER FUNCTIONS
# ============================================

def get_tier_modules(tier_name: str) -> list:
    """
    Get all modules for a tier (including inherited)
    
    Args:
        tier_name: 'taster', 'tier_1_practice', 'tier_2_certified', 'tier_3_premium'
    
    Returns:
        List of module IDs user has access to
    """
    if tier_name not in STUDENT_TIERS:
        return []
    
    tier = STUDENT_TIERS[tier_name]
    modules = []
    
    for module in tier['modules_allowed']:
        if module.startswith('*'):
            # Inherit from another tier
            parent_tier = module[1:]
            modules.extend(get_tier_modules(parent_tier))
        else:
            modules.append(module)
    
    return list(set(modules))  # Remove duplicates


def user_has_access_to_module(user_tier: str, module_id: str) -> bool:
    """
    Check if user's tier has access to a module
    
    Args:
        user_tier: User's tier ('taster', 'tier_1_practice', etc.)
        module_id: Module to check access for
    
    Returns:
        True if user has access, False otherwise
    """
    if user_tier not in STUDENT_TIERS:
        return False
    
    tier_modules = get_tier_modules(user_tier)
    
    # Check if module is explicitly denied
    denied_modules = STUDENT_TIERS[user_tier].get('modules_denied', [])
    if module_id in denied_modules:
        return False
    
    # Check direct match
    if module_id in tier_modules:
        return True
    
    # Check wildcards
    for tier_module in tier_modules:
        if tier_module.endswith('_full') and module_id.startswith(tier_module.replace('_full', '')):
            return True
    
    return False


def get_tier_restrictions(user_tier: str) -> dict:
    """Get restrictions for a tier"""
    if user_tier not in STUDENT_TIERS:
        return {}
    
    return STUDENT_TIERS[user_tier].get('restrictions', {})


def get_tier_info(tier_name: str) -> dict:
    """Get full tier information"""
    return STUDENT_TIERS.get(tier_name, {})


def get_all_tiers() -> dict:
    """Get all tier definitions"""
    return STUDENT_TIERS


# Export
__all__ = [
    'STUDENT_TIERS',
    'get_tier_modules',
    'user_has_access_to_module',
    'get_tier_restrictions',
    'get_tier_info',
    'get_all_tiers'
]
