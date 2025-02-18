import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Состояния для ConversationHandler
FIRST_PART, SECOND_PART, THIRD_PART, ADMIN_MODE = range(4)

# Пароль для доступа к редактированию задач
ADMIN_PASSWORD = "secretpassword"  # Твой пароль

# Тексты для задач, которые можно менять
task_1 = "Это ваша первая часть задания. Выполните её, и мы продолжим."
task_2 = "Отлично, продолжим. Выполни вторую часть задания."
task_3 = "Поздравляю! Ты завершил все задания."

# Функция для отправки фразы
def send_phrase(update, phrase):
    update.callback_query.message.reply_text(phrase)

# Начальный обработчик
def start(update, context):
    keyboard = [
        [InlineKeyboardButton("Начать", callback_data='start_task')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Привет! Нажми кнопку, чтобы начать.', reply_markup=reply_markup)
    return FIRST_PART

# Обработчик первой части задания
def first_part(update, context):
    update.callback_query.answer()
    send_phrase(update, task_1)
    return SECOND_PART

# Обработчик второй части задания
def second_part(update, context):
    update.callback_query.answer()
    send_phrase(update, task_2)
    return THIRD_PART

# Обработчик третьей части задания
def third_part(update, context):
    update.callback_query.answer()
    send_phrase(update, task_3)
    return ConversationHandler.END

# Обработчик команды для входа в админ-режим
def admin_command(update, context):
    # Проверка пароля
    if context.args and context.args[0] == ADMIN_PASSWORD:
        update.message.reply_text("Добро пожаловать в админ-режим! Вы можете изменить тексты заданий.")
        return ADMIN_MODE
    else:
        update.message.reply_text("Неверный пароль! Попробуйте снова.")
        return ConversationHandler.END

# Обработчик для изменения задач
def change_task(update, context):
    if len(context.args) < 2:
        update.message.reply_text("Пожалуйста, укажите номер задачи (1, 2, 3) и новый текст задания.")
        return ADMIN_MODE
    
    task_number = context.args[0]
    new_task_text = " ".join(context.args[1:])
    
    global task_1, task_2, task_3
    
    if task_number == '1':
        task_1 = new_task_text
        update.message.reply_text("Задание 1 обновлено.")
    elif task_number == '2':
        task_2 = new_task_text
        update.message.reply_text("Задание 2 обновлено.")
    elif task_number == '3':
        task_3 = new_task_text
        update.message.reply_text("Задание 3 обновлено.")
    else:
        update.message.reply_text("Неверный номер задачи! Используйте 1, 2 или 3.")
        return ADMIN_MODE
    
    return ADMIN_MODE

# Отмена выполнения
def cancel(update, context):
    update.message.reply_text('Выход из задания.')
    return ConversationHandler.END

# Основная функция для запуска бота
def main():
    # Вводим токен бота
    token = 'ВАШ_ТОКЕН'

    # Создаем объект Updater и передаем ему токен
    updater = Updater(token, use_context=True)
    
    # Получаем диспетчер для регистрации обработчиков
    dp = updater.dispatcher
    
    # Определяем ConversationHandler с состояниями
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FIRST_PART: [CallbackQueryHandler(first_part, pattern='^start_task$')],
            SECOND_PART: [CallbackQueryHandler(second_part)],
            THIRD_PART: [CallbackQueryHandler(third_part)],
            ADMIN_MODE: [
                CommandHandler('admin', admin_command),  # Команда для входа в админ-режим
                CommandHandler('changetask', change_task),  # Команда для изменения задания
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    
    # Регистрируем обработчик
    dp.add_handler(conversation_handler)
    
    # Запускаем бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
