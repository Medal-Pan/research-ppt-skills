# Research PPT Skills

[中文](README.md) · English

A research presentation skill collection maintained by [Medal-Pan](https://github.com/Medal-Pan), combining a lightweight custom image-reconstruction skill with attributed local versions of third-party skills.

| Task | Skill | Main output |
| --- | --- | --- |
| Paper → journal club presentation | [nature-paper2ppt](skills/nature-paper2ppt/SKILL.md) | Editable PPTX with source figures and speaker notes |
| Screenshot → editable text and simple shapes | [image-to-editable-ppt](skills/image-to-editable-ppt/SKILL.md) | Hybrid reconstruction, preview and source comparison |
| Image-only slides → finer object reconstruction | [nature-image2ppt](skills/nature-image2ppt/SKILL.md) | Object-level PPTX with page manifests and visual QA |
| Article / outline → visually consistent image slides | [codex-ppt](skills/codex-ppt/SKILL.md) | Image-based PPTX with notes; slide artwork remains raster |
| Scientific data → Origin figures in PowerPoint | [ace-sci-origin](skills/ace-sci-origin/SKILL.md) | Editable Origin project and PPT OLE objects; Windows required |

## Install

```bash
git clone https://github.com/Medal-Pan/research-ppt-skills.git
cd research-ppt-skills
python scripts/install_skills.py --skill image-to-editable-ppt --dry-run
python scripts/install_skills.py --skill image-to-editable-ppt
```

The standard-library installer copies selected skill directories only. It refuses to overwrite an existing installation. The default destination is `$CODEX_HOME/skills`, or `~/.codex/skills` if unset. Use `--dest` for another host; host compatibility has not been exhaustively tested.

Runtime dependencies are installed separately. See [installation](docs/INSTALL.md), the selected skill, and its requirements. `nature-paper2ppt` includes its shared terminology reference for standalone installation.

## Use

Attach your source material and ask your agent:

```text
Use $image-to-editable-ppt to reconstruct the attached slide as a 16:9 PPTX.
Keep complex artwork as source crops and rebuild major text and simple shapes
as editable PowerPoint objects. Include a rendered preview and source comparison.
```

Reconstruction is hybrid; photographs and complex local visuals may remain images. Never infer experimental data from appearance without labeling it as approximate. Online image/OCR services may receive the relevant inputs. Structural package checks are not a substitute for rendered visual review.

## Attribution

Third-party licenses remain in each skill directory. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for upstream projects, packaging changes and linked companion tools. Original collection documentation, installer, validator and the lightweight `image-to-editable-ppt` skill use [MIT](LICENSE).
