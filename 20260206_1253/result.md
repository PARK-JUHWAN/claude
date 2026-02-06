# Deferred Image Loading - Conversion Results

## Summary

All `src="{{placeholder}}"` attributes on `<img>` and `<iframe>` elements have been converted to `src="" data-src="{{placeholder}}"`.
All `style="background-image: url('{{placeholder}}')"` attributes have been converted to `style="" data-bg="{{placeholder}}"`.

## Conversion Counts

| File | src → data-src | style → data-bg |
|------|---------------|-----------------|
| sapphire_index.html | 19 | 3 |
| sapphire_about.html | 9 | 1 |
| sapphire_joint.html | 13 | 1 |
| sapphire_spine.html | 11 | 1 |
| sapphire_sports.html | 11 | 1 |
| **Total** | **63** | **7** |

## JavaScript Modification (sapphire_main.js)

The `replaceInNode` function in the config loader section (lines 1-33) was updated to:
1. After attribute replacement, if an element has `data-src` and empty `src`, copy the resolved `data-src` value into `src`
2. After attribute replacement, if an element has `data-bg`, set `node.style.backgroundImage` to the resolved value

Lines 34+ remain completely untouched.

## Verification Results

### Zero hardcoded paths introduced
- Confirmed: All `data-src` and `data-bg` attributes contain only `{{placeholder}}` patterns
- No hardcoded image paths (e.g., `sapphire_assets/...`) were introduced

### All placeholders preserved
- All `{{image_xxx}}`, `{{icon_xxx}}`, and `{{map_embed}}` placeholders are present in `data-src` or `data-bg` attributes
- The config.json-based customization system continues to work as before

### Zero remaining src="{{...}}" patterns
- Confirmed: No `<img>` or `<iframe>` elements have `src` attributes containing `{{...}}` placeholders
- Browser will no longer attempt to load `{{placeholder}}` as URLs (eliminating 404 errors)

### Korean text preservation
- All Korean text verified intact with no mojibake patterns detected
- UTF-8 encoding used for all file I/O operations
