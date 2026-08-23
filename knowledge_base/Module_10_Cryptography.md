---
source: Module 10 Cryptography.pdf (instructor deck, full — final section of deck)
session: 10
---

# Module 10 — Cryptography

> Maps to CEH official Chapter 20.

## Official learning objectives (CEH Ch.20)

1. Explain Cryptography Concepts
2. Explain Encryption Algorithms
3. Explain Cryptography Tools
4. Explain Public Key Infrastructure (PKI)
5. Explain Email Encryption
6. Explain Disk Encryption
7. Explain Cryptanalysis Techniques

## 1. What is Cryptography?

The process of hiding or coding information so that only the intended
recipient can read it. Primary purpose: **preserve confidentiality**.

## 2. Cryptographic Components

| Component | Description |
|---|---|
| Plaintext | Original readable data before encryption |
| Ciphertext | Scrambled/encoded data after encryption |
| Secret key | Enables transformation between plaintext and ciphertext |
| Encryption algorithm | Function that transforms plaintext → ciphertext using a key |
| Decryption algorithm | Function that transforms ciphertext → plaintext using a key |

## 3. Symmetric Encryption

Uses the **same key** for both encryption and decryption. Fast, suitable
for bulk data encryption. Key distribution is the challenge.

| Algorithm | Key/Block size | Notes |
|---|---|---|
| AES-128 | 128-bit key | Current standard — fast, secure |
| AES-256 | 256-bit key | Higher security, slightly slower |
| AES-512 | 512-bit key | Maximum AES security |
| DES | 64-bit key, 64-bit block | Legacy — broken, too short key |
| 3DES | 168-bit key | DES applied 3 times — legacy, deprecated |

## 4. Asymmetric Encryption

Uses **two different keys**: public key (encryption) and private key
(decryption). Solves key distribution problem but much slower than
symmetric.

### RSA (Rivest-Shamir-Adleman)

Most common asymmetric algorithm. Used in HTTPS/TLS for key exchange,
digital signatures, and email encryption (PGP/GPG). Works alongside
End-to-End Encryption (E2EE) technology.

**How RSA works (simplified):** generate two large primes → compute
modulus → derive public and private keys → encrypt with public key,
decrypt with private key. Security relies on difficulty of factoring
large numbers.

## 5. Hashing

One-way cryptographic function — **preserves integrity**. Cannot be
reversed ("dehashed").

### Hash Function Properties

1. Produces **fixed-length** output regardless of input size
2. Accepts **variable-length** input
3. Easy to compute H(X) = h for any X
4. Computationally **infeasible** to find X given h (pre-image resistance)
5. **Weak collision resistance** — infeasible to find Y ≠ X where H(X) = H(Y)
6. **Strong collision resistance** — infeasible to find any pair (X,Y) where H(X) = H(Y)

### Common Hash Algorithms

| Algorithm | Output size | Status |
|---|---|---|
| MD4 | 128-bit | Broken |
| MD5 | 128-bit | Broken — collisions demonstrated |
| SHA-1 | 160-bit | Deprecated — collisions demonstrated |
| SHA-256 | 256-bit | Current standard (SHA-2 family) |
| SHA-512 | 512-bit | Current standard (SHA-2 family) |
| NTLM | 128-bit | Windows authentication hash |
| LM (LANMAN) | 128-bit | Legacy Windows — severely weak |

## 6. Digital Signatures

Used to preserve **authenticity** and **non-repudiation**. The sender
signs a message hash with their private key; the receiver verifies with
the sender's public key. If the signature verifies, the message is
authentic and hasn't been tampered with.

## 7. Cryptanalysis

The science of breaking cryptographic codes **without the key**.

**Example technique:** letter frequency analysis — in English, 'e' is
the most common letter. By analyzing frequency distribution of ciphertext
characters, you can map them back to plaintext letters (effective against
simple substitution ciphers, not modern algorithms).

## 8. Practical Application (CEH context)

- **Symmetric + Asymmetric together (hybrid):** TLS handshake uses RSA
  to exchange a symmetric session key, then AES for bulk data encryption.
  This combines asymmetric security with symmetric speed.
- **Hashing in authentication:** passwords stored as hashes (see Module 6),
  verified by hashing input and comparing.
- **Digital signatures in certificates:** HTTPS certificates use digital
  signatures to verify server identity (PKI).
