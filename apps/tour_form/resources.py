from import_export import resources, fields

from .models import TourForm


class TourFormResource(resources.ModelResource):
    user = fields.Field(column_name='Пользователь', attribute='user')
    people_count = fields.Field(column_name='Количество человек', attribute='people_count')
    status = fields.Field(column_name='Статус', attribute='status')
    answered_by = fields.Field(column_name='Менеджер', attribute='answered_by')
    answered_at = fields.Field(column_name='Ответили', attribute='answered_at')
    is_bought = fields.Field(column_name='Куплено', attribute='is_bought')

    class Meta:
        model = TourForm
        fields = ('id', 'user', 'full_name', 'region__name', 'user__branch__name', 'tour_offer__barcode', 'tour_type__name', 'country__name', 'city__name', 'from_date', 'to_date', 'room_count',
                  'holidays', 'phone', 'people_count', 'status', 'is_bought', 'created_at', 'answered_at', 'answered_by')

    def dehydrate_user(self, tour_form):
        return tour_form.user.get_userinfo()

    def dehydrate_people_count(self, tour_form):
        return tour_form.tour_people.count()

    def dehydrate_status(self, tour_form):
        return tour_form.tour_offer.status if hasattr(tour_form, 'tour_offer') else "Javob berilmagan"

    def dehydrate_answered_by(self, tour_form):
        return tour_form.tour_offer.answered_by.get_userinfo() if hasattr(tour_form, 'tour_offer') else \
            "Javob berilmagan"

    def dehydrate_answered_at(self, tour_form):
        if hasattr(tour_form, 'answered_at') and tour_form.answered_at:
            time_difference = tour_form.answered_at - tour_form.created_at
            return time_difference.total_seconds() // 60
        return "Javob berilmagan"

    def dehydrate_is_bought(self, tour_form):
        if tour_form.is_bought:
            return "Ha"
        return "Yo'q"

    def export(self, queryset=None, **kwargs):
        dataset = super().export(queryset=queryset, **kwargs)

        dataset.headers = [
            "Zayavka ID", "Sotuvchi", "Mijoz", "Hudud", "Filial", "Shtrix kod", "Sayohat turi", "Davlat", "Shahar",
            "Boshlanish sanasi", "Tugash sanasi", "Xonalar soni", "Dam olish kunlari soni", "Telefon", "Odamlar soni",
            "Status", "Sotib olingan", "Yaratilgan vaqti", "Javob berilgan", "Admin"
        ]

        return dataset

