# Master Data Model

# Purpose

This document defines the Master Data Management (MDM) strategy used by Algeria Scouting Hub.

Its objective is to create a Single Source of Truth for every football entity managed by the platform.

The MDM layer guarantees that every real-world object exists only once, regardless of the number of external data providers.

---

# What is Master Data?

Master Data represents business entities that remain relatively stable over time.

Examples:

- A player
- A club
- A competition
- A country

Unlike statistics or transfers, Master Data changes very slowly and serves as the foundation for the entire platform.

---

# MDM Principles

The platform follows five core principles.

## 1. Single Source of Truth

Every real-world entity exists only once.

Example:

FBref

↓

Transfermarkt

↓

Wikipedia

↓

Sofascore

↓

One Golden Player

---

## 2. Source Independence

The platform never depends on a specific provider.

External websites are only data providers.

The business model remains independent.

---

## 3. Historical Tracking

No important information is overwritten.

Historical values are always preserved.

Examples:

- market value
- transfers
- contracts
- injuries
- club history

---

## 4. Data Quality

Every imported value receives metadata.

Examples:

- source
- confidence score
- import date
- verification status

The platform can therefore explain every business decision.

---

## 5. Explainability

Every important decision must be explainable.

Example:

Player eligible for Algeria

↓

Father born in Algeria

↓

FIFA Article 7

↓

Source:

Wikipedia

↓

Confidence:

95%

---

# Golden Records

Golden Records are the official business references of the platform.

Only one Golden Record may exist for each real-world entity.

The following entities are considered Golden Records.

## Player

Represents a unique football player.

Never duplicated.

Never tied to a specific website.

---

## Club

Represents a football club.

Examples:

Manchester City

Olympique Lyonnais

MC Alger

---

## Competition

Examples:

Premier League

Ligue 1

Champions League

CAF Champions League

---

## Season

Examples:

2024/2025

2025/2026

---

## Country

Represents geopolitical countries.

Example:

France

Algeria

Morocco

Spain

---

## Nationality

Represents a citizenship.

A player may own multiple nationalities.

---

## Position

Represents football positions.

Examples:

Goalkeeper

Left Back

Central Midfielder

Right Winger

---

## Coach

Represents football coaches.

---

## Agent

Represents FIFA licensed agents.

---

## Stadium

Represents football stadiums.

---

## DataSource

Represents external providers.

Examples:

FBref

Transfermarkt

Wikipedia

Sofascore

Fotmob

FIFA

CAF

FAF

---

# Relationship Entities

Relationship entities connect Golden Records together.

## PlayerClub

Stores the complete club history of a player.

Includes:

- start date
- end date
- squad number
- contract

---

## PlayerNationality

Stores every nationality owned by a player.

Includes:

- acquisition type
- birth
- father
- mother
- naturalization

---

## PlayerPosition

Allows multiple positions.

Example:

Primary

Secondary

Occasional

---

## CompetitionSeason

Links competitions to seasons.

Example:

Premier League

↓

2025/2026

---

## ClubCompetition

Links clubs to competitions.

---

# Source Registry

Every imported entity is mapped to its original source.

Example:

Golden Player

↓

PlayerSource

↓

FBref

↓

Player ID = 34892

↓

Transfermarkt

↓

Player ID = 55521

↓

Wikipedia

↓

URL

---

# Source Mapping

The platform stores external identifiers.

Examples:

fbref_id

transfermarkt_id

sofascore_id

fotmob_id

wikipedia_url

fifa_id

This allows synchronization without duplication.

---

# Matching Engine

The Matching Engine determines whether two imported records represent the same real-world entity.

Matching criteria may include:

- full name
- birth date
- nationality
- club
- position
- external identifiers

Future versions may include AI-assisted matching.

---

# Data Quality Layer

Each imported attribute stores metadata.

Metadata includes:

- source
- confidence score
- imported_at
- verified
- verified_by

This enables complete traceability.

---

# Historical Data

The following business entities are historized.

- Club History
- Market Value
- Transfers
- Contracts
- Injuries
- Eligibility
- Statistics

Nothing is permanently overwritten.

---

# Business Ownership

Golden Records are owned by Algeria Scouting Hub.

External websites never own business entities.

They only provide information.

---

# Business Goal

The MDM layer ensures that every football player, club and competition has a single trusted representation inside the platform.

Everything else in the application depends on this layer.

The MDM is therefore considered the foundation of the entire platform.