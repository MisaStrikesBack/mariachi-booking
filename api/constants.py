# -*- coding: utf-8 -*-

# reservation status options
ACTIVE = "A"
CANCELLED = "C"

STATUS_OPTIONS = (
    (ACTIVE, "Activa"),
    (CANCELLED, "Cancelada")
)

HOTEL_FILTERS_DICT = {
    'country': 'address__city__country_id',
    'city': 'address__city_id'
}
