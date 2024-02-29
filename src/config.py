from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env',
                                      env_file_encoding='utf-8',
                                      extra='ignore')
    db_user: SecretStr
    db_password: SecretStr
    db_host: str = 'mongo'
    db_port: SecretStr
    db_name: SecretStr
    coll_name: SecretStr
    telegram_token: SecretStr

    @property
    def mongodb_url(self) -> str:
        return 'mongodb://{user}:{password}@{host}:{port}'.format(
            user=self.db_user.get_secret_value(),
            password=self.db_password.get_secret_value(),
            host=self.db_host,
            port=int(self.db_port.get_secret_value()),
        )


conf = Config()


'''
    @property
    def bot_token(self):
        return self.telegram_token.get_secret_value()



    @property
    def database_uri(self):
        return f'{self.database_url}/{self.db_name.get_secret_value()}'
'''
