import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ast

def str_to_dict(source_str):
    '''Return a dict list from a custom field string.'''

    return ast.literal_eval(source_str)

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
        # Template helper function names should begin with the name of the
        # extension they belong to, to avoid clashing with functions from
        # other extensions.
        return {'astr_to_dict': str_to_dict}
