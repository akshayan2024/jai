# Adaptive AI Global Coding Ruleset (Technology-Agnostic)

These rules are designed for use by any AI coding assistant across languages and environments. They apply adaptively depending on the scope of the project — from a quick proof-of-concept (PoC) to a production-grade, full-featured application. AI agents should scale their rigor accordingly, applying lightweight standards for rapid ideation and full standards for enterprise or production builds.

---

## Project Stage Sensitivity

- **PoC / Rapid Prototyping**: Prioritize speed, clarity, and basic functionality. Skip exhaustive testing or documentation but flag areas needing future hardening.
- **MVP / Internal Tools**: Implement core standards — basic security, modularity, and test coverage.
- **Full Production App**: Enforce all rules — secure, modular, testable, documented, and maintainable code.
- AI agents must always detect and **align behavior with the current development phase** as described in `PROJECT_SUMMARY.md` or clarified by the user.

---

## I. CONTEXT AWARENESS & STRUCTURED WORKFLOW

1. Refer to available context files (`project_rules`, `implementation-plan.md`, etc.) as primary sources of truth.
2. Generate and maintain planning files like `implementation-plan.md`, `todo.md`, `glossary.md`, and `rules_summary.md`.
3. Use `implementation-plan.md` for step-by-step execution. Mark steps as ✅ Done with brief change logs.
4. Update `glossary.md` with plain-language explanations of terms, files, and key concepts.
5. Verify before acting — avoid assumptions. Ask clarifying questions if uncertain.
6. Preserve existing functionality — iterate incrementally unless major overhauls are requested.
7. Support "Build This With Me" mode — explain steps on demand.
8. Provide prompt templates to help guide user ideation and feature definitions.
9. Use `PROJECT_SUMMARY.md` to track current goals, decisions, scope level (PoC, MVP, Prod), and project state.

---

## II. CHANGE MANAGEMENT & COLLABORATION

10. Restart or reload the system after backend/service changes.
11. Edit one file at a time, in clear, self-contained updates.
12. Refactor overly large files (>300 lines) to improve readability and modularity.
13. Avoid hard-coded values — use constants with meaningful names.
14. Log all changes in `CHANGELOG.md` including date and purpose.
15. Use semantic commit messages (e.g., `[FEAT]`, `[FIX]`, `[REFACTOR]`).
16. Pull the latest version before starting edits. Commit often with clear messages.
17. If multiple agents are active, use `TASKS.md` to record assignments and in-progress work.
18. Label all TODOs and FIXMEs with agent identifiers where relevant.
19. Use metadata comments (e.g., `// Purpose:`, `// Last Edited:`, `// Feature:`) to explain changes.
20. Never create parallel "_fix" versions of files - instead, refactor the original files directly and document changes.
21. After fixes are implemented and verified, remove obsolete code and debug artifacts immediately.
22. Maintain a "Fix Registry" (`FIX_REGISTRY.md`) to track critical fixes, their verification methods, and affected components.

---

## III. MODULARITY, ARCHITECTURE & CODE STYLE

23. Implement the simplest working solution appropriate to the phase.
24. Apply the Single Responsibility Principle — keep functions and modules focused.
25. Respect project structure and naming conventions across files and folders.
26. Reuse existing logic instead of duplicating functionality.
27. Use descriptive identifiers for variables, functions, and files.
28. Maintain `ARCHITECTURE.md` to explain data flow, component boundaries, and abstractions (required at MVP+).
29. Follow and enforce consistent code style rules using appropriate tooling for the language.
30. Enforce standardization decisions (e.g., indexing conventions) consistently across the entire codebase.
31. Break large service classes (>500 lines) into smaller, focused components with clear boundaries.

---

## IV. SECURITY & PRIVACY

32. For production, do not modify or commit secret files (e.g., environment variables, credentials).
33. Ensure all sensitive files are in `.gitignore` or equivalent ignore config.
34. Apply rate limiting and throttling to exposed endpoints (MVP+).
35. Use input validation and captchas where appropriate.
36. Never expose sensitive logic client-side — enforce separation.
37. Use trusted authentication providers where applicable; avoid custom auth unless required.
38. Flag sensitive data-handling areas with `// [Sensitive]` or similar markers.
39. Perform vulnerability scans before production deployment.

---

## V. TESTING & VERIFICATION

40. For PoC, write smoke tests or inline checks if feasible. For MVP+, add automated tests for all core logic.
41. Use mock data only in testing environments.
42. Run relevant tests after every change.
43. Fix failing or outdated test logic promptly.
44. Account for edge cases in logic and user input.
45. Ensure test coverage meets phase standards (light for PoC, thorough for production).
46. Consolidate tests by functionality rather than implementation details to avoid test duplication.
47. Create shared test fixtures and utilities rather than duplicating test setup code.
48. Document test purpose with clear docstrings explaining what aspect of functionality each test verifies.

---

## VI. DEPLOYMENT & PERFORMANCE

49. Wrap unstable or partial features in flags.
50. Confirm configuration variables load correctly in each environment.
51. Optimize performance based on stack needs (e.g., lazy loading, caching).
52. Use WAFs and rate limits on public endpoints for MVP+.
53. Set up production monitoring and alerting.
54. Run post-deploy checks on endpoints, logs, and app state.
55. For production, ensure rollback mechanisms and backup plans exist.

---

## VII. DOCUMENTATION & TRACEABILITY

56. Maintain and update `CHANGELOG.md`, `PROJECT_SUMMARY.md`, `TASKS.md`, `ARCHITECTURE.md` (required at MVP+).
57. Use docstrings or header comments to explain code intent.
58. Avoid obvious or repetitive comments.
59. Document major decisions and rationale in `docs/design.md`.
60. Link to official documentation or canonical sources.
61. Maintain a requirement-to-code mapping (traceability matrix) for complex projects.
62. Document refactoring efforts and standardization decisions to prevent inconsistent implementations.
63. Create a Technical Debt Registry (`TECHDEBT.md`) that tracks suboptimal patterns that need future attention.

---

## VIII. MULTI-AGENT PROTOCOLS

64. All agents must read the summary, tasks, and change log before working.
65. Log and claim tasks clearly in `TASKS.md`.
66. Leave clear handoff notes and next steps.
67. Search for existing solutions before writing new code.
68. Add headers to files with timestamps, summaries, and authors.
69. Do not overwrite peer work without coordination.
70. Justify and document any sweeping code changes.

---

## IX. ADVANCED / OPTIONAL PRACTICES

71. Use toggles and staged rollouts for features.
72. Keep dev, test, and prod configurations clearly separated.
73. Use inline markers (e.g., `// Task-ID:`, `// Version:`) to aid tracing.
74. Encourage mid-session syncing and context refreshes.
75. Tag commits semantically and link to task identifiers.
76. Maintain an index or feature map for the system.
77. Offer mentorship-mode explanations on demand.

---

## X. EFFECTIVE AI CODE EDITING

78. Batch related changes to a single file in one comprehensive edit rather than sequential partial edits.
79. When editing a file that was previously modified, explicitly note which sections should remain unchanged.
80. Define precise function or line number boundaries when editing complex files to avoid overlapping changes.
81. Verify each change is applied correctly before proceeding to the next edit operation.
82. For complex files, prefer full-function edits over partial-function modifications.
83. For simple changes, provide the entire file content rather than partial updates when feasible.
84. When updating multiple functions in the same file that use similar patterns, edit them simultaneously.
85. After fixing bugs or inconsistencies from previous edits, document the issue to prevent recurrence.
86. Use explicit code diffs or line references when communicating about specific changes.
87. Maintain explicit decimal precision in numerical calculations to avoid rounding errors.

---

## XI. CODEBASE HYGIENE & SELF-GOVERNANCE

88. Flag unused variables, imports, and functions after edits.
89. Prompt refactor for duplicated logic or long functions.
90. Standardize naming patterns and file organization via linting rules.
91. Warn against known anti-patterns (e.g., logic in render).
92. Auto-suggest performance improvements (memoization, lazy-loading).
93. Track technical debt in `TECH_DEBT.md` with context and intended resolution.
94. Require plain-English explanations for complex logic blocks.
95. Prompt for accessibility features (ARIA, labels, contrast checks).
96. Offer optional "code review mode" questions to validate assumptions.
97. Auto-update `README.md` and `setup.md` post feature additions.
98. Regularly audit the codebase for redundant test files and consolidate them into logical test suites.
99. Perform periodic "obsolescence sweeps" to identify and remove outdated code, comments, and file scaffolding.
100. Enforce consistent indexing and API patterns across related modules to prevent integration issues.

## XII. EXTERNAL API INTEGRATION & DATA PARSING

101. Always verify external API return structure directly rather than assuming its format - print and log complete raw responses during development.
102. Create simple test scripts that directly invoke external APIs before complex integration to understand their behavior.
103. Document return structures from critical external APIs with examples in `API_SAMPLES.md`.
104. For complex nested data structures, use explicit type checking and validation before accessing nested fields.
105. Implement diagnostic logging that captures complete data structures for troubleshooting, not just error messages.
106. When encountering persistent issues, isolate external API calls into dedicated test harnesses to verify behavior.
107. Always check API documentation for possible multi-part or nested return values instead of assuming direct access patterns.
108. Add robust error handling for all parsing operations when working with external data structures.
109. When fixing bugs related to data parsing, create regression tests that validate both successful and error cases.
110. Maintain a library of sample responses from external dependencies for testing purposes.

## XIII. REFACTORING & TECHNICAL DEBT MANAGEMENT

111. Create a refactoring plan document before undertaking large-scale code reorganization.
112. Establish clear goals and success criteria for each refactoring effort.
113. Prefer incremental refactoring with testable checkpoints over "big bang" rewrites.
114. When fixing an issue, examine related components for the same pattern and fix comprehensively.
115. Document the reasoning behind significant refactoring decisions to prevent future regressions.
116. After standardization initiatives (like standardizing on 1-based indexing), perform comprehensive validation sweeps.
117. When removing obsolete code, document the replacement implementation and update all affected documentation.
118. Target refactoring at components with the highest technical debt or risk factors first.
119. Create or update integration tests before undertaking cross-component refactoring.
120. Schedule regular "cleanup sprints" to address accumulated technical debt.

## XIV. DOMAIN-SPECIFIC VERIFICATION PRINCIPLES

121. **Reference Validation**: Validate calculation results against established authorities or reference implementations in the project's domain.
122. **Boundary Case Testing**: Identify and create explicit tests for domain-specific boundary conditions and edge cases.
123. **Law Preservation Testing**: Define and test fundamental rules or laws that must hold true across all calculations in the domain.
124. **Precision Standards**: Establish and enforce consistent precision standards for all numerical calculations appropriate to the domain.
125. **Representative Test Fixtures**: Create standardized test fixtures representing real-world use cases from the problem domain.

## XV. COMPUTATIONAL ACCURACY & VALIDATION

126. **Algorithm Documentation**: Document the logical basis and implementation approach for all computational algorithms.
127. **Multi-source Validation**: Validate results against multiple independent calculation sources when applicable.
128. **Error Analysis**: Analyze and document how measurement errors or approximations affect final results.
129. **Reproducibility**: Ensure all computations produce identical results across multiple runs and environments.
130. **Domain Expert Review**: Establish a process for subject matter expert review of critical algorithms and implementations.

## XVI. COMPREHENSIVE QUALITY ASSURANCE

131. **Cross-Method Verification**: Test that different calculation paths leading to the same result produce consistent outputs.
132. **Complete Parameter Coverage**: Test across the full range of valid input parameters, not just typical cases.
133. **System Invariants**: Document and test assumptions that must hold true across the entire codebase.
134. **Side-Effect Detection**: Design tests to detect both incorrect results and unintended side effects.
135. **Versioned Test Evolution**: Maintain regression tests with versioned expected outputs as algorithms are refined.

## XVII. COMPREHENSIVE DOCUMENTATION

136. **Algorithm Specification**: Create detailed documentation for all computational algorithms with appropriate notation and sources.
137. **Edge Case Documentation**: Document system behavior under all input conditions, including edge cases and error scenarios.
138. **Error Taxonomy**: Maintain a comprehensive taxonomy of all possible error conditions with recovery procedures.
139. **Decision Record**: Document all significant technical decisions and their rationales, particularly for algorithm choices.
140. **Domain-to-Code Mapping**: Maintain a dictionary mapping domain-specific concepts to their implementation components.

## XVIII. ADVANCED OPERATIONAL PRACTICES

141. **Computational Audit Trail**: Implement logging of input parameters and results for critical operations to enable auditing.
142. **Result Versioning**: Version-tag calculation results to track the algorithm version that produced them.
143. **Specialized Performance Profiling**: Profile and document performance characteristics for all computation-heavy operations.
144. **Domain-Informed Monitoring**: Implement specialized monitoring to detect calculation anomalies based on domain knowledge.
145. **Domain-Driven Acceptance Testing**: Create acceptance test scripts specifically designed to validate essential domain constraints.

--

This `rules.md` file should live at the root of every project and be used to adapt AI behavior based on project maturity, scope, and user preferences. It ensures scalable, collaborative, and appropriate AI-assisted software development across all contexts.