from aiogram.fsm.state import State, StatesGroup

class AdminAddCategory(StatesGroup):
    get_name = State()
    accept = State()


class AdminAddSubCategory(StatesGroup):
    get_parent_category = State()
    get_name = State()
    accept = State()


class AdminAddProduct(StatesGroup):
    get_category = State()
    get_sub_category = State()
    get_photo = State()
    get_name = State()
    get_price = State()
    get_description = State()
    get_count = State()
    check_data = State()
    accept = State()


class AdminAddCountProduct(StatesGroup):
    get_product_id = State()
    get_count = State()
    accept = State()


class MakeOrder(StatesGroup):
    get_address = State()
    check_address = State()
    set_payment_service = State()


class MakeAnswer(StatesGroup):
    get_question = State()
    

class GetItem(StatesGroup):
    get_sub_category = State()
    select_item = State()
    select_item_on_basket = State()
    get_count = State()
    del_item = State()
    del_accept = State()
    accept = State()

