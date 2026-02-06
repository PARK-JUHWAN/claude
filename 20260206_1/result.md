# Image Path Migration Result

## Summary
- Total images extracted: 45 unique image paths
- Total replacements made: 69 across all HTML files
- HTML files modified: 5
- Config keys added: 45

## Per-File Statistics
- sapphire_index.html: 21 replacements
- sapphire_about.html: 10 replacements
- sapphire_joint.html: 14 replacements
- sapphire_spine.html: 12 replacements
- sapphire_sports.html: 12 replacements

## Config Keys Added

### Common (header/footer)
- `image_logo`: `sapphire_assets/sapphire_logo_1_200x60.webp`
- `image_logo_white`: `sapphire_assets/sapphire_logowhite_1_200x60.webp`
- `icon_instagram`: `sapphire_assets/sapphire_instagram_1_48x48.webp`
- `icon_youtube`: `sapphire_assets/sapphire_youtube_1_48x48.webp`

### Index - Hero
- `image_hero_1`: `sapphire_assets/sapphire_hero_1_1920x800.webp`
- `image_hero_2`: `sapphire_assets/sapphire_hero_2_1920x800.webp`
- `image_hero_3`: `sapphire_assets/sapphire_hero_3_1920x800.webp`

### Index - Intro
- `image_intro`: `sapphire_assets/sapphire_hospital_1_800x600.webp`

### Index - Departments
- `image_dept_1`: `sapphire_assets/sapphire_knee_1_400x400.webp`
- `image_dept_2`: `sapphire_assets/sapphire_shoulder_1_400x400.webp`
- `image_dept_3`: `sapphire_assets/sapphire_spine_1_400x400.webp`
- `image_dept_4`: `sapphire_assets/sapphire_foot_1_400x400.webp`

### Index - Doctors
- `image_doctor_1`: `sapphire_assets/sapphire_doctor_1_400x500.webp`
- `image_doctor_2`: `sapphire_assets/sapphire_doctor_2_400x500.webp`
- `image_doctor_3`: `sapphire_assets/sapphire_doctor_3_400x500.webp`

### Index - Facilities
- `image_facility_1`: `sapphire_assets/sapphire_surgery_1_800x600.webp`
- `image_facility_2`: `sapphire_assets/sapphire_rehab_1_800x600.webp`
- `image_facility_3`: `sapphire_assets/sapphire_imaging_1_800x600.webp`

### Index - Location Icons
- `icon_location`: `sapphire_assets/sapphire_location_1_64x64.webp`
- `icon_phone`: `sapphire_assets/sapphire_phone_1_64x64.webp`
- `icon_clock`: `sapphire_assets/sapphire_clock_1_64x64.webp`

### About
- `image_about_hero`: `sapphire_assets/sapphire_about_hero_1_1920x400.webp`
- `image_about_interior`: `sapphire_assets/sapphire_about_interior_1_800x600.webp`
- `image_about_gallery_1`: `sapphire_assets/sapphire_about_gallery_1_600x400.webp`
- `image_about_gallery_2`: `sapphire_assets/sapphire_about_gallery_2_600x400.webp`

### Joint
- `image_joint_hero`: `sapphire_assets/sapphire_joint_hero_1_1920x400.webp`
- `image_joint_intro`: `sapphire_assets/sapphire_joint_intro_1_800x600.webp`
- `image_joint_acl`: `sapphire_assets/sapphire_joint_acl_1_400x400.webp`
- `image_joint_arthritis`: `sapphire_assets/sapphire_joint_arthritis_1_400x400.webp`
- `image_shoulder_frozen`: `sapphire_assets/sapphire_shoulder_frozen_1_400x400.webp`

### Treatment (shared)
- `image_treatment_injection`: `sapphire_assets/sapphire_treatment_injection_1_600x400.webp`
- `image_treatment_rehab`: `sapphire_assets/sapphire_treatment_rehab_1_600x400.webp`
- `image_treatment_surgery`: `sapphire_assets/sapphire_treatment_surgery_1_600x400.webp`

### Spine
- `image_spine_hero`: `sapphire_assets/sapphire_spine_hero_1_1920x400.webp`
- `image_spine_intro`: `sapphire_assets/sapphire_spine_intro_1_800x600.webp`
- `image_spine_turtle`: `sapphire_assets/sapphire_spine_turtle_1_400x400.webp`
- `image_spine_stenosis`: `sapphire_assets/sapphire_spine_stenosis_1_400x400.webp`
- `image_spine_disc`: `sapphire_assets/sapphire_spine_disc_1_400x400.webp`

### Sports
- `image_sports_hero`: `sapphire_assets/sapphire_sports_hero_1_1920x400.webp`
- `image_sports_intro`: `sapphire_assets/sapphire_sports_intro_1_800x600.webp`
- `image_sports_injury`: `sapphire_assets/sapphire_sports_injury_1_400x400.webp`
- `image_sports_post_surgery`: `sapphire_assets/sapphire_sports_post_surgery_1_400x400.webp`

### Therapists
- `image_therapist_1`: `sapphire_assets/sapphire_therapist_1_300x300.webp`
- `image_therapist_2`: `sapphire_assets/sapphire_therapist_2_300x300.webp`
- `image_therapist_3`: `sapphire_assets/sapphire_therapist_3_300x300.webp`

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

## Validation
- Hardcoded sapphire_assets paths remaining: 0
- All {{image_xxx}} placeholders: 69 found
- Korean text preserved: YES
- Korean text integrity: YES
- Mojibake patterns detected: 0
- Korean character count:
  - new_sapphire_index.html: 182 characters (lower count expected - most text in {{template_variables}})
  - new_sapphire_about.html: 596 characters
  - new_sapphire_joint.html: 832 characters
  - new_sapphire_spine.html: 778 characters
  - new_sapphire_sports.html: 743 characters
- Sample Korean words verified per file:
  - index: 병원소개, 관절센터, 척추센터, 스포츠 재활센터, 진료센터, 의료진, 시설, 오시는 길
  - about: 병원소개, 의료진, 시설안내, 진료실, 물리치료실, 층별 안내
  - joint: 관절센터, 무릎 질환, 어깨 질환, 치료 방법, 주사치료, 재활치료, 수술치료
  - spine: 척추센터, 거북목, 디스크, 협착증, 목 질환, 허리 질환
  - sports: 스포츠 재활센터, 재활 프로그램, 치료사 소개, 스포츠 부상

## Output Files
- `new_sapphire_config.json`
- `new_sapphire_index.html`
- `new_sapphire_about.html`
- `new_sapphire_joint.html`
- `new_sapphire_spine.html`
- `new_sapphire_sports.html`
- `result.md`
