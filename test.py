import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import json
from ВОТ import SettingsHandler, WeatherHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton  # Импортируем для создания mock-объектов


@pytest.mark.asyncio
@patch("builtins.open", new_callable=MagicMock)
async def test_start(mock_open):
    settings_handler = SettingsHandler()
    mock_update = AsyncMock()
    mock_update.effective_user.first_name = "TestUser"  # Устанавливаем mock имя
    mock_context = MagicMock()

    # Подготавливаем mock для файла
    mock_open.return_value.__enter__.return_value.read.return_value = json.dumps({})

    # Вызываем метод start
    await settings_handler.start(mock_update, mock_context)

    # Проверяем, что сообщение отправлено пользователю
    mock_update.message.reply_text.assert_called_with(
        "Привет, TestUser! Вы добавлены в систему.\nКоманда /weather для погоды, а /settings для настройки городов."
    )


@pytest.mark.asyncio
@patch("builtins.open", new_callable=MagicMock)
async def test_settings(mock_open):
    settings_handler = SettingsHandler()
    mock_update = AsyncMock()
    mock_update.effective_user.id = "12345"  # Добавляем user ID
    mock_context = MagicMock()

    # Подготавливаем mock данных
    mock_open.return_value.__enter__.return_value.read.return_value = json.dumps({
        "12345": {"name": "TestUser", "cities": ["City1", "City2", "City3"]}
    })

    # Ожидаемый reply_markup
    expected_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="City1")],
            [KeyboardButton(text="City2")],
            [KeyboardButton(text="City3")],
        ],
        one_time_keyboard=True,
        resize_keyboard=True,
    )

    # Вызываем метод settings
    await settings_handler.settings(mock_update, mock_context)

    # Проверяем, что пользователю отправлено сообщение с правильными параметрами
    mock_update.message.reply_text.assert_called_with(
        "Выберите ячейку для изменения:", reply_markup=expected_keyboard
    )

@pytest.mark.asyncio
@patch("selenium.webdriver.Chrome")
async def test_weather(mock_driver):
    weather_handler = WeatherHandler()
    mock_update = AsyncMock()
    mock_context = MagicMock()

    # Настройка mock для Selenium WebDriver
    driver_mock = mock_driver.return_value
    driver_mock.get = MagicMock()
    driver_mock.find_element.return_value.text = "Mocked data"

    # Вызываем метод weather
    await weather_handler.fetch_weather(mock_update, mock_context)

    # Проверяем, что пользователю отправлено сообщение
    mock_update.message.reply_text.assert_called_with(
        "Текущая температура в Mocked data: Mocked data°C\nОщущается как: Mocked data°C\nУсловия: Mocked data"
    )
