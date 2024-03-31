import aiogram
import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

# Bot token can be obtained via https://t.me/BotFather
TOKEN = '7021922965:AAFgpeUCisXYM-s6rDbzhwBtTNZ62jL0x0o'

# All handlers should be attached to the Router (or Dispatcher)
# Initialize Dispatcher instance
dp = Dispatcher()


async def check_bbr_status(chat_id: int) -> bool:
    """
    Check if BBR is already enabled
    """
    try:
        status = subprocess.check_output(['sysctl', 'net.ipv4.tcp_congestion_control']).decode('utf-8')
        return 'bbr' in status
    except subprocess.CalledProcessError as e:
        logging.error(f"Error checking BBR status: {e}")
        await bot.send_message(chat_id, 'Failed to check BBR status. Contact the bot administrator.')
        return False


async def enable_bbr(chat_id: int) -> None:
    """
    Enable BBR congestion control algorithm
    """
    try:
        if not await check_bbr_status(chat_id):
            subprocess.run(['modprobe', 'tcp_bbr'])
            with open('/etc/sysctl.conf', 'r') as f:
                if 'net.ipv4.tcp_congestion_control=bbr' not in f.read():
                    with open('/etc/sysctl.conf', 'a') as f:
                        f.write('net.core.default_qdisc=fq \nnet.ipv4.tcp_congestion_control=bbr\n')
            subprocess.run(['sysctl', '-p'])
            await bot.send_message(chat_id, 'BBR has been enabled successfully! Enjoy the better connections')
        else:
            await bot.send_message(chat_id, 'BBR is already running. No need to activate it again.')
    except Exception as e:
        logging.error(f"Error enabling BBR: {e}")
        await bot.send_message(chat_id, 'Failed to enable BBR. Contact the bot administrator.')


@dp.message_handler(commands=['enable_bbr'])
async def enable_bbr_handler(message: types.Message) -> None:
    """
    Handler for enabling BBR
    """
    chat_id = message.chat.id
    await enable_bbr(chat_id)


async def main() -> None:
    # Start polling for updates
    await dp.start_polling()


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    # Run main function asynchronously
    asyncio.run(main())
