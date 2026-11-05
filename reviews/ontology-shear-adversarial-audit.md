# Independent adversarial audit of Gemini's Ontology Shear report

**Status:** audit of the preserved artifact [gemini-ontology-shear-original.md](gemini-ontology-shear-original.md). Not a consensus. Prior experiments remain untouched.

## What the report claims

A detector can distinguish genuine "ontology shear" (descriptive categories become inadequate for compression and intervention) from ordinary schema mismatch or coordinate change, using an MDL + intervention-efficacy criterion on a multi-paradigm evaluator.

## Independently verified points

- The three states produce identical outputs on the two reported inputs (3 → 6, 7 → 17).
- The supplied detector returns False when asked to apply a "weights" intervention to the lookup state, because the state lacks a `weights` attribute.
- Observer C (I/O only) sees no difference on the tested points.

## Defects and unsupported conclusions

1. **Structural attribute check is not ontology detection.**  
   The decisive test is `hasattr(state, "weights")`. Failure is manufactured by the detector's own interface assumption. No attempt is made to translate the intended intervention into the target representation. An ordinary missing-method or type-error is reported as shear.

2. **Behavioral equivalence is tested too narrowly.**  
   Only inputs 3 and 7 are shown. The lookup covers 0–9. Independent checks (see new experiment) confirm divergence outside that range (e.g., input 10 or negative values). The report's table of extended inputs was not produced by the supplied code.

3. **MDL comparison is absent.**  
   `get_schema_mdl` returns `len(str(...))` or `len(json.dumps(...))`. These are string-length proxies, not Minimum Description Length. No comparison of competing descriptive frameworks is performed.

4. **"Connectionist" label is unsupported.**  
   State 1 is thresholded arithmetic with two coefficients. It has no matrix multiplication, no learned weights, and no neural-network dynamics. Attributing connectionist properties is inaccurate.

5. **Several adversarial cases are described but not executed.**  
   Semantic hollow-out, obfuscated representations, underdetermination, and recovery appear only as narrative. The executable toy does not implement them.

6. **Mathematical claims are over-extended.**  
   Loss of predictive adequacy on a toy is not equivalent to failure of a Galois connection. A universal interpreter's ability to simulate the system does not establish that the old descriptive framework was resource-efficiently adequate, nor that a new ontology has arisen.

7. **Additional issues.**  
   - Lambda rules in State 0 cannot be patched by the detector (explicitly proxied as failure).  
   - No resource accounting beyond the implicit cost of the attribute check.  
   - The UTM competitor is correctly noted as always available; the report then treats resource-bounded epistemology as sufficient to reify "ontology shear" without showing a case that resists ordinary causal-dependency tracking.

## Challenge to Sol's prior assessment

Sol correctly identified the attribute-check circularity and the missing MDL. The further claim that the lookup and arithmetic implementations are "textbook differing computational ontologies" is also unsupported; they are different Python objects implementing the same extensional function on a finite domain. The distinction that survives is causal role of a stored artifact, not ontology.

## What remains interesting

The hollow-out scenario (artifacts preserved, execution redirected) is a real software phenomenon. It is better studied as causal-role preservation versus artifact preservation than as ontology shear. That is the subject of the follow-up experiment.
