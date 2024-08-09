from import_export import resources, fields

from .models import TourForm


class TourFormResource(resources.ModelResource):
    user = fields.Field(column_name='Пользователь', attribute='user')
    people_count = fields.Field(column_name='Количество человек', attribute='people_count')
    status = fields.Field(column_name='Статус', attribute='status')
    answered_by = fields.Field(column_name='Менеджер', attribute='answered_by')
    answered_at = fields.Field(column_name='Ответили', attribute='answered_at')

    class Meta:
        model = TourForm
        fields = ('id', 'user', 'region__name', 'tour_type__name', 'country__name', 'city__name', 'from_date', 'to_date', 'room_count',
                  'holidays', 'phone', 'people_count', 'status', 'created_at', 'answered_at', 'answered_by')

    def dehydrate_user(self, tour_form):
        return tour_form.user.get_userinfo()

    def dehydrate_people_count(self, tour_form):
        return tour_form.tour_people.count()

    def dehydrate_status(self, tour_form):
        return tour_form.tour_offer.status if hasattr(tour_form, 'tour_offer') else "Не отвечено"

    def dehydrate_answered_by(self, tour_form):
        return tour_form.tour_offer.answered_by.get_userinfo() if hasattr(tour_form, 'tour_offer') else "Не отвечено"

    def dehydrate_answered_at(self, tour_form):
        if hasattr(tour_form, 'answered_at') and tour_form.answered_at:
            time_difference = tour_form.answered_at - tour_form.created_at
            return time_difference.total_seconds() // 60
        return "Не отвечено"


    def export(self, queryset=None, **kwargs):
        dataset = super().export(queryset=queryset, **kwargs)

        dataset.headers = [
            'ID', 'Пользователь', 'Регион', 'Тип тура', 'Страна', 'Город', 'Дата начала', 'Дата окончания',
            'Количество комнат', 'Количество дней отдыха', 'Телефон', 'Количество человек', 'Статус', 'Создано',
            'Ответили', 'Менеджер'
        ]

        return dataset

