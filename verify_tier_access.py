"""
TIER ACCESS VERIFICATION
Run this to verify all tiers have correct module access

Usage:
    python verify_tier_access.py
"""

from tier_access_control import STUDENT_TIERS, get_tier_modules

def verify_all_tiers():
    """Verify all tier configurations match pricing page"""
    
    print("=" * 80)
    print("TIER ACCESS VERIFICATION - CRITICAL BUSINESS CHECK")
    print("=" * 80)
    
    errors = []
    
    for tier_id, tier_data in STUDENT_TIERS.items():
        print(f"\n{'=' * 80}")
        print(f"TIER: {tier_data['name']} (£{tier_data['price']}) - {tier_data['duration_days']} days")
        print(f"{'=' * 80}")
        
        modules = get_tier_modules(tier_id)
        print(f"📊 Total Modules Accessible: {len(modules)}")
        
        # Check critical modules
        critical_checks = {
            "Information Governance": "information_governance" in modules,
            "Partial Booking List": "partial_booking_list" in modules,
            "Certification Exam": "certification_exam" in modules,
            "Career Coach": "career_coach" in modules,
            "Cancer Pathways": "cancer_pathways" in modules,
            "MDT Coordination": "mdt_coordination" in modules
        }
        
        print("\n🔍 Critical Features Check:")
        for feature, has_access in critical_checks.items():
            status = "✅" if has_access else "❌"
            print(f"  {status} {feature}")
        
        # VERIFY AGAINST PRICING PAGE CLAIMS
        print("\n✔️  Verification Tests:")
        
        if tier_id == "taster":
            # £99 Taster checks
            if len(modules) >= 15:
                errors.append(f"❌ TASTER ERROR: Has {len(modules)} modules (should be <15)!")
                print(f"  ❌ FAIL: Too many modules ({len(modules)}, should be <15)")
            else:
                print(f"  ✅ PASS: Limited modules ({len(modules)})")
            
            if "certification_exam" in modules:
                errors.append("❌ TASTER ERROR: Has certification (shouldn't have it)!")
                print("  ❌ FAIL: Has certification exam (shouldn't)")
            else:
                print("  ✅ PASS: No certification exam")
            
            if "information_governance" in modules:
                errors.append("❌ TASTER ERROR: Has Information Governance (shouldn't)!")
                print("  ❌ FAIL: Has IG (shouldn't)")
            else:
                print("  ✅ PASS: No Information Governance")
        
        elif tier_id == "tier_1_practice":
            # £499 Tier 1 checks
            if len(modules) < 30:
                errors.append(f"❌ TIER 1 ERROR: Only {len(modules)} modules (should be 30+)!")
                print(f"  ❌ FAIL: Too few modules ({len(modules)}, should be 30+)")
            else:
                print(f"  ✅ PASS: Has 30+ modules ({len(modules)})")
            
            if "information_governance" not in modules:
                errors.append("❌ TIER 1 ERROR: Missing Information Governance!")
                print("  ❌ FAIL: Missing Information Governance")
            else:
                print("  ✅ PASS: Has Information Governance")
            
            if "partial_booking_list" not in modules:
                errors.append("❌ TIER 1 ERROR: Missing Partial Booking List!")
                print("  ❌ FAIL: Missing Partial Booking List")
            else:
                print("  ✅ PASS: Has Partial Booking List")
            
            if "certification_exam" in modules:
                errors.append("❌ TIER 1 ERROR: Has certification (shouldn't)!")
                print("  ❌ FAIL: Has certification (shouldn't)")
            else:
                print("  ✅ PASS: No certification exam (correct)")
            
            if "career_coach" in modules:
                errors.append("❌ TIER 1 ERROR: Has career coach (shouldn't)!")
                print("  ❌ FAIL: Has career coach (shouldn't)")
            else:
                print("  ✅ PASS: No career coach (correct)")
        
        elif tier_id == "tier_2_certified":
            # £1,299 Tier 2 checks
            if "certification_exam" not in modules:
                errors.append("❌ TIER 2 ERROR: Missing certification exam!")
                print("  ❌ FAIL: Missing certification exam")
            else:
                print("  ✅ PASS: Has certification exam")
            
            if "information_governance" not in modules:
                errors.append("❌ TIER 2 ERROR: Missing Information Governance!")
                print("  ❌ FAIL: Missing Information Governance")
            else:
                print("  ✅ PASS: Has Information Governance")
            
            if "partial_booking_list" not in modules:
                errors.append("❌ TIER 2 ERROR: Missing Partial Booking List!")
                print("  ❌ FAIL: Missing Partial Booking List")
            else:
                print("  ✅ PASS: Has Partial Booking List")
            
            if "career_coach" in modules:
                errors.append("❌ TIER 2 ERROR: Has career coach (that's Tier 3!)!")
                print("  ❌ FAIL: Has career coach (that's Tier 3)")
            else:
                print("  ✅ PASS: No career coach (correct)")
        
        elif tier_id == "tier_3_premium":
            # £1,799 Tier 3 checks
            if "career_coach" not in modules:
                errors.append("❌ TIER 3 ERROR: Missing career coach!")
                print("  ❌ FAIL: Missing career coach")
            else:
                print("  ✅ PASS: Has career coach")
            
            if "certification_exam" not in modules:
                errors.append("❌ TIER 3 ERROR: Missing certification!")
                print("  ❌ FAIL: Missing certification exam")
            else:
                print("  ✅ PASS: Has certification exam")
            
            if "information_governance" not in modules:
                errors.append("❌ TIER 3 ERROR: Missing Information Governance!")
                print("  ❌ FAIL: Missing Information Governance")
            else:
                print("  ✅ PASS: Has Information Governance")
    
    # FINAL RESULT
    print("\n" + "=" * 80)
    if errors:
        print("❌ VERIFICATION FAILED!")
        print("=" * 80)
        print("\n🚨 ERRORS FOUND:")
        for error in errors:
            print(error)
        print("\n⚠️  FIX THESE BEFORE TAKING PAYMENTS!")
    else:
        print("✅ ALL TIERS VERIFIED - CORRECT!")
        print("=" * 80)
        print("\n✅ All tiers match pricing page")
        print("✅ Access control is correct")
        print("✅ Ready for production")
    
    print("=" * 80)
    
    return len(errors) == 0


if __name__ == "__main__":
    success = verify_all_tiers()
    
    if not success:
        print("\n⚠️  CRITICAL: Fix tier access before deploying!")
        exit(1)
    else:
        print("\n🎉 SUCCESS: Tier access verified!")
        exit(0)
