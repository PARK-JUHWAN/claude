# Result: Deferred Image Loading (src -> data-src)

## Conversion Summary

### src -> data-src Conversions

| File | src -> data-src | style -> data-bg |
|------|:-:|:-:|
| sapphire_index.html | 1 | 0 |
| sapphire_about.html | 0 | 0 |
| sapphire_joint.html | 0 | 0 |
| sapphire_spine.html | 0 | 0 |
| sapphire_sports.html | 0 | 0 |
| **Total** | **1** | **0** |

### Detail

- **sapphire_index.html**: `<iframe src="{{map_embed}}"` converted to `<iframe src="" data-src="{{map_embed}}"`
- **sapphire_about.html ~ sapphire_sports.html**: No `src` attributes contained `{{...}}` placeholders. All `<img>` tags use hardcoded asset paths (`sapphire_assets/...`), which were left untouched as required. All `style="background-image: ..."` attributes also use hardcoded paths, not `{{...}}` placeholders.

### sapphire_main.js Changes

Updated the `replaceInNode` function (config loader, lines 1-33 region) to add deferred loading resolution:

1. After attribute replacement, if an element has `data-src` and its `src` is empty, the resolved `data-src` value is copied into `src`
2. If an element has `data-bg`, the resolved value is applied via `node.style.backgroundImage`

No changes were made to code after the config loader section (line 34+).

## Verification Results

### 1. Zero src="{{...}}" patterns remaining

All 5 HTML output files were scanned. No `src="{{...}}"` patterns remain (excluding `data-src` attributes).

### 2. All {{placeholder}} strings preserved

| File | Original Placeholders | New Placeholders | Missing |
|------|:-:|:-:|:-:|
| sapphire_index.html | 55 | 55 | 0 |
| sapphire_about.html | 17 | 17 | 0 |
| sapphire_joint.html | 12 | 12 | 0 |
| sapphire_spine.html | 12 | 12 | 0 |
| sapphire_sports.html | 12 | 12 | 0 |

### 3. Zero hardcoded image paths introduced

No hardcoded paths were substituted for `{{...}}` placeholders. The only conversion (`{{map_embed}}`) is preserved in the `data-src` attribute.

### 4. Korean text preservation

| File | Korean Words | Mojibake Patterns |
|------|:-:|:-:|
| sapphire_index.html | 60 | 0 |
| sapphire_about.html | 189 | 0 |
| sapphire_joint.html | 276 | 0 |
| sapphire_spine.html | 254 | 0 |
| sapphire_sports.html | 262 | 0 |
| sapphire_main.js | 7 | 0 |

All files read/written with `encoding='utf-8'`. No sed, PowerShell, or str_replace used. Korean text verified intact with zero mojibake patterns detected.
