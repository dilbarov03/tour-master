from import_export import resources, fields

from .models import UserBooking


class UserBookingResource(resources.ModelResource):
    user = fields.Field(column_name='Пользователь', attribute='user')

    class Meta:
        model = UserBooking
        fields = ('id', 'user', 'region__name', 'full_name', 'tg_username', 'phone',
                  'tour__name', 'tour__category__name', 'tour__start_date',
                  'tour__barcode', 'total_price', 'created_at')

    def dehydrate_user(self, user_booking):
        return user_booking.user.get_userinfo()

    def export(self, queryset=None, **kwargs):
        dataset = super().export(queryset=queryset, **kwargs)

        dataset.headers = [
            'ID', 'Кассир', 'Регион', 'Клиент', 'Username в Telegram', 'Телефон',
            'Тур', 'Категория', 'Дата начала', 'Штрихкод', 'Общая стоимость', 'Дата создания'
        ]

        return dataset
