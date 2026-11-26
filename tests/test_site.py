from html.parser import HTMLParser
from pathlib import Path
import re
import unittest
from urllib.parse import parse_qs, urlparse


ROOT = Path(__file__).resolve().parents[1]
VIDEOS = {
    "P6Va0_KILi4": "Universe Day 2 Keynote - 2025",
    "rRRXZTnJ22A": "GitHub Galaxy Virtual Keynote - 2023",
    "CyWoCxQtlZ8": "AMD x GitHub Customer Story - 2025",
    "NlFA9Ky9FTM": "GitHub Copilot App Launch - 2026",
    "spGNNNY7RRM": "RKO Keynote Opening Animation - 2025",
    "kjqk153yf64": "GitHub Universe Event Recap Sizzle - 2026",
    "0ZGKn4VfC74": "TQ Ventures Podcast - 2026",
    "8opU-MX7uGY": "Tuva AI company launch - 2026",
    "RCFEqGYVhOE": "Behind the scenes of GitHub Universe 2024",
}
LOCAL_POSTERS = {
    "P6Va0_KILi4": "./assets/universe-keynote.jpg",
    "rRRXZTnJ22A": "./assets/galaxy-keynote.jpg",
    "RCFEqGYVhOE": "./assets/universe-documentary.jpg",
}


class Document(HTMLParser):
    def __init__(self):
        super().__init__()
        self.elements = []

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))


class SiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (ROOT / "index.html").read_text()
        cls.doc = Document()
        cls.doc.feed(cls.html)

    def test_video_associations_and_order(self):
        videos = [
            (attrs["data-video"], attrs["data-title"])
            for tag, attrs in self.doc.elements if tag == "figure" and "data-video" in attrs
        ]
        self.assertEqual(videos, list(VIDEOS.items()))
        links = [
            parse_qs(urlparse(attrs["href"]).query).get("v", [None])[0]
            for tag, attrs in self.doc.elements
            if tag == "a" and "youtube.com/watch" in attrs.get("href", "")
        ]
        for video_id in VIDEOS:
            self.assertEqual(links.count(video_id), 2)
            self.assertIn(
                LOCAL_POSTERS.get(video_id, f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"),
                self.html,
            )

    def test_accessible_document(self):
        elements = self.doc.elements
        self.assertIn(("html", {"lang": "en"}), elements)
        self.assertEqual(sum(tag == "h1" for tag, _ in elements), 1)
        self.assertEqual(sum(tag == "article" for tag, _ in elements), 8)
        self.assertFalse(any(tag == "iframe" for tag, _ in elements))
        ids = [attrs["id"] for _, attrs in elements if "id" in attrs]
        self.assertEqual(len(ids), len(set(ids)))
        for tag, attrs in elements:
            if tag == "img":
                self.assertIn("alt", attrs)
                self.assertIn("width", attrs)
                self.assertIn("height", attrs)
            if "aria-labelledby" in attrs:
                self.assertIn(attrs["aria-labelledby"], ids)
            if tag == "a" and attrs.get("href", "").startswith("#"):
                self.assertIn(attrs["href"][1:], ids)
            if tag == "a" and attrs.get("target") == "_blank":
                self.assertIn("noopener", attrs["rel"])

    def test_local_assets_and_subpath_support(self):
        urls = []
        for tag, attrs in self.doc.elements:
            for attr in ("src", "href"):
                if attr in attrs:
                    urls.append(attrs[attr])
            if "srcset" in attrs:
                urls.extend(part.strip().split()[0] for part in attrs["srcset"].split(","))
        urls.extend(re.findall(r'url\("([^"]+)"\)', (ROOT / "styles.css").read_text()))
        for url in urls:
            self.assertFalse(url.startswith("/"), f"Root-relative path breaks Pages: {url}")
            if url.startswith("./"):
                asset = ROOT / url
                self.assertTrue(asset.is_file(), f"Missing asset: {url}")
                self.assertGreater(asset.stat().st_size, 0)
        self.assertTrue((ROOT / ".nojekyll").is_file())
        self.assertFalse((ROOT / "CNAME").exists())

    def test_valid_local_fonts_and_image_budget(self):
        for path in (ROOT / "assets").glob("*.woff2"):
            self.assertEqual(path.read_bytes()[:4], b"wOF2")
        for name in ("FiraSans-OFL.txt", "Montserrat-OFL.txt"):
            self.assertIn("SIL OPEN FONT LICENSE", (ROOT / "assets" / name).read_text())
        for name in ("steve-james.jpg", "steve-james-small.jpg"):
            image = ROOT / "assets" / name
            self.assertEqual(image.read_bytes()[:2], b"\xff\xd8")
            self.assertLess(image.stat().st_size, 200_000)


if __name__ == "__main__":
    unittest.main()
