import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ast
import json

def str_to_dict(source_str):
    '''Return a dict list from a custom field string.'''

    return ast.literal_eval(source_str)

def freq_to_text(update_freq):
    '''Return a dict list from a custom field string.'''

    upds = {
        'R/P10Y': 'Cada diez años',
        'R/P4Y': 'Cada cuatro años',
        'R/P3Y': 'Cada tres años',
        'R/P2Y': 'Cada dos años',
        'R/P1Y': 'Anualmente',
        'R/P6M': 'Cada medio año',
        'R/P4M': 'Cuatrimestralmente',
        'R/P3M': 'Trimestralmente',
        'R/P2M': 'Bimestralmente',
        'R/P1M': 'Mensualmente',
        'R/P0.5M': 'Cada 15 días',
        'R/P0.33M': 'Tres veces por mes',
        'R/P1W': 'Semanalmente',
        'R/P0.5W': 'Dos veces a la semana',
        'R/P0.33W': 'Tres veces a la semana',
        'R/P1D': 'Diariamente',
        'R/PT1H': 'Cada hora',
        'R/PT1S': 'Continuamente actualizado',
        'eventual': 'Eventual'
    }

    return upds[update_freq]

def json_loads(json_string):
    return json.loads(json_string)

def field_types():
    types = [
        ("string", u"Texto (string)"),
        ("integer", u"Número entero (integer)"),
        ("number", u"Número decimal (number)"),
        ("boolean", u"Verdadero/falso (boolean)"),
        ("time", u"Tiempo ISO-8601 (time)"),
        ("date", u"Fecha ISO-8601 (date)"),
        ("date-time", u"Fecha y hora ISO-8601 (date-time)"),
        ("object", u"JSON (object)"),
        ("geojson", u"GeoJSON (geojson)"),
        ("geo_point", u"GeoPoint (geo_point)"),
        ("array", u"Lista de valores en formato JSON (array)"),
        ("binary", u"Valor binario en base64 (binary)"),
        ("any", u"Otro (any)")
    ]

    # if field_type_id:
    #     filtered_field_type = [t for t in types if t[0] == field_type_id]
    #     if filtered_field_type:
    #         return filtered_field_type[0]
    #     return None

    return types

class MdsThemePlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IDatasetForm)


    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')

    def get_helpers(self):
        '''Register the most_popular_groups() function above as a template
        helper function.

        '''
        return {
            'astr_to_dict': str_to_dict, 
            'freq_to_text': freq_to_text, 
            'json_loads': json_loads,
            'field_types': field_types
            }

    def _modify_package_schema(self, schema):
        schema.update({
            'super_theme': [toolkit.get_converter('convert_to_extras'),
                            toolkit.get_validator('ignore_missing')]
        })
        schema.update({
            'update_frequency': [toolkit.get_converter('convert_to_extras'),
                            toolkit.get_validator('ignore_missing')]
        })
        schema['resources'].update({
                'file_fields_dict' : [ toolkit.get_validator('ignore_missing') ]
        })
        return schema

    def create_package_schema(self):
        schema = super(MdsThemePlugin, self).create_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def update_package_schema(self):
        schema = super(MdsThemePlugin, self).update_package_schema()
        schema = self._modify_package_schema(schema)
        return schema


    def show_package_schema(self):
        schema = super(MdsThemePlugin, self).show_package_schema()
        schema.update({
            'super_theme': [toolkit.get_converter('convert_from_extras'),
                            toolkit.get_validator('ignore_missing')]
        })
        schema.update({
            'update_frequency': [toolkit.get_converter('convert_from_extras'),
                            toolkit.get_validator('ignore_missing')]
        })
        schema['resources'].update({
                'file_fields_dict' : [ toolkit.get_validator('ignore_missing') ]
        })
        return schema

    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return True

    def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []