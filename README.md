# Greak Sentry

A community bot for the GreakArmo gaming server on [Fluxer](https://fluxer.app), written in Python.

## What it does

- **Welcomes new members** in #welcome-lobby and points them to the rules.
- **Rules check.** Members react ✅ to the rules message to get the **Verified** role. Voice channels only let Verified members in, so no reaction means no voice.
- **Game roles.** Members react in #pick-your-games to get roles for Battlefield 6, The Division 2, Marvel Rivals, Overwatch, and Space Marine 2.
- **Free games.** Posts new free-to-keep PC games (Steam, Epic, GOG, Ubisoft) with how long they're free. Data comes from GamerPower.
- **Patch notes.** Posts official update announcements for each game from Steam into that game's own patch notes channel (like #bf6-patch-notes) and pings that game's role.
- **Twitch alerts** when GreakArmo goes live.
- **YouTube alerts** when a new video is uploaded.
- **Moderation.** Watches #general for aggressive language. It deletes the message, gives a strike, and times people out after too many strikes. Severe stuff gets an instant timeout. Admins and mods are never flagged. Everything is logged in #mod-log.
- **Join and leave log** in #mod-log.

Everything you'd want to change is in **`config.toml`**, including channel names, games, messages, the word lists, and how strict moderation is.

---

## 1. Create the bot on Fluxer

1. Create a new application in Fluxer's developer or bot settings and add a bot to it.
2. Copy the **bot token**. Treat it like a password.
3. If there are switches for **Server Members** and **Message Content** access, turn both on. The bot needs them to see people join and to read chat for moderation and commands.
4. Invite the bot to your server with these permissions:
   - Manage Roles, Manage Channels, Manage Messages
   - Timeout Members (sometimes called Moderate Members)
   - View Channels, Send Messages, Embed Links, Add Reactions, Read Message History
   - Mention @everyone (for live and video alerts)
5. **Important:** In your server's role list, drag the bot's role **above** Verified and all the game roles. A bot can only give out roles that sit below its own.

## 2. Run it on your PC

You need Python 3.11 or newer.

```bash
git clone https://github.com/entity97/Greak-Sentry.git
cd Greak-Sentry
python -m venv .venv
# Windows:  .venv\Scripts\activate
# Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Copy `.env.example` to a new file called `.env` and fill in:

```
FLUXER_TOKEN=your-bot-token
GUILD_ID=your-server-id
```

Then start it:

```bash
python main.py
```

Leave that window open. The bot runs while it's open and your PC is awake.

If you have Docker installed, you can use `docker compose up -d` instead. It keeps running in the background and restarts on its own.

## 3. Set up your server (one time)

In any channel, type:

| Command | What it does |
|---|---|
| `!setup` | Creates any missing channels and roles from `config.toml`, then posts the rules message and the game roles message with their reactions. Safe to run again. It only adds what's missing. |
| `!lockvoice` | Locks every voice channel so only **Verified** members can join. Run it again whenever you add a new voice channel. |

After `!setup`, you may want to:

- Make **#mod-log** private so only mods can see it.
- Make **#rules** and the alert channels read-only for regular members. They can still react.

Existing members, including you, need to react to the rules too, unless they have a role that can already join voice.

## Commands

| Command | Who | What |
|---|---|---|
| `!sentry` | Everyone | Lists the commands |
| `!freegames` | Everyone | Shows free games you can claim right now |
| `!setup` | Admins | Creates missing channels and roles, and posts the panels |
| `!lockvoice` | Admins | Restricts voice channels to Verified members |
| `!checkfeeds` | Admins | Checks free games, patch notes, Twitch, and YouTube right away |
| `!pardon @user` | Admins | Clears someone's language strikes |

"Admins" means the server owner, or anyone with a role listed under `admin_roles` in `config.toml` (Admin and Moderator by default).

## Changing things

Open `config.toml`. Every section has comments explaining it. Common changes:

- **Add a game.** Copy one of the `[[games]]` blocks, change the name, role, and emoji, and add its Steam app ID for patch notes. The ID is the number in the game's Steam store link. Set `patch_channel` and `category`, then run `!setup` again.
- **Patch notes channels.** Each game's notes go to its `patch_channel`. `!setup` creates that channel inside the game's `category` if a category with that name exists. Emojis and caps are ignored, so "💥 BATTLEFIELD 6" matches "Battlefield 6". Create your categories before running `!setup`. If you'd rather have one shared channel, leave `patch_channel` blank and set `patch_notes` under `[channels]`.
- **Rename a channel.** Change it under `[channels]` to match your server.
- **Moderation words.** Add to `warn_terms` or `severe_terms`. Matching ignores caps, stretched letters ("fuuuck"), and swaps like `0` for `o`.
- **Pings.** Each alert has a `ping` setting. Use `"@everyone"`, `"@here"`, a role name like `"Free Games"`, or `""` for no ping.

Restart the bot after editing `config.toml`.

## Twitch keys (optional but recommended)

Twitch alerts work out of the box using a free public service. For faster, more reliable alerts, use Twitch's official API:

1. Go to [dev.twitch.tv/console](https://dev.twitch.tv/console) and log in.
2. Click **Register Your Application**. Use any name, set the OAuth Redirect URL to `http://localhost`, and choose the category **Chat Bot**.
3. Open the app, copy the **Client ID**, then click **New Secret** and copy that too.
4. Add both to `.env`:
   ```
   TWITCH_CLIENT_ID=...
   TWITCH_CLIENT_SECRET=...
   ```

## How the feeds avoid spam

The first time each feed runs, the bot just notes what's already out there and doesn't post it. After that, it only posts new things. What it has posted is saved in `data/state.json`. If that file is lost, the bot starts fresh without reposting old items.

If the stream is already live when the bot starts, it won't announce it. It announces the next time you go live.

## Hosting on FluxerHost

The repo includes a `Dockerfile`, so it's ready for container hosting.

- Set `FLUXER_TOKEN`, `GUILD_ID`, and the optional Twitch keys as **environment variables** in the host's settings. Don't upload `.env`.
- If the host offers persistent storage, attach it at `/app/data` so the bot remembers what it posted between restarts.
- The bot only makes outgoing connections. It doesn't listen on any ports.
- 1 CPU, 0.5 GB RAM, and 1 GB of storage is plenty.

## Tests

```bash
python -m unittest discover tests
```

These run offline with a fake Fluxer server. They check welcomes, reaction roles, voice locking, moderation, and the feed parsers.

## Project layout

```
main.py              Starts the bot
config.toml          All your settings
sentry/
  core.py            Connects to Fluxer and finds your channels and roles
  welcome.py         Welcome messages, join and leave log
  roles.py           Rules check, game roles, !setup, !lockvoice
  moderation.py      Language filter, strikes, timeouts
  feeds.py           Free games, patch notes, Twitch, YouTube
  commands.py        ! commands
  parsers.py         Reads the data from each feed
  text.py            Word matching and text helpers
  state.py           Saves what's been posted
```

## Credits

Built on [fluxer.py](https://github.com/Fluxer-py/fluxer.py). Free games data by [GamerPower](https://www.gamerpower.com).
