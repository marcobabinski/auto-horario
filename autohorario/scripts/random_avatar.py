import PIL.Image
import os
from dicebear import DAvatar, DStyle, DOptions, DColor, DFormat, bulk_create
import random
import uuid

# Enable anonymous usage statistics
os.environ['ENABLE_PYTHON_DICEBEAR_USAGE_STATS'] = 'false'

palette = ["#66a650", "#b9d850",  "#82dcd7", "#208cb2",  "#d78b98", "#a13d77",  "#b8560f", "#dc9824", "#efcb84", "#e68556", "#c02931"]

# Creating options
options = DOptions(
    backgroundColor=DColor(random.choice(palette)),
    scale=75,
)

# Making a DAvatar object
# for i in range(5):
#     av = DAvatar(
#         style=DStyle.avataaars_neutral,
#         # seed="autohorario",
#         options=options
#     )
#     print(av.url_svg)  # Prints the svg url

def generate(seed):
    id = uuid.uuid4()

    av = DAvatar(
        style=DStyle.avataaars_neutral,
        seed=seed,
        options=options
    )

    av.save(
        location="media",  # Passing `None` will save it in the current working directory
        file_name=id,
        file_format=DFormat.webp,
        overwrite=True,
        open_after_save=False
    )
    return f"media/{id}"

print(generate("123123123123"))

# Editing the DAvatar object
# av.edit(
#     extra_options=DOptions(backgroundColor=DColor("000000"))
# )
# # Using `extra_options` keep the `rotate` option but override the `backgroundColor` option

# print(av.url_webp)  # Prints the webp url

# # Editing the style specific customisations
# av.customise(
#     blank_options={
#         "face": "variant04"
#     }
# )
# # Using `blank_options` will delete your previous customisations for this DAvatar and generate new ones

# print(av.url_png)  # Prints the png url

# # Saving an avatar to your device
# av.save(
#     location=None,  # Passing `None` will save it in the current working directory
#     file_name="dicebear_avatar",
#     file_format=DFormat.svg,
#     overwrite=True,
#     open_after_save=False
# )

# # Converting the DAvatar object into a PIL.Image.Image object
# av_img: PIL.Image.Image = av.pillow()

# # Opening and viewing the DAvatar image
# av.open(use_pil=True)  # or av.view()

# # Creating multiple random avatars of the same style at once