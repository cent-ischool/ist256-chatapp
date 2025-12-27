# Project Requirements

This document tracks high-level feature requirements for the IST256 Chatapp organized by version.

## Version Guidelines

- **Major version** (x.0.0): Breaking changes, major architectural shifts
- **Minor version** (1.x.0): New features, backward compatible
- **Patch version** (1.0.x): Bug fixes, minor improvements

---

## v1.0.1

**Status**: Released
**Release Date**: 2025-01-15

### Features

- Added "Session" page to admin menu to view session variables
- Added version number constant in constants.py
- Version number displayed in the app footer of the sidebar

### Technical Notes

- Simple implementation, no database changes
- UI-only feature using Streamlit
- Admin-only access via user type check
