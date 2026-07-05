# Data Platform Architecture

## Purpose

This document defines the technical and data architecture of Algeria Scouting Hub.

The goal is to build a source-agnostic football data platform capable of integrating multiple external providers without changing the core business model.

---

# Architecture Principle

The platform must not depend on a single data provider.

FBref, Transfermarkt, SofaScore, FotMob, Wikipedia or future APIs are only external sources.

The core system only understands standardized business entities such as:

- Player
- Club
- Competition
- Season
- Match
- Statistics
- Eligibility

---

# High-Level Architecture

```text
External Sources
      |
      v
Connectors
      |
      v
Raw Landing Layer
      |
      v
Standardization Engine
      |
      v
Operational Database
      |
      v
Data Warehouse
      |
      v
API / Dashboard / AI