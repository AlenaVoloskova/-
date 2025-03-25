from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy_garden.mapview import MapView, MapMarkerPopup
import geocoder

# Глобальная переменная для хранения статуса GPS
gps_status = False

# Получение геолокации с использованием geocoder
def get_location():
    try:
        
        g = geocoder.ip('me')  # Определение местоположения по IP
        return g.latlng
    except Exception as e:
        print(f"Ошибка при получении геолокации: {e}")
        return None

# Обработчик получения координат и возвращение значений
def on_location():
    global gps_status
    if not gps_status: 
        return

    location = get_location() # (0.00124, 0.1258192) адрес IP
    if location:
        latitude, longitude = location
        app.update_map(latitude, longitude)

class GeoLocationApp(App):
    def build(self):
        # Установка белого фона с помощью контейнера(функции build(self))
        self.background_color = (1, 1, 1, 1)  

        # Главный контейнер
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        
        self.status_label = Label(text="Можно ли отслеживать вашу геолокацию?", size_hint=(1, 0.1))
        self.layout.add_widget(self.status_label)

        
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=10)
        self.yes_button = Button(text="Да", on_press=self.enable_gps)
        self.no_button = Button(text="Нет", on_press=self.disable_gps)
        button_layout.add_widget(self.yes_button)
        button_layout.add_widget(self.no_button)
        self.layout.add_widget(button_layout)

        
        self.map_view = MapView(zoom=15, lat=55.751244, lon=37.618423)  # Начальные координаты (Москва), если возникнет ошибка при получении IP
        self.map_view.size_hint = (1, 0.8)
        self.map_view.opacity = 0  
        self.layout.add_widget(self.map_view)

        # Список маркеров (глобальная переменная)
        self.markers = []

        return self.layout

    def enable_gps(self, instance):
        global gps_status
        
        location = get_location()
        if location:
            gps_status = True
            latitude, longitude = location
            self.status_label.text = "Геолокация включена."
            self.map_view.opacity = 1 
            self.update_map(latitude, longitude)
        else:
            gps_status = False
            self.status_label.text = "Не удалось получить геолокацию."

    def disable_gps(self, instance):
        global gps_status
        gps_status = False
        self.status_label.text = "Геолокация отключена."
        self.map_view.opacity = 0  

    def update_map(self, latitude, longitude):
        # Очистка старых маркеров(проходится по всему списку маркеров)
        self.clear_markers()

        
        self.current_marker = MapMarkerPopup(lat=latitude, lon=longitude, source="profile.png")
        self.current_marker.add_widget(Label(text="Ваше местоположение"))
        self.map_view.add_marker(self.current_marker)
        self.markers.append(self.current_marker)  # Добавляем маркер в список

        
        self.map_view.center_on(latitude, longitude)

        
        self.add_nearby_places(latitude, longitude)

    def clear_markers(self):
        
        for marker in self.markers:
            self.map_view.remove_marker(marker)
        self.markers.clear()

    def add_nearby_places(self, latitude, longitude):
        
        nearby_places = [
            {"name": "Парк Горького", "lat": latitude + 0.005, "lon": longitude + 0.005, "rating": "4.5/5"},
            {"name": "Кафе 'Счастье'", "lat": latitude - 0.003, "lon": longitude + 0.002, "rating": "4.2/5"},
            {"name": "Ресторан 'Вкусно'", "lat": latitude + 0.005, "lon": longitude - 0.001, "rating": "4.7/5"},
        ]

        
        for place in nearby_places:
            marker = MapMarkerPopup(lat=place["lat"], lon=place["lon"])
            marker.add_widget(Label(text=f"{place['name']}\nРейтинг: {place['rating']}"))
            self.map_view.add_marker(marker)
            self.markers.append(marker)  

    def on_stop(self):
        
        pass  

GeoLocationApp().run()