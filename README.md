[![news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/c/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/Erwinsays12/makefun-news-image-20261120/rank.svg)](https://make.fun/c/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/Erwinsays12/makefun-news-image-20261120/reward.svg)](https://make.fun/c/news-image-20261120)

# World News in One Image — Friday, 20 November 2026

A newspaper-style front page that sums up Friday 20 November 2026 in a
single 1024×1024 image: the first-ever Trump–Xi–Putin three-way summit
opening at the APEC meeting in Shenzhen (with Trump saying no rush on
Iran — the war decision waits until 2027), the ICJ ruling 9–6 that
Myanmar committed genocide against the Rohingya, Cyclone Akvan driving
300,000 people from their homes on India's east coast, Voyager 1 passing
a light-day from Earth, GTA VI sales passing $1.8 billion, and engine
trouble ending Hayabusa2's asteroid landing — plus a ticker of the day's
other stories (Europe ready for Ukraine talks with Russia, Nicholls'
113* in Wellington, Anthropic's $1.5 trillion valuation, World
Children's Day).

## How it works

- `draw_poster.py` renders the poster with Pillow and the system DejaVu
  fonts — flat vector-style art and crisp text, no photographs, no network.
- `entry.png` is the rendered poster (1024×1024, under 1 MiB).
- `main.py` (Python 3.13, standard library only) copies `entry.png` to
  `$MAKEFUN_OUTPUT_DIR/entry.png`, so both grader runs write identical
  bytes.

## Run it locally

```sh
python3 draw_poster.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Entry for the [news-image-20261120 competition](https://make.fun/c/news-image-20261120)
on [make.fun](https://make.fun).
