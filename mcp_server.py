import sys, json
from client import AutonomousJsonSchemaDiffPatcherClient
sys.stdout.reconfigure(encoding='utf-8')

def handle_mcp():
    patcher = AutonomousJsonSchemaDiffPatcherClient()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps({"status": "ready", "skill": "genpark-autonomous-json-schema-diff-patcher-skill"}))
        return
    req = json.loads(sys.stdin.read() or "{}")
    s1 = req.get("schema_old", {})
    s2 = req.get("schema_new", {})
    v = req.get("current_version", "1.0.0")
    res = patcher.analyze_schema_evolution(s1, s2, current_version=v)
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    handle_mcp()
