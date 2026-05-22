"""
CloakBrowser driver — agent-facing script.
Usage: uv tool run --from "cloakbrowser[patchright]" python driver.py <url> [--headed] [--screenshot path.png]
"""
import sys, time, json, argparse
sys.stdout.reconfigure(encoding='utf-8')
from cloakbrowser import launch

parser = argparse.ArgumentParser()
parser.add_argument("url", help="URL to navigate to")
parser.add_argument("--headed", action="store_true", help="Show browser window")
parser.add_argument("--screenshot", default="screenshot.png", help="Screenshot output path")
parser.add_argument("--wait", type=int, default=3, help="Seconds to wait after load")
parser.add_argument("--recaptcha", action="store_true", help="Intercept reCAPTCHA v3 score")
args = parser.parse_args()

browser = launch(backend="patchright", headless=not args.headed, humanize=True)
page = browser.new_page()
page.set_viewport_size({"width": 1280, "height": 900})

score_result = {}
if args.recaptcha:
    def handle_response(response):
        if "recaptcha-v3-verify" in response.url or "v3scores" in response.url:
            try:
                score_result.update(response.json())
            except:
                pass
    page.on("response", handle_response)

page.goto(args.url)

if args.recaptcha:
    for _ in range(25):
        time.sleep(1)
        if "Received response" in page.inner_text("body"):
            break
    if score_result:
        print("RECAPTCHA:", json.dumps(score_result))
else:
    time.sleep(args.wait)

page.screenshot(path=args.screenshot)
print("title:", page.title())
print("url:", page.url)
print("screenshot:", args.screenshot)

browser.close()
