# Publishing & Branch Strategy

## Branch Structure

```
main                    ← stable, tagged releases only
├── develop             ← integration branch (PRs merge here)
│   ├── feature/xxx     ← new features
│   └── fix/xxx         ← bug fixes
└── release/x.y.z      ← release candidates → triggers TestPyPI
```

## Workflow

```
1. feature/add-fno-support → PR → develop
2. develop (tested, stable) → create branch release/0.2.0
3. release/0.2.0 push → GitHub Actions → auto-publish to TestPyPI
4. Test: pip install -i https://test.pypi.org/simple/ nse-data==0.2.0
5. If good → merge release/0.2.0 → main → tag v0.2.0
6. Tag v0.2.0 push → GitHub Actions → auto-publish to PyPI
```

## Triggers

| Event | Target | When |
|-------|--------|------|
| Push to `release/*` branch | **TestPyPI** | Creating/updating a release branch |
| Push tag `v*` | **PyPI (production)** | Tagging a release on main |
| Manual workflow dispatch | Either | On-demand from GitHub Actions UI |

## One-Time Setup (GitHub)

### 1. Create GitHub Environments

Go to **Settings → Environments** and create:

- **`testpypi`** — no protection rules needed
- **`pypi`** — add protection rule: "Required reviewers" (yourself)

### 2. Configure Trusted Publishing (OIDC — no tokens needed)

#### TestPyPI
1. Go to [test.pypi.org/manage/account/publishing](https://test.pypi.org/manage/account/publishing/)
2. Add new publisher:
   - PyPI project name: `nse-data`
   - Owner: `NikhilSuthar`
   - Repository: `nse-data`
   - Workflow: `publish.yml`
   - Environment: `testpypi`

#### PyPI
1. Go to [pypi.org/manage/account/publishing](https://pypi.org/manage/account/publishing/)
2. Add new publisher:
   - PyPI project name: `nse-data`
   - Owner: `NikhilSuthar`
   - Repository: `nse-data`
   - Workflow: `publish.yml`
   - Environment: `pypi`

### 3. No API tokens needed
The workflow uses OIDC trusted publishing — GitHub proves identity to PyPI without storing secrets.

## Manual Publishing (Local)

If you need to publish manually without GitHub Actions:

```bash
# Install tools
pip install build twine

# Build
python -m build

# Publish to TestPyPI
twine upload --repository testpypi dist/*

# Test install
pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ nse-data

# Publish to PyPI (production)
twine upload dist/*
```

## Version Bumping

Update version in TWO places before creating a release branch:
1. `pyproject.toml` → `version = "x.y.z"`
2. `src/nsedata/__init__.py` → `__version__ = "x.y.z"`

## Quick Commands

```bash
# Create release branch (triggers TestPyPI)
git checkout develop
git checkout -b release/0.1.0
git push -u origin release/0.1.0

# After testing, merge to main and tag (triggers PyPI)
git checkout main
git merge release/0.1.0
git tag v0.1.0
git push origin main --tags

# Clean up
git branch -d release/0.1.0
git push origin --delete release/0.1.0
```
