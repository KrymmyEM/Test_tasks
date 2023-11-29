from typing import List, Optional

from sqlalchemy import BigInteger, Boolean, CheckConstraint, Column, DateTime, ForeignKeyConstraint, Identity, Index, Integer, Numeric, PrimaryKeyConstraint, SmallInteger, String, Text, UniqueConstraint
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy.orm.base import Mapped

class Base(DeclarativeBase, AsyncAttrs):
    pass

class Categories(Base):
    __tablename__ = 'categories'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='categories_pkey'),
    )

    id = mapped_column(BigInteger,
                       Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1))
    name = mapped_column(String(60), nullable=False)

    sub_categories: Mapped[List['SubCategories']] = relationship('SubCategories', uselist=True,
                                                                 back_populates='category')


class CheckChannels(Base):
    __tablename__ = 'check_channels'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='check_channels_pkey'),
        UniqueConstraint('channel_id', name='check_channels_channel_id_key')
    )

    id = mapped_column(BigInteger,
                       Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1))
    channel_id = mapped_column(Integer, nullable=False)


class CheckGroups(Base):
    __tablename__ = 'check_groups'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='check_groups_pkey'),
        UniqueConstraint('groups_id', name='check_groups_groups_id_key')
    )

    id = mapped_column(BigInteger,
                       Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1))
    groups_id = mapped_column(Integer, nullable=False)


class Maillings(Base):
    __tablename__ = 'maillings'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='maillings_pkey'),
    )

    id = mapped_column(BigInteger,
                       Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1))
    message = mapped_column(Text, nullable=False)
    get_on_send = mapped_column(Boolean, nullable=False)
    finished = mapped_column(Boolean, nullable=False)
    photo = mapped_column(String(100))


class PaymentService(Base):
    __tablename__ = 'payment_service'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='payment_service_pkey'),
    )

    id = mapped_column(BigInteger,
                       Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1))
    name = mapped_column(String(60), nullable=False)

    orders: Mapped[List['Orders']] = relationship('Orders', uselist=True, back_populates='payment')


class PaymentStatus(Base):
    __tablename__ = 'payment_status'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='payment_status_pkey'),
    )

    id = mapped_column(BigInteger,
                       Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1))
    name = mapped_column(String(60), nullable=False)

    orders: Mapped[List['Orders']] = relationship('Orders', uselist=True, back_populates='payment_status')


class Questions(Base):
    __tablename__ = 'questions'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='questions_pkey'),
    )

    id = mapped_column(BigInteger,
                       Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1))
    question = mapped_column(Text, nullable=False)
    count = mapped_column(Integer, nullable=False)
    answer = mapped_column(Text)


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='users_pkey'),
        UniqueConstraint('tg_id', name='users_tg_id_key')
    )

    id = mapped_column(BigInteger,
                       Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1))
    tg_id = mapped_column(Integer, nullable=False)
    admin = mapped_column(Boolean, nullable=False)

    addresses_deliver: Mapped[List['AddressesDeliver']] = relationship('AddressesDeliver', uselist=True,
                                                                       back_populates='user')
    baskets: Mapped[List['Baskets']] = relationship('Baskets', uselist=True, back_populates='user')


class AddressesDeliver(Base):
    __tablename__ = 'addresses_deliver'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], deferrable=True, initially='DEFERRED',
                             name='addresses_deliver_user_id_64c279db_fk_users_id'),
        PrimaryKeyConstraint('id', name='addresses_deliver_pkey'),
        Index('addresses_deliver_user_id_64c279db', 'user_id')
    )

    id = mapped_column(BigInteger,
                       Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1))
    adress = mapped_column(Text, nullable=False)
    user_id = mapped_column(BigInteger, nullable=False)

    user: Mapped['Users'] = relationship('Users', back_populates='addresses_deliver')


class Baskets(Base):
    __tablename__ = 'baskets'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], deferrable=True, initially='DEFERRED',
                             name='baskets_user_id_6ab0efdc_fk_users_id'),
        PrimaryKeyConstraint('id', name='baskets_pkey'),
        Index('baskets_user_id_6ab0efdc', 'user_id')
    )

    id = mapped_column(BigInteger,
                       Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1))
    sell = mapped_column(Boolean, nullable=False)
    user_id = mapped_column(BigInteger, nullable=False)

    user: Mapped['Users'] = relationship('Users', back_populates='baskets')
    orders: Mapped[List['Orders']] = relationship('Orders', uselist=True, back_populates='basket')
    basket_items: Mapped[List['BasketItems']] = relationship('BasketItems', uselist=True, back_populates='basket')


class SubCategories(Base):
    __tablename__ = 'sub_categories'
    __table_args__ = (
        ForeignKeyConstraint(['category_id'], ['categories.id'], deferrable=True, initially='DEFERRED',
                             name='sub_categories_category_id_dc42080e_fk_categories_id'),
        PrimaryKeyConstraint('id', name='sub_categories_pkey'),
        Index('sub_categories_category_id_dc42080e', 'category_id')
    )

    id = mapped_column(BigInteger,
                       Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1))
    name = mapped_column(String(60), nullable=False)
    category_id = mapped_column(BigInteger, nullable=False)

    category: Mapped['Categories'] = relationship('Categories', back_populates='sub_categories')
    items: Mapped[List['Items']] = relationship('Items', uselist=True, back_populates='sub_category')


class Items(Base):
    __tablename__ = 'items'
    __table_args__ = (
        ForeignKeyConstraint(['sub_category_id'], ['sub_categories.id'], deferrable=True, initially='DEFERRED',
                             name='items_sub_category_id_4591461b_fk_sub_categories_id'),
        PrimaryKeyConstraint('id', name='items_pkey'),
        Index('items_sub_category_id_4591461b', 'sub_category_id')
    )

    id = mapped_column(BigInteger,
                       Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1))
    photo = mapped_column(String(100), nullable=False)
    name = mapped_column(String(100), nullable=False)
    count = mapped_column(Integer, nullable=False)
    description = mapped_column(String(500), nullable=False)
    price = mapped_column(Numeric(8, 2), nullable=False)
    sub_category_id = mapped_column(BigInteger, nullable=False)

    sub_category: Mapped['SubCategories'] = relationship('SubCategories', back_populates='items')
    basket_items: Mapped[List['BasketItems']] = relationship('BasketItems', uselist=True, back_populates='item')


class Orders(Base):
    __tablename__ = 'orders'
    __table_args__ = (
        ForeignKeyConstraint(['basket_id'], ['baskets.id'], deferrable=True, initially='DEFERRED',
                             name='orders_basket_id_d41bfc7d_fk_baskets_id'),
        ForeignKeyConstraint(['payment_id'], ['payment_service.id'], deferrable=True, initially='DEFERRED',
                             name='orders_payment_id_85bb124e_fk_payment_service_id'),
        ForeignKeyConstraint(['payment_status_id'], ['payment_status.id'], deferrable=True, initially='DEFERRED',
                             name='orders_payment_status_id_4cf0e3c2_fk_payment_status_id'),
        PrimaryKeyConstraint('order_id', name='orders_pkey'),
        Index('orders_basket_id_d41bfc7d', 'basket_id'),
        Index('orders_order_id_5fe90b5c_like', 'order_id'),
        Index('orders_payment_id_85bb124e', 'payment_id'),
        Index('orders_payment_status_id_4cf0e3c2', 'payment_status_id')
    )

    order_id = mapped_column(String(55))
    address_deliver = mapped_column(Text, nullable=False)
    price = mapped_column(Numeric(10, 2), nullable=False)
    created_at = mapped_column(DateTime(True), nullable=False)
    basket_id = mapped_column(BigInteger, nullable=False)
    payment_service_data = mapped_column(Text)
    payment_id = mapped_column(BigInteger)
    payment_status_id = mapped_column(BigInteger)

    basket: Mapped['Baskets'] = relationship('Baskets', back_populates='orders')
    payment: Mapped[Optional['PaymentService']] = relationship('PaymentService', back_populates='orders')
    payment_status: Mapped[Optional['PaymentStatus']] = relationship('PaymentStatus', back_populates='orders')


class BasketItems(Base):
    __tablename__ = 'basket_items'
    __table_args__ = (
        ForeignKeyConstraint(['basket_id'], ['baskets.id'], deferrable=True, initially='DEFERRED',
                             name='basket_items_basket_id_2b854602_fk_baskets_id'),
        ForeignKeyConstraint(['item_id'], ['items.id'], deferrable=True, initially='DEFERRED',
                             name='basket_items_item_id_408d3201_fk_items_id'),
        PrimaryKeyConstraint('id', name='basket_items_pkey'),
        Index('basket_items_basket_id_2b854602', 'basket_id'),
        Index('basket_items_item_id_408d3201', 'item_id')
    )

    id = mapped_column(BigInteger,
                       Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1))
    count = mapped_column(Integer, nullable=False)
    basket_id = mapped_column(BigInteger, nullable=False)
    item_id = mapped_column(BigInteger, nullable=False)

    basket: Mapped['Baskets'] = relationship('Baskets', back_populates='basket_items')
    item: Mapped['Items'] = relationship('Items', back_populates='basket_items')

