# Steve James portfolio

A lightweight, independent implementation of [stevejames.tv](https://stevejames.tv/),
published at **https://muadsteeb.github.io/steve-james-portfolio/**.
The original domain and DNS are unchanged.

## Run locally

No build step, framework, or package installation is required:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Open http://127.0.0.1:8000. All site assets use relative paths, including fonts,
so the site also works under the GitHub Pages repository subpath.

## Update the portfolio

- `index.html` holds the biography and eight projects in the reference site's
  desktop row order. Each project keeps its video, category, title, role, and
  description together on mobile.
- `styles.css` defines the responsive layout and reduced-motion behavior.
- `script.js` progressively enhances navigation and video links. Without
  JavaScript, the navigation remains visible and video posters link to YouTube.
- Each `figure.video` has a YouTube ID in `data-video`, an accessible player title
  in `data-title`, matching poster/watch URLs, and a direct YouTube fallback link.
  Update all of those together when replacing a video.
- `assets/` contains the optimized portrait, favicon, and locally hosted fonts.

Video players are created only after a click and use `youtube-nocookie.com`.
Only one player remains active at a time; viewers can close it or use the direct
YouTube link if embedding is unavailable. Thumbnails still connect to YouTube
before playback. There are no analytics, tracking scripts, or contact forms.

## Publish

GitHub Pages is configured to deploy from **`main`, `/` (repository root)**.
Push changes to `main` and GitHub's Pages workflow publishes them automatically.
`.nojekyll` keeps this a plain static site. There is intentionally no `CNAME` file.

The site has no generated output or runtime dependencies. To check its structure:

```sh
python3 -m unittest discover -s tests -v
```

For browser interaction and layout checks, run the local server and open
http://127.0.0.1:8000/tests/browser.html. The harness checks 390px mobile,
768px tablet, and 1440px desktop layouts, navigation, video activation/closing,
and project associations. Also review the actual site visually at these widths.

## Content and assets

The owner authorized reuse of the portrait and written portfolio content from
stevejames.tv on November 19, 2026. Project dates, roles, descriptions, and video
associations reflect that reference snapshot; they are not generated claims.
The portrait is resized from the original hosted image. Public YouTube videos
remain on their original channels, with the original video IDs preserved.
No ownership of those third-party videos is implied.

Fira Sans and Montserrat are distributed under the SIL Open Font License;
their license notices are included in `assets/`. Portfolio content and the
portrait are not offered under those font licenses.
