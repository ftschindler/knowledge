# Hardware

A machine or peripheral in daily use: what it is, and how it presents itself to Linux.

One page per device, flat. A device page holds the standing facts about a thing, so everything
learned *whilst fixing* one lives under its own nature and links back here: a driver quirk that
cost an afternoon is a [finding](../findings/index.md), the software it was fixed in is a
[tool reference](../tools/index.md). That split is
[Split orthogonal classification axes across folders and tags](../knowledge_management/split_orthogonal_classification_axes_across_folders_and_tags.md)
applied to physical kit, and it is the reason this directory is a genre rather than a subject:
`hardware` is also a tag, and the tag is what collects the findings.

Three conventions are local to this genre.

**No page here carries an identifier that singles out a unit.** Model names, chipsets, firmware
versions and codec support are what make a page useful to anyone. Serial numbers, service tags,
MAC addresses and hostnames identify one machine and its owner, and this bundle is published.
Where a command's output is quoted and contained an address, the address is replaced with an
obvious placeholder rather than trimmed silently.

**The facts are read off the running device, not off a spec sheet**, because what a vendor
lists and what the kernel enumerates routinely differ. A page says which it is when the two
disagree.

**A device page is dated by the software it was read through.** Kernel and distribution
versions belong in the table, since half of what a page claims is really a claim about a
driver.

## Devices

- [Dell Precision 5470](dell_precision_5470.md) - the notebook these notes are written on: a 14-inch Alder Lake workstation whose audio runs over SoundWire and whose Bluetooth shares a die with its Wi-Fi
- [OpenMove by Shokz](openmove_by_shokz.md) - the open-ear bone-conduction headset, its four Bluetooth profiles, and the reason it is used in the low-quality one
