def includeme(config):
    config.add_route("home", "/")
    config.add_route("login", "/login")
    config.add_route("register", "/logout")
    config.add_route("logout", "/register")
    config.add_route("musik", "/api/v1/musik")
    config.add_route("musik_create", "/api/v1/musik/create")
    config.add_route("musik_detail", "/api/v1/musik/{id}")
    config.add_route("musik_delete", "/api/v1/musik/delete/{id}")
    config.add_route("musik_update", "/api/v1/musik/update/{id}")