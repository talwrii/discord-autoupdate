# Discord auto update
**@readwithai** - [X](https://x.com/readwithai) - [blog](https://readwithai.substack.com/) - [machine-aided reading](https://www.reddit.com/r/machineAidedReading/) - [📖](https://readwithai.substack.com/p/what-is-reading-broadly-defined
)[⚡️](https://readwithai.substack.com/s/technical-miscellany)[🖋️](https://readwithai.substack.com/p/note-taking-with-obsidian-much-of)

Automatically update discord if there is a new version when it runs on linux.

Discord, in their wisdom force you to install a new version of discord on Linux whenever one exists but does not handle the update themselves. They also quite regularly update discord. I want to run discord when my computer starts - but this behaviour is making this impossible.

This script installs a new version of discord if it exists and then run discords.

## Installation
You can install discord-autoupdate using [pipx](https://github.com/pypa/pipx):

```
pipx install discord-autoupdate
```

## Usage
If you run `discord-autoupdate` this will install a new version of discord if it exists and then run discords.

There are some other options which you can see with `--help`.

I use the following autostart script (in `~/.config/autostart`) to run `discord-autoupdate` on startup:

```
[Desktop Entry]
Exec=/home/alex/.local/bin/discord-autoupdate
Icon=Discord
Name=Discord
StartupNotify=true
Terminal=false
Type=Application
Version=1.0
```

You may wish to [add a desktop file](https://readwithai.substack.com/p/a-primer-on-linux-desktop-files) to run discord-autoupdate.

## About me
I am **@readwithai**. I create tools for reading, research and agency sometimes using the markdown editor [Obsidian](https://readwithai.substack.com/p/what-exactly-is-obsidian).

I also create a [stream of tools](https://readwithai.substack.com/p/my-productivity-tools) that are related to carrying out my work.

I write about lots of things - including tools like this - on [X](https://x.com/readwithai).
My [blog](https://readwithai.substack.com/) is more about reading and research and agency.
