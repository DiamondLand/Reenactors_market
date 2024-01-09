def send_product_card(name: str, description: str, price: int, prev_send: bool,
                            category: str = None, subcategory: str = None, subsubcategory: str = None, 
                            company_name: str = None):
    
    if prev_send is False:
        send_product_card_text = f"<b>{name.capitalize()}</b>\
        \n\n📝 <b>Описание:</b> <i>{description}</i>\
        \n🪙 <b>Стоимость:</b> <i>{price}</i>\
        \n😉 <b>Продавец:</b> <i>{company_name}</i>"
    else:
        send_product_card_text = f"<b>{name.capitalize()}</b>\
        \n\n➡️ <b>Описание:</b> <i>{description}</i>\
        \n➡️ <b>Стоимость:</b> <i>{price}₽</i>\
        \n➡️ <b>Категория:</b> <i>{category}</i>\
        \n➡️ <b>Подкатегория:</b> <i>{subcategory}</i>\
        \n➡️ <b>Подподкатегория:</b> <i>{subsubcategory}</i>"


    return send_product_card_text