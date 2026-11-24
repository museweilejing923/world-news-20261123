# World News — Monday, 23 November 2026, in One Image

Entry for the make.fun bounty **"Sum up 23 November's world news in one image"**
($100, 50 winners). One 1024x1024 infographic summing up the day's most
important world news, built to be polished and easy to understand at a glance.

## The image

Dark navy header with the date **MONDAY, 23 NOVEMBER 2026**, six main stories
as white cards (2x3 grid), each with a coloured top bar, a flat icon, a
category tag, a bold headline, one plain-English sentence and a key-data pill,
plus an "ALSO TODAY" footer with three more stories.

Main stories:

1. **Climate** — COP31 in Turkey collapsed after 49 hours of overtime; no deal
   on fossil fuels. (CNN, Reuters, Al Jazeera)
2. **War** — Ukraine says its drones sank a Russian warship off Libya; Russian
   strikes near Kyiv killed at least 15. (Reuters)
3. **Tech** — Nvidia reinstated Jensen Huang as CEO; shares jumped about 30%.
   (Reuters)
4. **Politics** — Democrats won 258 US House seats, the largest majority since
   1992, after flipping a North Carolina seat. (AP, CBS, Gulf News)
5. **Travel** — A Delta weight-and-balance computer failure delayed ~2,000
   flights on Thanksgiving Eve. (Xinhua, Business Standard, FlightAware)
6. **Diplomacy** — Nepal PM Balendra Shah's first visit to India; talks with
   PM Modi in New Delhi, 19 outcomes agreed. (Saachi Baat, PTI)

Also today: South Korea's education minister resigned over AI exam-cheating
fears (Reuters, Dawn); a candy factory fire in Banten, Indonesia killed 24
people; Yemen's Houthis claimed an attack on Saudi Arabia's Rabigh refinery.

## How it is built

The image is drawn programmatically with Pillow (`build_image.py`) — no AI
image generation, so the text is crisp and never garbled. `main.py` embeds
the finished PNG as base64 and writes it to `/output/entry.png`. It uses no
network, no randomness and no clock, so repeated runs are byte-identical.

## Run

```sh
python3 main.py        # writes /output/entry.png
python3 build_image.py # regenerates entry.png from scratch
```

## Files

- `main.py` — entry program (Python 3.13)
- `entry.png` — the infographic, 1024x1024, under 1 MiB
- `build_image.py` — the Pillow program that draws `entry.png`
- `LICENSE` — MIT
