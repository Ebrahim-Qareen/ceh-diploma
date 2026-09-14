# Session 7 — Student Activity & Rubric

## Activity: full triage on your own sample
Take the trojan you built in Lab A and carry it through the entire workflow, producing the incident triage report.

### Steps
1. **Static** (Lab B): hash + VirusTotal reasoning, strings, PE imports. Record IOCs.
2. **Dynamic** (Lab C): detonate in the isolated chamber; capture the C2 connection and any persistence.
3. **Map** every behaviour to a MITRE ATT&CK technique ID.
4. **Detect** (Lab D): a working YARA rule (fires on the sample, not on benign files) + a Sigma behaviour rule.
5. **Report** (Lab E): complete the triage template.

## Rubric (100 pts)
| Criterion | Pts |
|---|---|
| Static analysis correct & complete (hash, strings, imports, IOCs) | 20 |
| Dynamic analysis performed **with correct isolation** (proof VM was contained) | 20 |
| Behaviours mapped to accurate ATT&CK techniques | 15 |
| YARA rule works and is well-scoped (matches sample, not benign) | 15 |
| Sigma rule keys on a real observed behaviour + ATT&CK tag | 10 |
| Incident report: all six sections, clear verdict, actionable | 20 |

**Isolation gate:** any dynamic analysis done without demonstrated isolation scores 0 on that criterion regardless of results — the discipline is the skill.
