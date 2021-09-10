from logging import error
from flask import Flask, request, jsonify
from app.services import Serie
from app.services import create_table

def routes_views(app: Flask):


    @app.post('/series')
    def create():
        
        create_table()
        
        try:
            data = request.get_json()
            Serie.create_serie(data)
            return jsonify(Serie.return_serie_created(data)), 201
        except:
            return {'error': 'Serie not created!'}, 400

    
    @app.get('/series')
    def series():
        
        try:
            data = Serie.show_all_series()
            return jsonify(data), 200
        except:
            create_table()
            return {"data": []}, 200

    
    @app.get('/series/<int:serie_id>')
    def select_by_id(serie_id: int):
        
        data = Serie.show_specific_serie(serie_id)

        try:
            return jsonify(data), 200
        except TypeError:
            create_table()
            return {'error': 'Serie not found!'}, 404
        except serie_id == None:
            return {'error': 'Serie not found!'}, 404
        except:
            create_table()
            return {'error': 'Table has just been created!'}, 404
    