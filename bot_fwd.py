from pyrogram import Client, filters, enums
from pyrogram.types import InputMediaPhoto, InputMediaVideo, InputMediaAnimation, LabeledPrice, ChatInviteLink
from pyrogram.enums import MessageMediaType


CANAL_ACESSO = -1002199762776

tg = Client('leite')
tg.set_parse_mode(enums.ParseMode.HTML)


@tg.on_message(filters.command('start') & filters.private)
async def start(client, message):
    preco = []
    preco.append(LabeledPrice("Acesso Imediato", 50))

    await tg.send_invoice(message.chat.id, "Acesso ao canal",
                          "Acesse o melhor canal do telegram", 'XTR', preco)


@tg.on_pre_checkout_query()
async def responde_checkout(client, message):
    await tg.answer_pre_checkout_query(message.id, True)


@tg.on_message(filters.successful_payment)
async def libera_link(client, message):
    link = await tg.create_chat_invite_link(
        CANAL_ACESSO, name="Venda Link", member_limit=1)
    link_acesso = link.invite_link
    await tg.send_message(message.chat.id, "Entre no nosso canal<br/>" + link_acesso)


@tg.on_message((filters.video | filters.photo | filters.animation) & filters.private & filters.user('@fotavares'))
async def fwd(client, message):
    media_to_send = []
    if message.media == MessageMediaType.ANIMATION:
        media_to_send.append(InputMediaAnimation(
            message.animation.file_id))
    elif message.media == MessageMediaType.VIDEO:
        media_to_send.append(InputMediaVideo(
            message.video.file_id))
    elif message.media == MessageMediaType.PHOTO:
        media_to_send.append(InputMediaPhoto(
            message.photo.file_id))

    await tg.send_media_group(CANAL_ACESSO, media=media_to_send)

    await tg.delete_messages(message.chat.id, message.id)

tg.run()
