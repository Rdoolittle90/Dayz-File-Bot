from disnake import ModalInteraction
from disnake.ui import Modal, TextInput



class RemoveMapModal(Modal):
    def __init__(self) -> None:
        components: list = [
            TextInput(
                label="Map Name",
                placeholder="Namalsk",
                custom_id=f"map",
                min_length=1,
                max_length=25,
                required=True
            ),
            TextInput(
                label="Enter passkey",
                placeholder="use /get_key",
                custom_id=f"passkey",
                min_length=16,
                max_length=16,
                required=True
            )
        ]
        super().__init__(title="Select an Option Catagory", components=components)
    

    async def callback(self, interaction:ModalInteraction) -> None:
        map_str: str = interaction.data["components"][0]["components"][0]["values"][0]
        passkey: str = interaction.data["components"][0]["components"][0]["value"]

        print(map_str)
        print(passkey)