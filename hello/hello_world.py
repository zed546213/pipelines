import os

from kfp import dsl
from kfp import compiler

# In tests, we install a KFP package from the PR under test. Users should not
# normally need to specify `kfp_package_path` in their component definitions.
_KFP_PACKAGE_PATH = os.getenv('KFP_PACKAGE_PATH')


@dsl.component(kfp_package_path=_KFP_PACKAGE_PATH)
def hello_world(text: str) -> str:
    print(text)
    return text


@dsl.pipeline(name='hello-world', description='A simple intro pipeline')
def pipeline_hello_world(text: str = 'hi there'):
    """Pipeline that passes small pipeline parameter string to consumer op."""

    consume_task = hello_world(
        text=text)  # Passing pipeline parameter as argument to consumer op


if __name__ == "__main__":
    # execute only if run as a script
    compiler.Compiler().compile(
        pipeline_func=pipeline_hello_world,
        package_path='hello_world_pipeline.json')