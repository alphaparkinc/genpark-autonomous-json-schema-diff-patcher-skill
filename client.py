import json, sys
sys.stdout.reconfigure(encoding='utf-8')

class AutonomousJsonSchemaDiffPatcherClient:
    """
    Schema evolution analyzer. Compares two JSON object models or JSON Schemas,
    generates RFC 6902 standard JSON Patch operations ('add', 'remove', 'replace'),
    and classifies whether changes are BREAKING (Major) or NON-BREAKING (Minor/Patch).
    """
    def __init__(self):
        pass

    def compute_diff(self, old_obj, new_obj, path=""):
        patches = []
        breaking_flags = []

        if isinstance(old_obj, dict) and isinstance(new_obj, dict):
            # Check removed keys (Breaking Change)
            for k in old_obj:
                curr_path = f"{path}/{k}"
                if k not in new_obj:
                    patches.append({"op": "remove", "path": curr_path})
                    breaking_flags.append(f"Field '{curr_path}' was removed")
                else:
                    sub_patches, sub_breaking = self.compute_diff(old_obj[k], new_obj[k], curr_path)
                    patches.extend(sub_patches)
                    breaking_flags.extend(sub_breaking)

            # Check added keys (Non-breaking unless required)
            for k in new_obj:
                curr_path = f"{path}/{k}"
                if k not in old_obj:
                    patches.append({"op": "add", "path": curr_path, "value": new_obj[k]})

        elif isinstance(old_obj, list) and isinstance(new_obj, list):
            # Array diff
            for i, val in enumerate(new_obj):
                curr_path = f"{path}/{i}"
                if i < len(old_obj):
                    if old_obj[i] != val:
                        patches.append({"op": "replace", "path": curr_path, "value": val})
                else:
                    patches.append({"op": "add", "path": curr_path, "value": val})
            for i in range(len(new_obj), len(old_obj)):
                patches.append({"op": "remove", "path": f"{path}/{i}"})

        else:
            # Primitive value comparison
            if old_obj != new_obj:
                patches.append({"op": "replace", "path": path, "value": new_obj})
                if type(old_obj) != type(new_obj):
                    breaking_flags.append(f"Type mutation at '{path}': {type(old_obj).__name__} -> {type(new_obj).__name__}")

        return patches, breaking_flags

    def analyze_schema_evolution(self, current_schema, target_schema, current_version="1.0.0"):
        patches, breaking_flags = self.compute_diff(current_schema, target_schema)
        
        is_breaking = len(breaking_flags) > 0
        v_parts = [int(x) for x in current_version.split('.')]
        if is_breaking:
            recommended_version = f"{v_parts[0] + 1}.0.0"
            change_type = "MAJOR_BREAKING_CHANGE"
        elif len(patches) > 0:
            recommended_version = f"{v_parts[0]}.{v_parts[1] + 1}.0"
            change_type = "MINOR_BACKWARD_COMPATIBLE_EXPANSION"
        else:
            recommended_version = current_version
            change_type = "NO_SCHEMA_MUTATION"

        return {
            "status": "success",
            "current_version": current_version,
            "recommended_version": recommended_version,
            "evolution_type": change_type,
            "is_breaking": is_breaking,
            "breaking_reasons": breaking_flags,
            "total_patch_operations": len(patches),
            "rfc6902_json_patch": patches
        }
