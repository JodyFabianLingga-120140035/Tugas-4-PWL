from pyramid.view import view_config
from .. import models
from sqlalchemy.exc import SQLAlchemyError
import json
import traceback


@view_config(route_name="musik", renderer="json", request_method="GET")
def get_musik(request):
    try:
        results = request.dbsession.query(models.Musik).all()
        return {
            "status": "success",
            "data": [
                dict(
                    id=row.id,
                    title=row.title,
                    description=row.description,
                    year=row.year,
                )
                for row in results
            ],
        }
    except SQLAlchemyError as e:
        request.response.status = 500
        return {"status": "error", "message": str(e.orig)}
    except Exception as e:
        print(traceback.format_exc())
        request.response.status = 500
        return {"status": "error", "message": str(e)}


@view_config(route_name="musik_detail", renderer="json", request_method="GET")
def get_musik_detail(request):
    try:
        query = request.dbsession.query(models.Musik)
        result = query.filter(models.Musik.id == request.matchdict["id"]).first()

        if result is None:
            request.response.status = 404
            return {"status": "error", "message": "Not Found"}

        return {
            "status": "success",
            "data": {
                "id": result.id,
                "title": result.title,
                "description": result.description,
                "year": result.year,
            },
        }
    except SQLAlchemyError as e:
        request.response.status = 500
        return {"status": "error", "message": str(e.orig)}


@view_config(
    route_name="musik_create",
    renderer="json",
    request_method="POST",
    permission="admin",
)
def create_musik(request):
    try:
        musik = models.Musik(
            title=request.json_body["title"],
            year=request.json_body["year"],
            description=request.json_body["description"],
        )
        request.dbsession.add(musik)
        return {"status": "success", "data": request.json_body}
    except SQLAlchemyError as e:
        request.response.status = 500
        return {"status": "error", "message": str(e.orig)}
    except KeyError as e:
        request.response.status = 500
        return {"status": "error", "message": str(e) + " not found"}
    except Exception as e:
        request.response.status = 500
        return {"status": "error", "message": str(e)}


@view_config(
    route_name="musik_update", renderer="json", request_method="PUT", permission="admin"
)
def update_musik(request):
    try:
        query = request.dbsession.query(models.Musik)
        musik = query.filter(models.Musik.id == request.matchdict["id"]).first()

        if musik is None:
            request.response.status = 404
            return {"status": "error", "message": "Not Found"}

        musik.title = request.json_body["title"]
        musik.description = request.json_body["description"]
        musik.year = request.json_body["year"]
        return {"status": "success", "data": request.json_body}
    except SQLAlchemyError as e:
        return {"status": "error", "message": str(e.orig)}
    except KeyError as e:
        return {"status": "error", "message": str(e) + " not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@view_config(
    route_name="musik_delete",
    renderer="json",
    request_method="DELETE",
    permission="admin",
)
def delete_musik(request):
    try:
        query = request.dbsession.query(models.Musik)
        musik = query.filter(models.Musik.id == request.matchdict["id"]).first()

        if musik is None:
            request.response.status = 404
            return {"status": "error", "message": "Not Found"}

        request.dbsession.delete(musik)
        return {"status": "success"}
    except SQLAlchemyError as e:
        return {"status": "error", "message": str(e.orig)}
    except KeyError as e:
        return {"status": "error", "message": str(e) + " not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
