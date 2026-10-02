#!/usr/bin/env python3
"""
tools/verify_assets.py
Verifies all startup image assets according to implementation/ASSET_ACCEPTANCE.md
and data/asset_manifest.json.
"""

import hashlib
import json
import os
import sys
from PIL import Image

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MANIFEST_PATH = os.path.join(REPO_ROOT, "data", "asset_manifest.json")
STARTUPS_JSON_PATH = os.path.join(REPO_ROOT, "data", "startups.json")
PUBLIC_ASSETS_DIR = os.path.join(REPO_ROOT, "apps", "web", "public")
SOURCE_ASSETS_DIR = os.path.join(REPO_ROOT, "assets", "source")

EXPECTED_VARIANTS = {
    "desktop": {"width": 1280, "height": 800, "max_bytes": 350 * 1024},
    "mobile": {"width": 600, "height": 750, "max_bytes": 200 * 1024},
    "thumb": {"width": 320, "height": 320, "max_bytes": 50 * 1024},
}


def compute_sha256(filepath: str) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    print("=== STARTUP KILLER ASSET VERIFICATION ===")

    # 1. Load manifest and startups.json
    if not os.path.exists(MANIFEST_PATH):
        print(f"ERROR: Manifest not found at {MANIFEST_PATH}")
        return 1

    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    with open(STARTUPS_JSON_PATH, "r", encoding="utf-8") as f:
        startups_data = json.load(f)

    expected_slugs = {s["slug"] for s in startups_data.get("startups", [])}
    manifest_assets = manifest.get("assets", [])
    manifest_slugs = {a["slug"] for a in manifest_assets}

    if expected_slugs != manifest_slugs:
        print(f"ERROR: Slugs mismatch! Missing: {expected_slugs - manifest_slugs}, Extra: {manifest_slugs - expected_slugs}")
        return 1

    total_images = 0
    passed_images = 0
    errors = []

    print(f"\nChecking 10 startups ({len(expected_slugs)} slugs):")
    for asset in manifest_assets:
        slug = asset["slug"]
        print(f"\n-> Startup [{slug}]:")

        # Check source master.jpg
        master_path = os.path.join(SOURCE_ASSETS_DIR, slug, "master.jpg")
        if not os.path.exists(master_path):
            errors.append(f"Missing master.jpg for {slug} at {master_path}")
            print(f"   [FAIL] master.jpg not found: {master_path}")
        else:
            try:
                with Image.open(master_path) as m_img:
                    print(f"   [PASS] master.jpg exists ({m_img.width}x{m_img.height}, {os.path.getsize(master_path) / 1024:.1f} KiB)")
            except Exception as e:
                errors.append(f"Cannot decode master.jpg for {slug}: {e}")
                print(f"   [FAIL] master.jpg decode error: {e}")

        files = asset.get("files", {})
        expected_sha = asset.get("sha256", {})

        for variant, spec in EXPECTED_VARIANTS.items():
            total_images += 1
            rel_file = files.get(variant)
            if not rel_file:
                errors.append(f"{slug} {variant}: path missing in manifest")
                print(f"   [FAIL] {variant}: missing path in manifest")
                continue

            # Full file path in public dir
            clean_rel = rel_file.lstrip("/")
            file_path = os.path.join(PUBLIC_ASSETS_DIR, clean_rel)

            if not os.path.exists(file_path):
                errors.append(f"{slug} {variant}: file not found at {file_path}")
                print(f"   [FAIL] {variant}: file not found ({file_path})")
                continue

            # Verify size
            file_size = os.path.getsize(file_path)
            max_bytes = spec["max_bytes"]
            if file_size > max_bytes:
                errors.append(f"{slug} {variant}: size {file_size} exceeds max {max_bytes} bytes")
                print(f"   [FAIL] {variant}: size {file_size / 1024:.1f} KiB > {max_bytes / 1024:.1f} KiB")
                continue

            # Verify dimensions & decode
            try:
                with Image.open(file_path) as img:
                    if (img.width, img.height) != (spec["width"], spec["height"]):
                        errors.append(f"{slug} {variant}: dim {img.width}x{img.height} != expected {spec['width']}x{spec['height']}")
                        print(f"   [FAIL] {variant}: dim {img.width}x{img.height} != {spec['width']}x{spec['height']}")
                        continue
                    if img.format != "WEBP":
                        errors.append(f"{slug} {variant}: format {img.format} != WEBP")
                        print(f"   [FAIL] {variant}: format is not WEBP ({img.format})")
                        continue
            except Exception as e:
                errors.append(f"{slug} {variant}: decode error {e}")
                print(f"   [FAIL] {variant}: cannot decode: {e}")
                continue

            # Verify SHA-256
            actual_sha = compute_sha256(file_path)
            exp_sha = expected_sha.get(variant)
            if exp_sha and actual_sha.lower() != exp_sha.lower():
                errors.append(f"{slug} {variant}: SHA256 mismatch (actual {actual_sha} != manifest {exp_sha})")
                print(f"   [FAIL] {variant}: SHA256 mismatch")
                continue

            passed_images += 1
            print(f"   [PASS] {variant}: {spec['width']}x{spec['height']}, {file_size / 1024:.1f} KiB, SHA256 verified")

    print("\n=== SUMMARY ===")
    print(f"Total WebP assets checked: {total_images}")
    print(f"Passed: {passed_images}/{total_images}")

    if errors:
        print(f"\nFAILED with {len(errors)} errors:")
        for err in errors:
            print(f"  - {err}")
        return 1

    print("\nAll 30 WebP images and 10 masters PASSED verification!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
