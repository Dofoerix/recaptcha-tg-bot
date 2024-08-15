import os
from pathlib import Path

from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, JsonConfigSettingsSource, PydanticBaseSettingsSource, SettingsConfigDict


class MessagesText(BaseModel):
    joined: str
    answer: str
    no_nums: str
    no_text: str
    correct_0: str
    correct_1: str
    correct_2: str
    correct_3: str
    correct_4: str
    incorrect: str


class BotConfig(BaseSettings):
    token: SecretStr
    owner_id: int
    chat_ids: list[int]
    include_directories: list[str]
    exclude_directories: list[str]
    no_caption_directories: list[str]
    kick_delay: int
    messages_text: MessagesText

    model_config = SettingsConfigDict(
        json_file=os.path.join(Path(__file__).parents[1], 'settings.json'),
        json_file_encoding='utf-8'
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: BaseSettings,
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return JsonConfigSettingsSource(settings_cls),