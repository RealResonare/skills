---
name: mechDesign
description: 机械设计 playbook：需求澄清、方案选型（传动/机构/结构件）、强度/刚度/疲劳/振动校核、DFMA、标准件选型、公差与工程图。用于"设计/计算/校核某个机械结构"类任务。
---

# mechDesign — 机械设计 playbook

> **English Quick Start**
>
> This skill drives mechanical product design from requirements to manufacturable drawings: requirement clarification, solution selection (transmission/mechanism/structure), strength/stiffness/fatigue/vibration check, DFMA (design for manufacturing & assembly), standard-part selection, tolerancing and engineering drawings. It follows GB/ISO standards and delivers calculations with safety factors, not guesses.
> Core loop: **需求澄清 → 方案设计与选型 → 详细设计 → 计算校核（强度/刚度/疲劳/振动） → DFMA 评审 → 工程图与 BOM → 交付**.
> Hard rules: every critical dimension must have a calculation basis; vibration & fatigue are first-class citizens; prefer standard parts over custom; state UNVERIFIED for anything not calculated or verified.

## Purpose

This skill guarantees that mechanical designs produced with the AI's help are **calculated, drawable, manufacturable, assemblable, and durable**: every key dimension backed by a calculation, vibration/fatigue checked (not just static strength), DFMA applied, standard parts preferred, and deliverables (drawings/BOM/calculation report) complete. It covers GB/ISO standard systems.

## When to Invoke

Invoke whenever the user wants to:

- Design a mechanical product / mechanism / structure (transmission, linkage, frame, enclosure, etc.).
- Select standard parts (gears, belts, chains, bearings, reducers, couplings, linear guides, bolts).
- Verify strength / stiffness / fatigue / vibration of a loaded component.
- Review a design for manufacturability & assemblability (DFMA).
- Generate engineering drawings, BOM, or calculation reports.

Do **not** invoke for circuit/PCB work (see `electricDesign` / `pcbDesign`), firmware (see `embeddedDev`), or 3D-printing-specific modeling (see `3dprint`).

## Unified Pipeline (Mandatory Order)

| # | Step | Gate / Rule |
|---|---|---|
| 1 | **Collect requirements** | Always establish: function, load spectrum (forces/torques/speed/duty cycle), working environment (temperature/media/cleanliness), space constraints, batch & cost targets, acceptance standard (GB/ISO/customer spec). State assumptions. |
| 2 | **Solution selection** | Give **2–3 alternative schemes** (e.g., gear vs timing belt vs planetary reducer), compared by efficiency/precision/noise/cost/life. Use the references for selection formulas. Prefer standard parts. |
| 3 | **Detailed design** | Dimension parts per selection; build parameter model or drawing. Compute transmission chain efficiency (multiply stage efficiencies: motor→coupling→gearbox→belt→screw, ~0.95–0.98 each) to size the motor. |
| 4 | **Calculation check** | **Four checks, all mandatory**: strength (σ ≤ [σ] with safety factor), stiffness (deflection/twist limits), fatigue (Goodman/Soderberg with stress concentration Kt; rainflow + Miner for irregular loads), **vibration (first natural frequency must avoid working speed ±20%)**. See `references/calculations.md`. |
| 5 | **DFMA review** | Minimize part count, symmetrical design, anti-error (poka-yoke), avoid over-constraint, check manufacturability & assemblability. See `references/dfma-checklist.md`. |
| 6 | **Standard parts & tolerances** | Select standard parts with formulas (see `references/standard-parts.md`); assign tolerances per GB/T 1800/1804 (see `references/tolerances-drawings.md`). |
| 7 | **Drawings & BOM** | Engineering drawing per GB/T 17450/4459/131; BOM with standard-part specs. See `references/tolerances-drawings.md`. |
| 8 | **Deliver** | Calculation report (with formulas & numbers), scheme comparison, drawings/BOM, assumptions, UNVERIFIED list, next steps. |

## Core Rules (Non-Negotiable)

1. **Every key dimension has a calculation basis.** No "I think 8mm is enough" — compute or state the assumption.
2. **Static strength is only the floor.** Loaded parts must also be checked for fatigue (Goodman/Soderberg, Kt from charts/simulation, not guessed) and, for rotating parts, vibration (avoid working speed ±20%).
3. **Stiffness often limits before strength.** Precision shafts, lead screws, cantilevers: size by deflection/twist first.
4. **Vibration is a first-class citizen.** Rotating machinery must have first natural frequency computed; thin/large-span structures need modal thinking.
5. **Prefer standard parts** (bearings, reducers, couplings, rails, fasteners) over custom machining — cheaper, reliable, replaceable.
6. **Safety factors** per application: 1.5 light duty / 2.0 general / 3.0+ shock; reducer peak/rated torque ≥ 1.5; inertia ratio load/motor ≤ 5.
7. **Thermal & tribology matter.** ΔT 1°C on steel ≈ 11µm/m; sliding pairs respect PV limits (Cu alloy PV ≤ 1.5 MPa·m/s, self-lubricating polymer PV ≤ 0.3).
8. **Never invent material properties or standard values.** Use the reference tables (verified typical values) or the actual standard; mark UNVERIFIED otherwise.

## References

| File | Content |
|---|---|
| `references/materials.md` | Material selection: steel/aluminum/stainless matrix, heat treatment, casting/welding notes, typical properties |
| `references/transmissions.md` | Transmission selection: gear/belt/chain/screw/linkage, efficiency, selection formulas, reducer sizing |
| `references/calculations.md` | Strength/stiffness/fatigue/vibration: formulas, safety factors, stress concentration, shaft/beam/bearing calc |
| `references/dfma-checklist.md` | DFMA review: part count, symmetry, poka-yoke, manufacturability, assemblability, standard parts |
| `references/tolerances-drawings.md` | GB/T 1800/1804 tolerances, GD&T, surface roughness, drawing standards, BOM |

## Output Contract

Every deliverable must include:

1. **Calculation report**: input load, formulas used, key values, safety factors, results (PASS/FAIL per check).
2. **Scheme comparison table**: alternatives vs efficiency/precision/noise/cost/life + recommendation.
3. **Standard parts list** with selection basis (load → part → model).
4. **Drawings/BOM** when requested (per GB drawing standards).
5. **Assumptions & UNVERIFIED list**: anything assumed (material, load spectrum, standards) clearly marked.
