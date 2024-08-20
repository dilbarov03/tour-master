from import_export import resources, fields

from .models import UserBooking


class UserBookingResource(resources.ModelResource):
    user = fields.Field(column_name='Sotuvchi', attribute='user')
    is_bought = fields.Field(column_name='Sotib olingan', attribute='is_bought')

    class Meta:
        model = UserBooking
        fields = ('id', 'user', 'branch__name', 'region__name', 'full_name', 'tg_username', 'phone',
                  'tour__name', 'tour__category__name', 'tour__start_date',
                  'tour__barcode', 'total_price', 'is_bought', 'created_at')

    def dehydrate_user(self, user_booking):
        return user_booking.user.get_userinfo()

    def dehydrate_is_bought(self, user_booking):
        if user_booking.is_bought:
            return "Ha"
        return "Yo'q"

    def export(self, queryset=None, **kwargs):
        dataset = super().export(queryset=queryset, **kwargs)

        dataset.headers = [
            "Zayavka ID", "Sotuvchi", "Filial", "Hudud", "Mijoz", "Telegramdagi foydalanuvchi nomi", "Telefon",
            "Tur nomi", "Sayohat turi", "Boshlanish sanasi", "Shtrix kod", "Umumiy narxi", "Sotib olingan",
            "Yaratilgan vaqti"
        ]

        return dataset
