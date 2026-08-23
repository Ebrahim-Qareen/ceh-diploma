---
session: 1
title: Foundations, Lab Build & First Contact
doc: Instructor Guide
---

# Session 1 — Instructor Guide

> **Deliver from `sessions/session-01/index.html`.** 22 pages, arrow keys to
> navigate, sidebar to jump. The page carries every diagram — you should not need
> to draw on the whiteboard, though you may want to for the 5-phase loop.

## Pre-class checklist

- [ ] **Replace the instructor-intro box on page 2** with your own background. It ships as a
      placeholder and will be visible on the projector if you forget.
- [ ] Drop the 8 screenshots into `sessions/session-01/assets/img/`. Missing files render as a
      labelled placeholder rather than a broken image, so the page is safe if any are absent —
      but the virtualization and lab pages are noticeably weaker without them.
- [ ] Your own KALI-ATK01 and METASPLOITABLE2 up on VMnet1, able to ping each other.
- [ ] Baseline snapshots exist on both (you demo the revert live on page 17).
- [ ] Metasploitable2 IP noted — you need it during the page-19 demo.
- [ ] Confirm `nmap` and `nc` are present on your Kali.
- [ ] Projector: terminal font 24pt+. Open the session page in a second window.
- [ ] `labs/setup_guide.md` link ready to send students for tonight's build.
- [ ] Pair list prepared, or a plan to draw it live on page 2.

## What changed from the original plan

The VM build is **homework now, not class work**. Class covers virtualization and lab design as
theory (pages 15–17) so students build with understanding, and the reclaimed hour goes to the
prior-knowledge recall block and a longer first-contact lab. Students who arrive with VMs already
built do the page-19 lab live; students who don't watch, then repeat it at home. Nobody is exempt
from personally running the commands — they are time-shifted, not excused.

## Teaching flow

### Page 2 — Who's in the room (15 min)

The most important 15 minutes of the session, and the easiest to rush. Three student questions:
name and current role, which prior course felt strongest, and why CEH.

**What to actually do with the answers:** write down who claims networking vs Linux vs Windows.
You will use this in the recall block — direct a recall question at someone whose strength it is
*not*, then let their partner rescue them. That establishes the pair as a unit on day one and
tells you where the room is genuinely weak.

Be explicit that the pair is a peer-check unit, never shared execution. Students who have done
group projects will otherwise default to splitting work.

### Page 3 — The breach story (7 min)

Read the table row by row. The point is the third column: four of the five steps were sitting in a
log nobody read. Let the pair discussion run its full two minutes — the "technology or people?"
question has no clean answer, which is what makes it useful.

### Pages 4–7 — Recall block (30 min) · the ask-first mechanic

**This is the block most likely to be delivered wrong.** It is not a lecture and not revision. The
pattern for every one of these is:

1. Ask the room the question on the page. **Wait.** Do not fill the silence.
2. Let two or three people answer, including a wrong answer if you get one.
3. *Then* reveal the diagram, which frames the same knowledge as attack surface.

**Common misconceptions to expect**
- *"We already did OSI."* Yes — but not as a target list. If someone says this, ask them which
  layer ARP poisoning lives at and why that matters. Point made.
- *TCP handshake:* many will recite SYN/SYN-ACK/ACK correctly but not see why skipping the third
  packet matters. That connection is the whole point of the page — do not move on until it lands.
- *authN vs authZ:* almost everyone can define them and almost nobody applies them. The IDOR
  question separates the two groups.

**Page 7 (course map)** is a 5-minute page — do not over-explain it. Tell students to note their
two shakiest rows and move on.

### Pages 8–11 — Theory core (42 min)

- **Page 8 (attack formula):** the ask-first question about the unpatched server is the hook.
  The defender's-leverage box is the business case for a SOC — say it out loud, it lands with
  students aiming at SOC roles.
- **Page 9 (hats):** anchor everything on the authorization axis. Push back hard on
  "grey hat is fine" — this is a genuine misconception and it has ended careers.
- **Page 10 (5 phases):** the 80/5/15 time split surprises most rooms. Draw the loop on the
  whiteboard as well as showing it, if you have one. The defensive consequence — detection that
  only watches exploitation is watching the wrong 5% — is the takeaway.
- **Page 11 (frameworks):** 12 minutes for three frameworks is tight and deliberately so. Kill
  Chain: the defender's advantage. ATT&CK: the hierarchy, and note the three sub-technique files
  are the same ones from the Windows recall 40 minutes earlier. Diamond: pivoting only.

### Page 12 — Activity: map the breach (13 min)

Walk the room. The goal is fluency with the vocabulary, not correctness. Debrief 2–3 pairs and
spend your debrief time on the **last row** — three tactics, not one. Noticing that real intrusions
don't map cleanly is the actual skill being taught.

### Page 13 — Authorization + RoE activity (20 min)

Theory ~10, writing ~10. Collect or peer-check the RoE documents; this is the students' first
evidence artefact. The commonest gap in first drafts is a missing prohibited-actions section —
students write what they *may* do and stop.

### Pages 15–17 — Virtualization and the lab (37 min)

Sourced from the instructor's own *Virtual Machines* deck plus `labs/lab_design.md`.

- **Page 15:** the partitioning question is the whole hook — if they accept a disk can be split,
  they accept a machine can be. Emphasise the **VT-x check as tonight's first task**; a locked
  BIOS is the single most common build blocker and you want to know tomorrow, not before Session 3.
  Mention the Hyper-V / WSL2 / Docker conflict explicitly — it catches at least one student per cohort.
- **Page 16:** the three network modes. Spend your time on host-only being a *safety control*, not
  a preference. State plainly that a vulnerable VM briefly exposed on a real network must be
  assumed compromised and rebuilt.
- **Page 17:** **demo the revert live.** Boot Kali, `touch /tmp/snapshot-test`, revert, show the
  file is gone. Thirty seconds, and it converts snapshot discipline from advice into something
  they have seen work.

### Page 18 — Passive vs active (7 min)

Short. The crossing from "target cannot know" to "target definitely knows" is what makes the next
page meaningful. The `crt.sh` question is the reveal.

### Page 19 — First contact (30 min)

**Make the scope check verbal.** Have the room say the target range out loud before anyone types.

Demo script, then students repeat on their own Kali:

**1. Confirm the interface**
```
ip a
```
*Expected:* an interface (usually `eth0`) with a `192.168.56.x` address.
*If it shows `10.x` or `172.x`:* adapter is on NAT — this is the most common failure here.

**2. Host discovery**
```
sudo nmap -sn 192.168.56.0/24
```
*Expected:* Metasploitable2 as "Host is up", with a VMware OUI MAC address.

**3. Confirm reachability**
```
ping -c 3 <MSF2_IP>
```
*Expected:* 3 replies, TTL ~64. Point out the TTL as free OS fingerprinting.

**4. Service and version sweep**
```
nmap -sV --top-ports 20 <MSF2_IP>
```
*Expected:* 21/ftp vsftpd 2.3.4, 22/ssh OpenSSH 4.7p1, 23/telnet, 25/smtp Postfix,
80/http Apache 2.2.8, 139+445/Samba.

**5. Manual banner grabbing**
```
nc -nv <MSF2_IP> 21
nc -nv <MSF2_IP> 22
nc -nv <MSF2_IP> 25
```
*Expected:* `220 (vsFTPd 2.3.4)`, `SSH-2.0-OpenSSH_4.7p1 Debian-8ubuntu1`,
`220 metasploitable.localdomain ESMTP Postfix (Ubuntu)`.
Insist on **pasting, not retyping** — the exact version string is the entire value.

**6. The SOC flip (60 seconds, no tools)**
"Everything you just ran is in that target's logs. One source IP touching many ports in a short
window — that's the textbook port-scan detection, and you just generated a perfect example.
In Session 3 you learn to do it quietly; as an analyst you learn to catch it."

**Call out `vsftpd 2.3.4` specifically.** That version shipped with a backdoor. Today's banner is
Session 4's CVE lookup and Session 5's shell — say so, it makes the whole course feel connected.

### Pages 20–22 — Wrap (26 min)

Lab report format, then the quiz (self-scoring, students click answers on their own screens or you
run it on the projector), then the homework brief. **Stress homework task 1 — the VT-x check —
happens tonight, not at the weekend.**

## Bridge to next session

Session 2 crosses back over the line into passive: OSINT, Google dorks, Shodan, WHOIS, certificate
transparency, theHarvester and DNS recon — building a complete target picture that never learns you
were looking. Everything phase 1 of the methodology promised.
