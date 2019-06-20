from flask_restful.inputs import boolean
from flask_restful.reqparse import Argument
from app.common import boilerplate


from flask import current_app, request
import flask_restful as restful
from flask_restful import abort, fields, marshal,marshal_with
from flask_restful import reqparse
from app.common.auth import is_authenticated
from app.common.response_templates import CTTVResponse
import time

__author__ = 'gkos-bio'

class Datasets(restful.Resource):

    @is_authenticated
    def get(self):
        """
        Given a dataset name and an ES query, returns all documents from this dataset
        """
        es = current_app.extensions['esquery']
        parser = boilerplate.get_parser()

        parser.add_argument('dataset', type=str, required=True, help="name of the dataset")
        parser.add_argument('query', type=str, required=True, help="query to retrieve data in ES format")

        args = parser.parse_args()

        dataset_name = args.get('dataset', '')
        print("get ", dataset_name)
        es_query = args.get('query', '')
        if not es_query:
            abort(404, message='No query specified in the request')
        res = es.get_documents_from_dataset(dataset_name, es_query)

        if not res:
            abort(404, message='Cannot find documents for dataset %s'%str(dataset_name))
        return CTTVResponse.OK(res)

    @is_authenticated
    def post(self):
        """
        Given a list of subjects id, returns related entities
        """
        es = current_app.extensions['esquery']
        parser = boilerplate.get_parser()

        parser.add_argument('dataset', type=str, required=True, help="name of the dataset")
        parser.add_argument('query', type=str, required=True, help="query to retrieve data in ES format")

        args = parser.parse_args()
        dataset_name = args.get('dataset', '')
        print("post ", dataset_name)
        es_query = args.get('query', '')
        if not es_query:
            abort(404, message='No query specified in the request')

        res = es.get_documents_from_dataset(dataset_name, es_query)

        if not res:
            abort(404, message='Cannot find relations for id %s'%str(subjects))
        return CTTVResponse.OK(res)



class DatasetList(restful.Resource):

    @is_authenticated
    def get(self):
        """
        Get a list of datasets stored in our back-end
        """
        es = current_app.extensions['esquery']
        res = es.get_dataset_list()
        if not res:
            abort(404, message='Cannot retrieve datasets')
        return CTTVResponse.OK(res)