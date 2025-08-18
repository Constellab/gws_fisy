from gws_core import (ConfigParams, AppConfig, AppType, OutputSpec,
                      OutputSpecs, ReflexResource, Task, TaskInputs,
                      TaskOutputs, app_decorator, task_decorator,
                      InputSpecs, ConfigSpecs, StrParam, FloatParam, IntParam)


@app_decorator("FisyAppConfig", app_type=AppType.REFLEX,
               human_name="Generate FisyApp app")
class FisyAppConfig(AppConfig):

    # retrieve the path of the app folder, relative to this file
    # the app code folder starts with a underscore to avoid being loaded when the brick is loaded
    def get_app_folder_path(self):
        return self.get_app_folder_from_relative_path(__file__, "_fisy_app")


@task_decorator("GenerateFisyApp", human_name="Generate FisyApp app",
                style=ReflexResource.copy_style())
class GenerateFisyApp(Task):
    input_specs = InputSpecs({})
    output_specs = OutputSpecs({'reflex_app': OutputSpec(ReflexResource)})
    config_specs = ConfigSpecs({
        'app_title': StrParam(default_value="FISY — App"),
        'corporate_tax_rate': FloatParam(default_value=0.25),
        'months': IntParam(default_value=36)
    })

    def run(self, params: ConfigParams, inputs: TaskInputs) -> TaskOutputs:
        app = ReflexResource()
        app.set_param('app_title', params.get('app_title', 'FISY — App'))
        app.set_param('corporate_tax_rate', params.get('corporate_tax_rate', 0.25))
        app.set_param('months', params.get('months', 36))
        app.set_app_config(FisyAppConfig())
        app.set_requires_authentication(False)
        app.set_name("Fisy App")
        return {'reflex_app': app}
