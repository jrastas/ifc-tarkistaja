# Regulation 1340/2025 Compliance Report

**Date:** 2026-02-25
**Regulation:** Ympäristöministeriön asetus 1340/2025
**Effective:** 1.1.2026
**Reviewed Files:** `liite1.yaml`, `liite2.yaml`
**Previous Report:** 2026-01-08 (now superseded)

---

## Executive Summary

The YAML mappings are now largely compliant with regulation 1340/2025. Significant updates made since the previous report (2026-01-08) have closed nearly all previously identified gaps.

| Category | Status |
|----------|--------|
| Liite 1 Coverage | ~98% |
| Liite 2 Coverage | ~95% |
| Required/Optional Accuracy | ~99% |

---

## Liite 1 Compliance

### Field-by-Field Matrix

| Category | Reg. Fields | Implemented | Missing | Coverage |
|----------|------------|-------------|---------|----------|
| Rakennuksen tietomalli | 1 | 1 | 0 | 100% |
| Suunnittelija | 2 | 2 | 0 | 100% |
| Rakennuspaikka | 6 | 6 | 0 | 100% |
| Rakentamistoimenpide | 4 | 4 | 0 | 100% |
| Rakennuskohde | 6–7 | 6 | 0–1 | ~95% |
| Latauspiste | 4 | 4 | 0 | 100% |
| Rakennus | 1 | 1 | 0 | 100% |
| Rakennuksen käyttötiedot | 2 | 2 | 0 | 100% |
| Käyttötarkoitus | 1 | 1 | 0 | 100% |
| Kantavan rakenteen rakennusaine | 2 | 2 | 0 | 100% |
| Lämmitysenergian lähde | 1 | 1 | 0 | 100% |
| Lämmitystapa | 1 | 1 | 0 | 100% |
| Julkisivun rakennusaine | 1 | 1 | 0 | 100% |
| Ulkokuoren tiedot | 7 | 7 | 0 | 100% |
| Sisätilojen tiedot | 3 | 3 | 0 | 100% |
| Rakennuksen osa | 11 | 11 | 0 | 100% |
| Rakennuksen osan varuste | 1 | 1 | 0 | 100% |
| Sisäverkko | 4 | 4 | 0 | 100% |
| Rakennuskohteen muutos | 7 | 7 | 0 | 100% |

### Remaining Liite 1 Gaps

#### Rakennuskohde — Possible missing field

The regulation table lists `Yrityksen nimi` under the Rakennuskohde class. This field is not present in `liite1.yaml`. Confidence is low due to PDF table extraction ambiguity — the field may refer to the company name of the project owner, complementing the existing `Omistajalaji` field.

| Field (Finnish) | Field (English) | Required | Status |
|-----------------|-----------------|----------|--------|
| Yrityksen nimi | Company Name | ? | ⚠️ Possibly missing |

#### Extra fields (not in regulation, harmless)

| Category | Field | Note |
|----------|-------|------|
| Rakennuspaikka | `katuosoite` | Not listed in regulation; complementary to `osoite` |

---

## Liite 2 Compliance

### Field-by-Field Matrix

| Category | Reg. Fields | Implemented | Missing | Coverage |
|----------|------------|-------------|---------|----------|
| Sijainti | 4 | 4 | 0 | 100% |
| Huoneisto | 12 | 12 | 0 | 100% |
| Väestönsuoja | 5 | 5 | 0 | 100% |
| Tila | 6 | 6 | 0 | 100% |
| Rakennusosat — Seinä | 8 | 8 | 0 | 100% |
| Rakennusosat — Laatta | 8 | 8 | 0 | 100% |
| Rakennusosat — Katto | 6 | 6 | 0 | 100% |
| Rakennusosat — Ovi | 7 | 7 | 0 | 100% |
| Rakennusosat — Ikkuna | 7 | 7 | 0 | 100% |
| Rakennusosat — Portaikko | 4 | 3 | 1 | 75% |
| Hissi | 10 | 10 | 0 | 100% |
| Sisäänkäynti | 9 | 9 | 0 | 100% |

### Remaining Liite 2 Gaps

#### Portaikko — Missing `Ulkovaipan osa`

The regulation defines `Ulkovaipan osa` as a generic property for all Rakennusosat. All other component types implement it, but the stair (`portaikko`) entry is missing it.

| Field (Finnish) | Field (English) | Required | Status |
|-----------------|-----------------|----------|--------|
| Ulkovaipan osa | Envelope Part | Yes | ❌ Missing from `portaikko` |

#### Extra categories (not in regulation)

| Category | IFC Entity | Note |
|----------|------------|------|
| `kerros` | `IfcBuildingStorey` | Not in Liite 2; structurally useful for IFC parsing but outside regulation scope |

---

## Required/Optional Status

All `x`-marked fields in the regulation (conditional — report if present) are correctly mapped to `required: false` in the YAML. All unmarked required fields are correctly mapped to `required: true`.

No required/optional mismatches remain.

---

## Summary of Changes Since Previous Report (2026-01-08)

The following gaps from the previous report have been resolved:

| Previously Reported Gap | Current Status |
|-------------------------|----------------|
| Rakennuskohteen muutos — entire category missing (7 fields) | ✅ All 7 fields added |
| Rakennuksen osan varuste — entire category missing | ✅ Added |
| Sisäverkko — `olemassa oleva valokuituverkko` missing | ✅ Added |
| Rakennuksen osa — `osatunnus`, `osittelun peruste`, `energiatehokkuusluokan alaindeksi` missing | ✅ All added |
| Sijainti — entire category missing (4 fields) | ✅ All 4 fields added |
| Väestönsuoja — entire category missing (5 fields) | ✅ All 5 fields added |
| Tila — entire category missing (6 fields) | ✅ All 6 fields added |
| Huoneisto — 9 of 12 fields missing | ✅ All 12 fields now present |
| Hissi — all fields incorrectly marked `required: true` | ✅ All corrected to `required: false` |
| Sisäänkäynti — 5 fields missing, 2 with wrong required status | ✅ All fields added and status corrected |

---

## Open Items

| Priority | Item | File |
|----------|------|------|
| Low | Investigate `Yrityksen nimi` under `Rakennuskohde` | `liite1.yaml` |
| Low | Add `Ulkovaipan osa` to `portaikko` | `liite2.yaml` |
| Info | `kerros` category has no direct regulation basis | `liite2.yaml` |
