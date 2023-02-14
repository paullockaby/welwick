import importlib.metadata
import importlib.resources
import logging
import os
import random
import sys
from collections import namedtuple
from typing import List, Optional

from mastodon import Mastodon

logger = logging.getLogger(__name__)


# creating a type to use for passing around our fortunes
FortuneData = namedtuple("FortuneData", ["text", "image_name", "image_text", "weight"])
Fortune = namedtuple("Fortune", ["text", "image_path", "image_text"])


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
    token = os.environ.get("ACCESS_TOKEN")
    if token is not None:
        token = token.strip()
        if len(token):
            return token

    # no token found anywhere
    raise ValueError("No value for ACCESS_TOKEN.")


def generate_fortune() -> Fortune:
    choices: List[FortuneData] = [
        FortuneData(
            text="The spirits are very happy today! They will do their best to shower everyone with good fortune.",
            image_name="Star",
            image_text="An oracle wearing a blue robe. Their arms are raised to behold a glowing star above their head.",
            weight=15,
        ),
        FortuneData(
            text="The spirits are in good humor today. I think you'll have a little extra luck.",
            image_name="Pyramid",
            image_text="An oracle wearing a blue robe. Their arms are raised to behold a bouncing pyramid above their head.",
            weight=20,
        ),
        FortuneData(
            text="The spirits feel neutral today. The day is in your hands.",
            image_name="SwirlingLights",
            image_text="An oracle wearing a blue robe. Their arms are raised to behold a swirling light above their head.",
            weight=15,
        ),
        FortuneData(
            text="This is rare. The spirits feel absolutely neutral today.",
            image_name="SwirlingLights",
            image_text="An oracle wearing a blue robe. Their arms are raised to behold a swirling light above their head.",
            weight=5,
        ),
        FortuneData(
            text="The spirits are somewhat annoyed today. Luck will not be on your side.",
            image_name="Bat",
            image_text="An oracle wearing a blue robe. Their arms are raised to behold a bat above their head, flapping its wings.",
            weight=10,
        ),
        FortuneData(
            text="The spirits are somewhat mildly perturbed today. Luck will not be on your side.",
            image_name="Bat",
            image_text="An oracle wearing a blue robe. Their arms are raised to behold a bat above their head, flapping its wings.",
            weight=10,
        ),
        FortuneData(
            text="The spirits are very displeased today. They will do their best to make your life difficult.",
            image_name="Skull",
            image_text="An oracle wearing a blue robe. Their arms are raised to behold a laughing red skill above their head.",
            weight=15,
        ),
    ]

    fortune = random.choices(choices, weights=[x.weight for x in choices])[0]

    image_path = importlib.resources.files("welwick.media")
    image_file = [
        x
        for x in image_path.iterdir()
        if image_path.is_dir() and str(x).endswith(f"/Luck{fortune.image_name}.gif")
    ][0]

    return Fortune(
        text=fortune.text,
        image_path=image_file,
        image_text=fortune.image_text,
    )


def run(
    token: str,
    token_stdin: bool,
    api_url: str,
) -> None:
    logger.info("using Mastodon API {}".format(api_url))
    token = get_mastodon_token(token, token_stdin)
    mastodon = Mastodon(
        access_token=token,
        api_base_url=api_url,
    )

    fortune = generate_fortune()
    media = mastodon.media_post(
        fortune.image_path,
        mime_type="image/gif",
        description=fortune.image_text,
        synchronous=True,
    )
    mastodon.status_post(fortune.text, media_ids=[media])
