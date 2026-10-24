from client import AutonomousJsonSchemaDiffPatcherClient
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

def main():
    patcher = AutonomousJsonSchemaDiffPatcherClient()
    print("=== AUTONOMOUS JSON SCHEMA DIFF PATCHER ===")
    
    v1_schema = {
        "user_id": "string",
        "email": "string",
        "legacy_phone_number": "string",
        "preferences": {"newsletter": True, "theme": "dark"}
    }
    
    v2_schema = {
        "user_id": "string",
        "email": "string",
        "mobile_phone": "string", # legacy_phone_number removed, mobile_phone added -> Breaking
        "preferences": {"newsletter": True, "theme": "system", "locale": "en_US"}
    }
    
    res = patcher.analyze_schema_evolution(v1_schema, v2_schema, current_version="1.4.0")
    print()
    print(f"Current: v{res['current_version']} -> Target Recommended: v{res['recommended_version']}")
    print(f"Evolution Class: {res['evolution_type']} (Breaking: {res['is_breaking']})")
    if res['breaking_reasons']:
        print("Breaking Changes Detected:")
        for r in res['breaking_reasons']:
            print(f"  - {r}")
    print()
    print(f"RFC 6902 JSON Patch ({res['total_patch_operations']} ops):")
    for op in res['rfc6902_json_patch']:
        print(f"  - [{op['op'].upper()}] {op['path']}")

if __name__ == "__main__":
    main()
