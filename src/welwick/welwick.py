import importlib.metadata
import importlib.resources
import logging
import os
import random
import sys
from dataclasses import dataclass
from typing import List, Optional

from mastodon import Mastodon

logger = logging.getLogger(__name__)


# creating a type to use for passing around our fortunes
@dataclass
class Fortune:
    text: str
    image_name: str
    image_type: str
    image_text: str
    weight: int = 0
    image_path: str = None


def get_version(package_name: str = __name__) -> str:
    try:
        return importlib.metadata.version(package_name)
    except importlib.metadata.PackageNotFoundError:
        return "0.0.0"


def get_mastodon_token(token: Optional[str], token_stdin: bool) -> str:
    # if provided then use it
    if token is not None:
        token = token.strip()
        if len(token):
            return token

    # if we were told to look to stdin then look there
    if token_stdin:
        tokens = sys.stdin.read().splitlines()
        if len(tokens) and len(tokens[0]):
            token = tokens[0].strip()
            if len(token):
                return token

    # if we didn't find it anywhere else then look for an environment variable
    token = os.environ.get("API_TOKEN")
    if token is not None:
        token = token.strip()
        if len(token):
            return token

    # no token found anywhere
    raise ValueError("No value for API_TOKEN.")


def get_mastodon_api(url: Optional[str]) -> str:
    # if provided then use it
    if url is not None:
        url = url.strip()
        if len(url):
            return url

    # if we didn't find it anywhere else then look for an environment variable
    url = os.environ.get("API_URL")
    if url is not None:
        url = url.strip()
        if len(url):
            return url

    # no token found anywhere
    raise ValueError("No value for API_URL.")


def generate_fortune() -> Fortune:
    choices: List[str] = [
        "Ah... yes, I can hear the spirits whispering something to me...",
        "Hoo.. I see a glimmer within my scrying orb... A shard of knowledge from the future!",
    ]
    intro_text = random.choice(choices)

    choices: List[Fortune] = [
        Fortune(
            text="The spirits are very happy today! They will do their best to shower everyone with good fortune.",
            image_name="LuckStar.gif",
            image_type="image/gif",
            image_text="An oracle wearing a blue robe. Their arms are raised to behold a glowing star above their head.",
            weight=15,
        ),
        Fortune(
            text="The spirits are in good humor today. I think you'll have a little extra luck.",
            image_name="LuckPyramid.gif",
            image_type="image/gif",
            image_text="An oracle wearing a blue robe. Their arms are raised to behold a bouncing pyramid above their head.",
            weight=20,
        ),
        Fortune(
            text="The spirits feel neutral today. The day is in your hands.",
            image_name="LuckSwirlingLights.gif",
            image_type="image/gif",
            image_text="An oracle wearing a blue robe. Their arms are raised to behold a swirling light above their head.",
            weight=15,
        ),
        Fortune(
            text="This is rare. The spirits feel absolutely neutral today.",
            image_name="LuckSwirlingLights.gif",
            image_type="image/gif",
            image_text="An oracle wearing a blue robe. Their arms are raised to behold a swirling light above their head.",
            weight=5,
        ),
        Fortune(
            text="The spirits are somewhat annoyed today. Luck will not be on your side.",
            image_name="LuckBat.gif",
            image_type="image/gif",
            image_text="An oracle wearing a blue robe. Their arms are raised to behold a bat above their head, flapping its wings.",
            weight=10,
        ),
        Fortune(
            text="The spirits are somewhat mildly perturbed today. Luck will not be on your side.",
            image_name="LuckBat.gif",
            image_type="image/gif",
            image_text="An oracle wearing a blue robe. Their arms are raised to behold a bat above their head, flapping its wings.",
            weight=10,
        ),
        Fortune(
            text="The spirits are very displeased today. They will do their best to make your life difficult.",
            image_name="LuckSkull.gif",
            image_type="image/gif",
            image_text="An oracle wearing a blue robe. Their arms are raised to behold a laughing red skill above their head.",
            weight=15,
        ),
    ]

    # chose a fortune
    fortune = random.choices(choices, weights=[x.weight for x in choices])[0]

    # insert the intro text
    fortune.text = f"{intro_text}\n\n{fortune.text}"
    logger.info(f"fortune: {fortune.text}")

    # find the full path to the image for this fortune
    image_path = importlib.resources.files("welwick.media")
    fortune.image_path = [
        x
        for x in image_path.iterdir()
        if image_path.is_dir() and str(x).endswith(f"/{fortune.image_name}")
    ][0]

    return fortune


def run(
    token: str,
    token_stdin: bool,
    api_url: str,
) -> None:
    api_url = get_mastodon_api(api_url)
    api_token = get_mastodon_token(token, token_stdin)

    logger.info("using Mastodon API {}".format(api_url))
    mastodon = Mastodon(
        access_token=api_token,
        api_base_url=api_url,
    )

    fortune = generate_fortune()
    media = mastodon.media_post(
        fortune.image_path,
        mime_type=fortune.image_type,
        description=fortune.image_text,
        synchronous=True,
    )
    mastodon.status_post(fortune.text, media_ids=[media])
