from aiogram.filters.callback_data import CallbackData


class CatalogeCallBack(CallbackData, prefix="cat"):
    type_cat: str
    id_cat: int


class ItemCallback(CallbackData, prefix="item"):
    action_type: str
    item_id: int = 0
    basket_item_id: int = 0


class PaymentCallBack(CallbackData, prefix="pay"):
    status: str
    payment_service: int
    order_id: str


class QuestionsCallBack(CallbackData, prefix="quest"):
    act: str
    quest_id: int