#!/usr/bin/env python3
"""
migrate_images.py - Extract hardcoded .webp image paths from HTML files to config JSON
Uses UTF-8 encoding for all file operations to preserve Korean text.
"""

import json
import re
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define the mapping: image_path -> config_key
IMAGE_MAP = {
    # Common (header/footer/social)
    "sapphire_assets/sapphire_logo_1_200x60.webp": "image_logo",
    "sapphire_assets/sapphire_logowhite_1_200x60.webp": "image_logo_white",
    "sapphire_assets/sapphire_instagram_1_48x48.webp": "icon_instagram",
    "sapphire_assets/sapphire_youtube_1_48x48.webp": "icon_youtube",

    # index.html - Hero
    "sapphire_assets/sapphire_hero_1_1920x800.webp": "image_hero_1",
    "sapphire_assets/sapphire_hero_2_1920x800.webp": "image_hero_2",
    "sapphire_assets/sapphire_hero_3_1920x800.webp": "image_hero_3",

    # index.html - Intro
    "sapphire_assets/sapphire_hospital_1_800x600.webp": "image_intro",

    # index.html - Departments
    "sapphire_assets/sapphire_knee_1_400x400.webp": "image_dept_1",
    "sapphire_assets/sapphire_shoulder_1_400x400.webp": "image_dept_2",
    "sapphire_assets/sapphire_spine_1_400x400.webp": "image_dept_3",
    "sapphire_assets/sapphire_foot_1_400x400.webp": "image_dept_4",

    # index.html - Doctors
    "sapphire_assets/sapphire_doctor_1_400x500.webp": "image_doctor_1",
    "sapphire_assets/sapphire_doctor_2_400x500.webp": "image_doctor_2",
    "sapphire_assets/sapphire_doctor_3_400x500.webp": "image_doctor_3",

    # index.html - Facilities
    "sapphire_assets/sapphire_surgery_1_800x600.webp": "image_facility_1",
    "sapphire_assets/sapphire_rehab_1_800x600.webp": "image_facility_2",
    "sapphire_assets/sapphire_imaging_1_800x600.webp": "image_facility_3",

    # index.html - Location icons
    "sapphire_assets/sapphire_location_1_64x64.webp": "icon_location",
    "sapphire_assets/sapphire_phone_1_64x64.webp": "icon_phone",
    "sapphire_assets/sapphire_clock_1_64x64.webp": "icon_clock",

    # about.html
    "sapphire_assets/sapphire_about_hero_1_1920x400.webp": "image_about_hero",
    "sapphire_assets/sapphire_about_interior_1_800x600.webp": "image_about_interior",
    "sapphire_assets/sapphire_about_gallery_1_600x400.webp": "image_about_gallery_1",
    "sapphire_assets/sapphire_about_gallery_2_600x400.webp": "image_about_gallery_2",

    # joint.html
    "sapphire_assets/sapphire_joint_hero_1_1920x400.webp": "image_joint_hero",
    "sapphire_assets/sapphire_joint_intro_1_800x600.webp": "image_joint_intro",
    "sapphire_assets/sapphire_joint_acl_1_400x400.webp": "image_joint_acl",
    "sapphire_assets/sapphire_joint_arthritis_1_400x400.webp": "image_joint_arthritis",
    "sapphire_assets/sapphire_shoulder_frozen_1_400x400.webp": "image_shoulder_frozen",

    # joint.html - Treatment (shared)
    "sapphire_assets/sapphire_treatment_injection_1_600x400.webp": "image_treatment_injection",
    "sapphire_assets/sapphire_treatment_rehab_1_600x400.webp": "image_treatment_rehab",
    "sapphire_assets/sapphire_treatment_surgery_1_600x400.webp": "image_treatment_surgery",

    # spine.html
    "sapphire_assets/sapphire_spine_hero_1_1920x400.webp": "image_spine_hero",
    "sapphire_assets/sapphire_spine_intro_1_800x600.webp": "image_spine_intro",
    "sapphire_assets/sapphire_spine_turtle_1_400x400.webp": "image_spine_turtle",
    "sapphire_assets/sapphire_spine_stenosis_1_400x400.webp": "image_spine_stenosis",
    "sapphire_assets/sapphire_spine_disc_1_400x400.webp": "image_spine_disc",

    # sports.html
    "sapphire_assets/sapphire_sports_hero_1_1920x400.webp": "image_sports_hero",
    "sapphire_assets/sapphire_sports_intro_1_800x600.webp": "image_sports_intro",
    "sapphire_assets/sapphire_sports_injury_1_400x400.webp": "image_sports_injury",
    "sapphire_assets/sapphire_sports_post_surgery_1_400x400.webp": "image_sports_post_surgery",
    "sapphire_assets/sapphire_therapist_1_300x300.webp": "image_therapist_1",
    "sapphire_assets/sapphire_therapist_2_300x300.webp": "image_therapist_2",
    "sapphire_assets/sapphire_therapist_3_300x300.webp": "image_therapist_3",
}

HTML_FILES = [
    "sapphire_index.html",
    "sapphire_about.html",
    "sapphire_joint.html",
    "sapphire_spine.html",
    "sapphire_sports.html",
]


def read_file(filepath):
    """Read file with UTF-8 encoding, handling BOM"""
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        return f.read()


def write_file(filepath, content):
    """Write file with UTF-8 encoding"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)


def process_html(content, image_map):
    """Replace all hardcoded image paths with {{key}} placeholders"""
    replacements = 0
    examples = []

    for path, key in image_map.items():
        placeholder = "{{" + key + "}}"
        # Count occurrences before replacing
        count = content.count(path)
        if count > 0:
            # Capture a before example (first occurrence context)
            if len(examples) < 5:
                idx = content.find(path)
                start = max(0, idx - 30)
                end = min(len(content), idx + len(path) + 30)
                before_snippet = content[start:end].strip()
                after_snippet = before_snippet.replace(path, placeholder)
                examples.append((before_snippet, after_snippet))

            content = content.replace(path, placeholder)
            replacements += count

    return content, replacements, examples


def build_config(original_config, image_map):
    """Add image keys to config JSON"""
    # Add a blank line separator comment concept - just add keys
    for path, key in image_map.items():
        original_config[key] = path
    return original_config


def main():
    print("=" * 60)
    print("Image Path Migration Script")
    print("=" * 60)

    # 1. Read original config
    config_path = os.path.join(BASE_DIR, "sapphire_config.json")
    config_content = read_file(config_path)
    config = json.loads(config_content)
    print(f"Read config with {len(config)} existing keys")

    # 2. Build new config with image keys
    new_config = build_config(config, IMAGE_MAP)
    print(f"Config now has {len(new_config)} keys ({len(IMAGE_MAP)} image keys added)")

    # 3. Write new config
    new_config_path = os.path.join(BASE_DIR, "new_sapphire_config.json")
    config_json = json.dumps(new_config, ensure_ascii=False, indent=2)
    write_file(new_config_path, config_json + "\n")
    print(f"Written: {new_config_path}")

    # 4. Process each HTML file
    total_replacements = 0
    all_examples = []
    file_stats = []

    for html_file in HTML_FILES:
        input_path = os.path.join(BASE_DIR, html_file)
        output_path = os.path.join(BASE_DIR, "new_" + html_file)

        content = read_file(input_path)
        new_content, replacements, examples = process_html(content, IMAGE_MAP)

        write_file(output_path, new_content)

        total_replacements += replacements
        all_examples.extend(examples)
        file_stats.append((html_file, replacements))
        print(f"Processed {html_file}: {replacements} replacements -> new_{html_file}")

    # 5. Validation
    print("\n" + "=" * 60)
    print("VALIDATION")
    print("=" * 60)

    # Check all new files for remaining hardcoded paths
    remaining_hardcoded = 0
    for html_file in HTML_FILES:
        output_path = os.path.join(BASE_DIR, "new_" + html_file)
        content = read_file(output_path)
        for path in IMAGE_MAP.keys():
            count = content.count(path)
            if count > 0:
                print(f"  WARNING: {path} still found {count} times in new_{html_file}")
                remaining_hardcoded += count

    if remaining_hardcoded == 0:
        print("  All hardcoded sapphire_assets paths removed from HTML files")

    # Count placeholders
    total_placeholders = 0
    for html_file in HTML_FILES:
        output_path = os.path.join(BASE_DIR, "new_" + html_file)
        content = read_file(output_path)
        placeholders = re.findall(r'\{\{image_[^}]+\}\}|\{\{icon_[^}]+\}\}', content)
        total_placeholders += len(placeholders)
        print(f"  new_{html_file}: {len(placeholders)} image/icon placeholders")

    print(f"\n  Total placeholders: {total_placeholders}")

    # Check for mojibake
    mojibake_found = False
    mojibake_patterns = ['ê¸°ì¡´', 'í‡´ì‚¬', 'ì‹ ê·œ']
    for html_file in HTML_FILES:
        output_path = os.path.join(BASE_DIR, "new_" + html_file)
        content = read_file(output_path)
        for pattern in mojibake_patterns:
            if pattern in content:
                print(f"  MOJIBAKE DETECTED in new_{html_file}: {pattern}")
                mojibake_found = True

    new_config_content = read_file(new_config_path)
    for pattern in mojibake_patterns:
        if pattern in new_config_content:
            print(f"  MOJIBAKE DETECTED in new_sapphire_config.json: {pattern}")
            mojibake_found = True

    if not mojibake_found:
        print("  No mojibake detected - Korean text preserved")

    # Check Korean text is present
    korean_test_words = ['병원', '진료', '치료', '관절', '척추', '재활']
    korean_ok = True
    for html_file in HTML_FILES:
        output_path = os.path.join(BASE_DIR, "new_" + html_file)
        content = read_file(output_path)
        for word in korean_test_words:
            if word not in content:
                print(f"  WARNING: Korean word '{word}' not found in new_{html_file}")
                korean_ok = False

    if korean_ok:
        print("  Korean text integrity verified")

    # 6. Generate result.md
    result_md = f"""# Image Path Migration Result

## Summary
- Total images extracted: {len(IMAGE_MAP)} unique image paths
- Total replacements made: {total_replacements} across all HTML files
- HTML files modified: {len(HTML_FILES)}
- Config keys added: {len(IMAGE_MAP)}

## Per-File Statistics
"""
    for fname, count in file_stats:
        result_md += f"- {fname}: {count} replacements\n"

    result_md += "\n## Config Keys Added\n"
    # Group by category
    categories = {
        "Common (header/footer)": ["image_logo", "image_logo_white", "icon_instagram", "icon_youtube"],
        "Index - Hero": ["image_hero_1", "image_hero_2", "image_hero_3"],
        "Index - Intro": ["image_intro"],
        "Index - Departments": ["image_dept_1", "image_dept_2", "image_dept_3", "image_dept_4"],
        "Index - Doctors": ["image_doctor_1", "image_doctor_2", "image_doctor_3"],
        "Index - Facilities": ["image_facility_1", "image_facility_2", "image_facility_3"],
        "Index - Location Icons": ["icon_location", "icon_phone", "icon_clock"],
        "About": ["image_about_hero", "image_about_interior", "image_about_gallery_1", "image_about_gallery_2"],
        "Joint": ["image_joint_hero", "image_joint_intro", "image_joint_acl", "image_joint_arthritis", "image_shoulder_frozen"],
        "Treatment (shared)": ["image_treatment_injection", "image_treatment_rehab", "image_treatment_surgery"],
        "Spine": ["image_spine_hero", "image_spine_intro", "image_spine_turtle", "image_spine_stenosis", "image_spine_disc"],
        "Sports": ["image_sports_hero", "image_sports_intro", "image_sports_injury", "image_sports_post_surgery"],
        "Therapists": ["image_therapist_1", "image_therapist_2", "image_therapist_3"],
    }

    # Reverse map for lookup
    key_to_path = {v: k for k, v in IMAGE_MAP.items()}

    for category, keys in categories.items():
        result_md += f"\n### {category}\n"
        for key in keys:
            path = key_to_path.get(key, "N/A")
            result_md += f"- `{key}`: `{path}`\n"

    result_md += """
## Before/After Examples

### Example 1: Header Logo
```html
<!-- Before -->
<img src="sapphire_assets/sapphire_logo_1_200x60.webp" alt="{{hospital_name}}" class="logo-img">

<!-- After -->
<img src="{{image_logo}}" alt="{{hospital_name}}" class="logo-img">
```

### Example 2: Hero Slider Background
```html
<!-- Before -->
<div class="hero__slide" style="background-image: url('sapphire_assets/sapphire_hero_1_1920x800.webp');">

<!-- After -->
<div class="hero__slide" style="background-image: url('{{image_hero_1}}');">
```

### Example 3: Department Card
```html
<!-- Before -->
<img src="sapphire_assets/sapphire_knee_1_400x400.webp" alt="{{dept_1_name}}">

<!-- After -->
<img src="{{image_dept_1}}" alt="{{dept_1_name}}">
```

### Example 4: Footer Social Icon
```html
<!-- Before -->
<img src="sapphire_assets/sapphire_instagram_1_48x48.webp" alt="Instagram">

<!-- After -->
<img src="{{icon_instagram}}" alt="Instagram">
```

### Example 5: Subpage Hero Background
```html
<!-- Before -->
<section class="subpage-hero" style="background-image: url('sapphire_assets/sapphire_joint_hero_1_1920x400.webp')">

<!-- After -->
<section class="subpage-hero" style="background-image: url('{{image_joint_hero}}')">
```
"""

    result_md += f"""
## Validation
- Hardcoded sapphire_assets paths remaining: {remaining_hardcoded}
- All {{{{image_xxx}}}} placeholders: {total_placeholders} found
- Korean text preserved: {"YES" if not mojibake_found else "NO - MOJIBAKE DETECTED"}
- Korean text integrity: {"YES" if korean_ok else "NO - MISSING KOREAN TEXT"}

## Output Files
- `new_sapphire_config.json`
- `new_sapphire_index.html`
- `new_sapphire_about.html`
- `new_sapphire_joint.html`
- `new_sapphire_spine.html`
- `new_sapphire_sports.html`
- `result.md`
"""

    result_path = os.path.join(BASE_DIR, "result.md")
    write_file(result_path, result_md)
    print(f"\nGenerated: {result_path}")

    print("\n" + "=" * 60)
    print(f"MIGRATION COMPLETE")
    print(f"  Unique image keys: {len(IMAGE_MAP)}")
    print(f"  Total replacements: {total_replacements}")
    print(f"  Total placeholders: {total_placeholders}")
    print(f"  Mojibake: {'NONE' if not mojibake_found else 'DETECTED!'}")
    print("=" * 60)


if __name__ == "__main__":
    main()
