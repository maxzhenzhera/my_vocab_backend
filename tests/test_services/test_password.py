import pytest
from pytest_mock import MockerFixture

from app.core.settings.dataclasses_.components import PasswordSettings
from app.db.models import User
from app.services.password import PasswordService


class TestPasswordService:
    @pytest.fixture(name='initial_password')
    def fixture_initial_password(self) -> str:
        return 'init_password'

    @pytest.fixture(name='new_password')
    def fixture_new_password(self) -> str:
        return 'new_password'

    @pytest.fixture(name='user')
    def fixture_user(self) -> User:
        return User(email='example@gmail.com')

    @pytest.fixture(name='settings')
    def fixture_settings(self) -> PasswordSettings:
        return PasswordSettings(
            pepper='test_pepper'
        )

    @pytest.fixture(name='service')
    def fixture_service(
            self,
            settings: PasswordSettings,
            user: User,
            initial_password: str
    ) -> PasswordService:
        service = PasswordService(settings, user)
        service.set_password(initial_password)
        return service

    def test_secret_functions_called_on_random_password_generating(
            self,
            mocker: MockerFixture
    ):
        secret_function_mock = mocker.patch('secrets.choice')
        secret_function_mock.return_value = ' '

        length = 10
        PasswordService.generate_random_password(length=length)

        assert secret_function_mock.call_count == length

    def test_password_length_on_random_password_generating(self):
        length = 10
        password = PasswordService.generate_random_password(length=length)

        assert len(password) == length

    def test_secret_functions_called_on_password_change(
            self,
            mocker: MockerFixture,
            service: PasswordService,
            new_password: str
    ):
        salt_function_mock = mocker.patch('bcrypt.gensalt')
        hash_function_mock = mocker.patch('passlib.context.CryptContext.hash')

        service.set_password(new_password)

        salt_function_mock.assert_called_once()
        hash_function_mock.assert_called_once()

    def test_passwords_differ_on_password_change(
            self,
            service: PasswordService,
            new_password: str
    ):
        initial_hashed_password = service.user.hashed_password
        initial_salt = service.user.salt

        service.set_password(new_password)

        new_hashed_password = service.user.hashed_password
        new_password_salt = service.user.salt

        assert initial_hashed_password != new_hashed_password
        assert initial_salt != new_password_salt

    def test_secret_functions_called_on_password_verifying(
            self,
            mocker: MockerFixture,
            service: PasswordService,
            initial_password: str
    ):
        verify_function_mock = mocker.patch('passlib.context.CryptContext.verify')

        service.verify_password(initial_password)

        verify_function_mock.assert_called_once()

    def test_correct_result_on_password_verifying(
            self,
            service: PasswordService,
            initial_password: str,
            new_password: str
    ):
        assert service.verify_password(initial_password)
        assert not service.verify_password(new_password)

    def test_password_salting(
            self,
            service: PasswordService,
            initial_password: str
    ):
        service.user.salt = ''

        assert not service.verify_password(initial_password)

    def test_password_peppering(
            self,
            service: PasswordService,
            initial_password: str
    ):
        service.settings = PasswordSettings(pepper='')

        assert not service.verify_password(initial_password)
