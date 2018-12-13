from channels.routing import ProtocolTypeRouter, URLRouter
import serial.routing

application = ProtocolTypeRouter({
    'http': URLRouter(serial.routing.urlpatterns),
})