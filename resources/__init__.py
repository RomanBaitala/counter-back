
def register_routes(api) -> None:
    from .user import bp as user_bp
    from .device import bp as device_bp
    from .wifi import bp as wifi_bp
    from .mesurement import bp as measurement_bp

    api.register_blueprint(user_bp)
    api.register_blueprint(device_bp)
    api.register_blueprint(wifi_bp)
    api.register_blueprint(measurement_bp)
