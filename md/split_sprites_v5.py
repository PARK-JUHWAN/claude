#!/usr/bin/env python3
"""
스프라이트 분할 스크립트 v5.1
=============================

GitHub 구조:
    claude/
    ├── ingredient/batch1/  (prompt.txt, origin.png, renew.png)
    ├── assets/             (결과물: PNG + sprite_index.json)
    └── md/                 (이 스크립트)

사용법:
    python md/split_sprites_v5.py \
        --prompt ingredient/batch1/prompt.txt \
        --origin ingredient/batch1/origin.png \
        --renew ingredient/batch1/renew.png \
        --output assets/

    # GitHub 자동 push
    python md/split_sprites_v5.py \
        --prompt ingredient/batch1/prompt.txt \
        --origin ingredient/batch1/origin.png \
        --renew ingredient/batch1/renew.png \
        --output assets/ \
        --push

출력:
    - 개별 PNG 파일들 ({name}_{number}_{width}x{height}.png)
    - sprite_index.json (누적)
"""

import argparse
import cv2
import numpy as np
from PIL import Image
import os
import json
import re
import subprocess
from datetime import datetime

# OCR 라이브러리
try:
    import easyocr
    OCR_ENGINE = "easyocr"
except ImportError:
    try:
        import pytesseract
        OCR_ENGINE = "pytesseract"
    except ImportError:
        OCR_ENGINE = None


def parse_prompt(prompt_path):
    """prompt 파일에서 아이템 이름 목록 추출"""
    
    with open(prompt_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    item_names = []
    lines = content.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # 패턴 1: "1. Hospital bed" 또는 "1) Hospital bed"
        match = re.match(r'^\d+[\.\)]\s*(.+)$', line)
        if match:
            name = match.group(1).strip()
            name = re.sub(r'\s*\([^)]*\)\s*$', '', name)
            item_names.append(name)
            continue
        
        # 패턴 2: "- Hospital bed" 또는 "* Hospital bed"
        match = re.match(r'^[-\*]\s*(.+)$', line)
        if match:
            name = match.group(1).strip()
            name = re.sub(r'\s*\([^)]*\)\s*$', '', name)
            item_names.append(name)
            continue
    
    return item_names


def normalize_name(name):
    """이름을 파일명 규칙에 맞게 정규화"""
    
    name = name.lower()
    name = re.sub(r'[^a-z0-9]', '', name)
    
    if name.endswith('s') and not name.endswith(('ss', 'us', 'is')):
        name = name[:-1]
    
    return name


def ocr_origin_easyocr(image_path):
    """EasyOCR로 origin 이미지에서 라벨 추출"""
    
    reader = easyocr.Reader(['en'], gpu=False, verbose=False)
    results = reader.readtext(image_path)
    
    labels = []
    for (bbox, text, conf) in results:
        if conf < 0.3:
            continue
        
        x_coords = [p[0] for p in bbox]
        y_coords = [p[1] for p in bbox]
        
        center_x = int(sum(x_coords) / 4)
        center_y = int(sum(y_coords) / 4)
        
        labels.append({
            'text': text.strip(),
            'x': center_x,
            'y': center_y,
            'confidence': conf
        })
    
    return labels


def ocr_origin_pytesseract(image_path):
    """Pytesseract로 origin 이미지에서 라벨 추출"""
    
    import pytesseract
    
    img = cv2.imread(image_path)
    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    
    labels = []
    n_boxes = len(data['text'])
    
    for i in range(n_boxes):
        text = data['text'][i].strip()
        conf = int(data['conf'][i])
        
        if not text or conf < 30:
            continue
        
        x = data['left'][i]
        y = data['top'][i]
        w = data['width'][i]
        h = data['height'][i]
        
        center_x = x + w // 2
        center_y = y + h // 2
        
        labels.append({
            'text': text,
            'x': center_x,
            'y': center_y,
            'confidence': conf / 100.0
        })
    
    return labels


def ocr_origin(image_path):
    """origin 이미지에서 OCR로 라벨 추출"""
    
    if OCR_ENGINE == "easyocr":
        return ocr_origin_easyocr(image_path)
    elif OCR_ENGINE == "pytesseract":
        return ocr_origin_pytesseract(image_path)
    else:
        print("  ⚠️ OCR 엔진 없음 (easyocr 또는 pytesseract 설치 필요)")
        return []


def merge_ocr_words(labels, distance_threshold=50):
    """인접한 OCR 단어들을 하나의 라벨로 병합"""
    
    if not labels:
        return []
    
    labels_sorted = sorted(labels, key=lambda l: (l['y'] // distance_threshold, l['x']))
    
    merged = []
    current_group = [labels_sorted[0]]
    
    for label in labels_sorted[1:]:
        last = current_group[-1]
        
        same_line = abs(label['y'] - last['y']) < distance_threshold
        close_x = label['x'] - last['x'] < distance_threshold * 2
        
        if same_line and close_x:
            current_group.append(label)
        else:
            merged_text = ' '.join([l['text'] for l in current_group])
            avg_x = sum([l['x'] for l in current_group]) // len(current_group)
            avg_y = sum([l['y'] for l in current_group]) // len(current_group)
            avg_conf = sum([l['confidence'] for l in current_group]) / len(current_group)
            
            merged.append({
                'text': merged_text,
                'x': avg_x,
                'y': avg_y,
                'confidence': avg_conf
            })
            
            current_group = [label]
    
    if current_group:
        merged_text = ' '.join([l['text'] for l in current_group])
        avg_x = sum([l['x'] for l in current_group]) // len(current_group)
        avg_y = sum([l['y'] for l in current_group]) // len(current_group)
        avg_conf = sum([l['confidence'] for l in current_group]) / len(current_group)
        
        merged.append({
            'text': merged_text,
            'x': avg_x,
            'y': avg_y,
            'confidence': avg_conf
        })
    
    return merged


def get_canvas_size(w, h):
    """비율에 따른 캔버스 크기 결정"""
    
    ratio = w / h if h > 0 else 1
    
    if ratio >= 2.5:
        return 96, 32
    elif ratio >= 1.5:
        return 64, 32
    elif ratio >= 0.67:
        return 32, 32
    elif ratio >= 0.4:
        return 32, 64
    else:
        return 32, 96


def is_valid_sprite(w, h, non_transparent_pixels):
    """글자/노이즈 필터링"""
    
    area = w * h
    
    if area < 100:
        return False
    if w < 8 or h < 8:
        return False
    
    ratio = w / h if h > 0 else 999
    if ratio > 8 or ratio < 0.125:
        return False
    
    if non_transparent_pixels < 50:
        return False
    
    return True


def split_sprites(image_path):
    """투명 배경 이미지에서 스프라이트 분할"""
    
    img = Image.open(image_path).convert('RGBA')
    img_array = np.array(img)
    
    alpha = img_array[:, :, 3]
    binary = (alpha > 10).astype(np.uint8) * 255
    
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    sprites = []
    
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        
        sprite_alpha = alpha[y:y+h, x:x+w]
        non_transparent_pixels = int(np.sum(sprite_alpha > 10))
        
        if not is_valid_sprite(w, h, non_transparent_pixels):
            continue
        
        sprite = img_array[y:y+h, x:x+w]
        canvas_w, canvas_h = get_canvas_size(w, h)
        
        center_x = x + w // 2
        center_y = y + h // 2
        
        sprites.append({
            'image': sprite,
            'x': x,
            'y': y,
            'w': w,
            'h': h,
            'center_x': center_x,
            'center_y': center_y,
            'canvas': (canvas_w, canvas_h),
            'pixels': non_transparent_pixels
        })
    
    return sprites


def match_labels_to_sprites(labels, sprites, prompt_names):
    """라벨 위치와 스프라이트 위치를 매칭"""
    
    matched_names = []
    used_labels = set()
    
    sprites_sorted = sorted(enumerate(sprites), key=lambda x: (x[1]['y'] // 50, x[1]['x']))
    
    for orig_idx, sprite in sprites_sorted:
        best_label = None
        best_distance = float('inf')
        best_label_idx = -1
        
        for i, label in enumerate(labels):
            if i in used_labels:
                continue
            
            dx = sprite['center_x'] - label['x']
            dy = sprite['center_y'] - label['y']
            distance = (dx**2 + dy**2) ** 0.5
            
            if distance < best_distance:
                best_distance = distance
                best_label = label
                best_label_idx = i
        
        if best_label and best_distance < 200:
            used_labels.add(best_label_idx)
            ocr_name = best_label['text']
            
            normalized_ocr = normalize_name(ocr_name)
            
            best_match = normalized_ocr
            for pname in prompt_names:
                normalized_prompt = normalize_name(pname)
                if normalized_ocr in normalized_prompt or normalized_prompt in normalized_ocr:
                    best_match = normalized_prompt
                    break
            
            matched_names.append((orig_idx, best_match, ocr_name))
        else:
            matched_names.append((orig_idx, None, None))
    
    unmatched_indices = [i for i, (_, name, _) in enumerate(matched_names) if name is None]
    unused_prompt_names = [normalize_name(n) for n in prompt_names]
    
    for _, name, _ in matched_names:
        if name and name in unused_prompt_names:
            unused_prompt_names.remove(name)
    
    for i, uidx in enumerate(unmatched_indices):
        if i < len(unused_prompt_names):
            orig_idx = matched_names[uidx][0]
            matched_names[uidx] = (orig_idx, unused_prompt_names[i], "(fallback)")
        else:
            orig_idx = matched_names[uidx][0]
            matched_names[uidx] = (orig_idx, f"unknown{uidx+1}", "(no match)")
    
    result = [None] * len(sprites)
    for orig_idx, name, ocr_name in matched_names:
        result[orig_idx] = (name, ocr_name)
    
    return result


def save_sprite(sprite_data, name, number, output_dir):
    """스프라이트를 캔버스 크기에 맞춰 저장"""
    
    canvas_w, canvas_h = sprite_data['canvas']
    sprite_img = Image.fromarray(sprite_data['image'])
    
    canvas = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
    
    w, h = sprite_data['w'], sprite_data['h']
    
    if w > canvas_w or h > canvas_h:
        scale = min(canvas_w / w, canvas_h / h)
        new_w = int(w * scale)
        new_h = int(h * scale)
        sprite_img = sprite_img.resize((new_w, new_h), Image.LANCZOS)
        w, h = new_w, new_h
    
    paste_x = (canvas_w - w) // 2
    paste_y = (canvas_h - h) // 2
    
    canvas.paste(sprite_img, (paste_x, paste_y))
    
    filename = f"{name}_{number}_{canvas_w}x{canvas_h}.png"
    filepath = os.path.join(output_dir, filename)
    canvas.save(filepath)
    
    return filename


def load_existing_json(output_dir):
    """assets 폴더의 기존 sprite_index.json 자동 로드"""
    
    json_path = os.path.join(output_dir, "sprite_index.json")
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def git_push(repo_root, batch_name):
    """GitHub 자동 push"""
    
    try:
        subprocess.run(["git", "add", "."], cwd=repo_root, check=True)
        subprocess.run(
            ["git", "commit", "-m", f"Add sprites from {batch_name}"],
            cwd=repo_root,
            check=True
        )
        subprocess.run(["git", "push"], cwd=repo_root, check=True)
        print(f"\n✅ GitHub push 완료!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n⚠️ Git push 실패: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='스프라이트 분할 스크립트 v5.1')
    parser.add_argument('--prompt', required=True, help='prompt.txt 경로')
    parser.add_argument('--origin', required=True, help='origin.png 경로 (OCR용)')
    parser.add_argument('--renew', required=True, help='renew.png 경로 (분할용)')
    parser.add_argument('--output', required=True, help='출력 폴더 (assets/)')
    parser.add_argument('--push', action='store_true', help='GitHub 자동 push')
    
    args = parser.parse_args()
    
    # 출력 폴더 생성
    os.makedirs(args.output, exist_ok=True)
    
    # batch 이름 추출 (ingredient/batch1/prompt.txt → batch1)
    batch_name = os.path.basename(os.path.dirname(args.prompt))
    
    # repo root 찾기 (assets/ 상위)
    repo_root = os.path.dirname(os.path.abspath(args.output))
    
    print(f"\n{'='*60}")
    print(f"스프라이트 분할 v5.1 - {batch_name}")
    print(f"{'='*60}")
    
    # 1. prompt에서 이름 추출
    print(f"\n[1/5] prompt 파싱: {args.prompt}")
    item_names = parse_prompt(args.prompt)
    print(f"  → 아이템: {len(item_names)}개")
    
    for i, name in enumerate(item_names[:5], 1):
        print(f"     {i}. {name}")
    if len(item_names) > 5:
        print(f"     ... 외 {len(item_names) - 5}개")
    
    # 2. origin에서 OCR
    print(f"\n[2/5] origin OCR: {args.origin}")
    if OCR_ENGINE:
        print(f"  → 엔진: {OCR_ENGINE}")
        raw_labels = ocr_origin(args.origin)
        labels = merge_ocr_words(raw_labels)
        print(f"  → 라벨: {len(labels)}개")
    else:
        print(f"  ⚠️ OCR 없음 - prompt 순서 사용")
        labels = []
    
    # 3. renew 이미지 분할
    print(f"\n[3/5] renew 분할: {args.renew}")
    sprites = split_sprites(args.renew)
    print(f"  → 스프라이트: {len(sprites)}개")
    
    # 4. 라벨-스프라이트 매칭
    print(f"\n[4/5] 이름 매칭")
    if labels:
        matched = match_labels_to_sprites(labels, sprites, item_names)
        print(f"  → OCR 기반 매칭")
    else:
        matched = []
        for i in range(len(sprites)):
            if i < len(item_names):
                matched.append((normalize_name(item_names[i]), item_names[i]))
            else:
                matched.append((f"unknown{i+1}", "(no prompt)"))
        print(f"  → prompt 순서 매칭")
    
    # 5. 기존 JSON 자동 로드
    existing = load_existing_json(args.output)
    if existing:
        print(f"\n  📂 기존 JSON 로드됨")
        counts = existing.get("counts", {}).copy()
        all_files = existing.get("files", []).copy()
        sources = existing.get("_meta", {}).get("sources", [])
        print(f"     기존 파일: {len(all_files)}개")
    else:
        counts = {}
        all_files = []
        sources = []
    
    # 6. 저장
    print(f"\n[5/5] PNG 저장: {args.output}")
    new_files = []
    
    sprites_with_names = list(zip(sprites, matched))
    sprites_with_names.sort(key=lambda x: (x[0]['y'] // 50, x[0]['x']))
    
    for i, (sprite, (name, ocr_name)) in enumerate(sprites_with_names):
        if not name:
            name = f"item{i+1}"
        
        count = counts.get(name, 0) + 1
        counts[name] = count
        
        filename = save_sprite(sprite, name, count, args.output)
        all_files.append(filename)
        new_files.append(filename)
        
        print(f"  {i+1:3d}. {filename}")
    
    # 소스 기록 추가
    sources.append({
        "batch": batch_name,
        "prompt": os.path.basename(args.prompt),
        "origin": os.path.basename(args.origin),
        "renew": os.path.basename(args.renew),
        "sprites": len(new_files),
        "date": datetime.now().strftime("%Y-%m-%d")
    })
    
    # JSON 저장
    index_data = {
        "_meta": {
            "sources": sources,
            "total_sprites": len(all_files),
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        "counts": dict(sorted(counts.items())),
        "files": sorted(all_files)
    }
    
    json_path = os.path.join(args.output, "sprite_index.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, indent=2, ensure_ascii=False)
    
    # 완료
    print(f"\n{'='*60}")
    print(f"✅ 완료!")
    print(f"   새로 생성: {len(new_files)}개")
    print(f"   총 파일:   {len(all_files)}개")
    print(f"   JSON:      sprite_index.json")
    print(f"{'='*60}")
    
    # GitHub push
    if args.push:
        print(f"\n📤 GitHub push...")
        git_push(repo_root, batch_name)


if __name__ == "__main__":
    main()
