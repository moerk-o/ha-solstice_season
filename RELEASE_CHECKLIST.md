# Release Checklist

## Before Release

- [ ] All changes are merged into `main`
- [ ] Bump version in `custom_components/solstice_season/manifest.json`
- [ ] Update `RELEASENOTES.md`:
  - [ ] Add new version section at the top
  - [ ] Link issue numbers: `[#123](https://github.com/moerk-o/ha-solstice_season/issues/123)`
  - [ ] Keep previous versions below
  - [ ] Use consistent section headers and icons from previous releases:
    - ✨ New Features
    - 🐞 Bug Fixes
    - 🔧 Infrastructure
    - 📝 Documentation
    - 💬 Feedback Needed!
  - [ ] For new section types, discuss first before adding
- [ ] Update README.md if needed (document new features/attributes)
- [ ] Commit and push changes

## Create Release

```bash
gh release create vX.Y.Z --title "vX.Y.Z" --notes-file RELEASENOTES.md
```

## After Release

- [ ] GitHub workflow (`release.yml`) automatically creates `solstice_season.zip` and attaches it to the release
- [ ] Verify ZIP is present in the release assets

## Workflows

The following GitHub Actions workflows run automatically:

- **validate.yaml** - Runs on every push/PR, validates Home Assistant (Hassfest) and HACS compatibility. Required for HACS listing.
- **release.yml** - Runs when a release is published, creates and uploads the ZIP asset.
