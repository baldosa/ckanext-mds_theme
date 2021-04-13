import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ast

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


class MdsThemePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')

    def get_helpers(self):
        '''Register the most_popular_groups() function above as a template
        helper function.

        '''
        return {'astr_to_dict': str_to_dict, 'freq_to_text': freq_to_text}

