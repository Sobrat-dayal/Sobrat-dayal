# Publish your GitHub profile

## Destination

Use the public profile repository **Sobrat-Dayal/Sobrat-Dayal**. GitHub currently reports its canonical spelling as `Sobrat-dayal/Sobrat-dayal`; these URLs refer to the same existing account and repository. Do not create a second account or an extra nested repository folder.

1. Sign in as Sobrat-Dayal and open https://github.com/Sobrat-Dayal/Sobrat-Dayal.
2. Back up the existing README and assets before replacing files. This package has not changed anything on GitHub.
3. Upload the **contents** of `Sobrat Github`, with `README.md` at the repository root and the `assets` and `scripts` folders beside it. Do not upload the enclosing folder or the ZIP itself.
4. Include `.github/workflows/refresh-profile.yml`. Hidden folders can be omitted by some file pickers. If needed, use GitHub's **Add file → Create new file**, enter that exact path, and paste its contents.
5. Review the diff and commit to the default branch. Keep the repository public. Open your profile and check the README.
6. Under **Actions**, enable workflows if prompted. Select **Refresh profile visuals → Run workflow** on the default branch. No personal access token or paid service is required; GitHub supplies a repository-scoped token.
7. Check that the run succeeds and updates the date in the activity graphics. The schedule requests 02:17 UTC (07:47 IST) daily, but GitHub can delay scheduled jobs or disable them after inactivity. Branch protection or organization policy may block the bot's push; adjust the policy intentionally or refresh manually instead.

The bundled dated images already work without Actions. To refresh locally, run `python scripts/update_profile.py` with Python 3.10 or newer and internet access. It uses only the standard library. Commit the two updated SVGs afterward.

## Make it yours

- Review the About wording. It is based only on public repository descriptions, not assumed education, employment, awards, or expertise.
- Add your actual LinkedIn, portfolio, and email links in Connect. No guessed social identities are included.
- Add technologies only when they represent your work. The current stack is intentionally limited to verified repository metadata.
- Featured descriptions summarize repository descriptions; they are not claims that a deployed service is available or independently tested.
- GitHub's avatar, sidebar, pinned repositories, native contribution calendar, and achievement badges are controlled by GitHub settings. A README cannot replace them. Pin the featured repositories separately in your profile UI.

## Layout and refresh behavior

The profile uses standard Markdown, headings, links, and supported image/alignment HTML. There are no scripts, iframes, style tags, CSS grids, or unsupported custom fonts in the README. The hero scales with the available width; individual stack badges wrap; projects stack vertically on narrow screens. SVG text is baked into the image and becomes smaller on mobile, so the essential introduction is repeated as real text beneath it.

All displayed images are relative local files. No third-party badge or stats service is required at viewing time. The separate 3D workflow uses the open-source GitHub Profile 3D Contrib action. The refresh script reads GitHub's public REST API and contribution-calendar HTML, validates the result, and then writes both graphics. If fetching fails, the workflow fails and the old dated images remain. GitHub HTML changes may require a parser update. Colors represent the levels returned by GitHub, not invented contribution counts. Graph dates are GitHub's dates; update timestamps are UTC.

Public source metadata and visual checks are documented in `VERIFICATION.md`. Asset and code terms are in `ATTRIBUTION.md` and `LICENSE`.

Reference: https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme

## Offline preview

Open `PREVIEW.html` in a browser to inspect a GitHub-rendered version with approximate dark-theme styling. It is a convenience preview, not the profile implementation; GitHub uses README.md. It can be omitted from the repository. Its rendered text is a static copy and must be regenerated if the README text changes.

## 3D building-style contribution tracker

The main README now uses `profile-3d-contrib/profile-night-green.svg`, matching the green building view in the supplied Pratham1603 profile. The bundled image was generated for **Sobrat-Dayal** using the same upstream generator (updated to v0.9.3); it is not Pratham's activity relabeled.

Upload `.github/workflows/profile-3d.yml` along with the README and `profile-3d-contrib` folder. Then open **Actions → Update 3D contribution skyline → Run workflow**. The workflow refreshes at 02:47 UTC (08:17 IST) daily, subject to GitHub scheduling delays. It is pinned to an upstream commit and uses GitHub's automatic repository token. No manually created secret is needed. Both image workflows share a concurrency group to avoid simultaneous bot pushes.

The generator also creates alternate palettes on its first run. To select a different style, change the README image filename to `profile-night-view.svg` or `profile-gitblock.svg` after the workflow creates it. The packaged initial view is night-green.

The initial image was generated using the existing signed-in GitHub CLI session; no token is included in this package. The scheduled repository token may have a narrower data view. Only enable private contribution visibility if you intend those aggregate counts to appear on your public profile. The language panel is replaced by scripts/enrich_languages.py: it lists every language returned by GitHub's languages API for public non-fork repositories, weighted by source bytes. This measures repository contents, not proficiency or commit activity.

The old flat calendar is retained in assets as an optional alternative. `Refresh profile visuals` still updates it and the repository statistics; `Update 3D contribution skyline` updates the buildings. No workflow has been published or run remotely by this task.
