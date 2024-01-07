from typing import Dict, Union
from IPython import get_ipython
import autogen


class IPythonUserProxyAgent(autogen.UserProxyAgent):
    
    def __init__(self, name: str, **kwargs):
        super().__init__(name, **kwargs)
        self._ipython = get_ipython()

    def generate_init_message(self, *args, **kwargs) -> Union[str, Dict]:
        return super().generate_init_message(*args, **kwargs) + """If you suggest code, the code will be executed in IPython."""

    def run_code(self, code, **kwargs):
        result = self._ipython.run_cell("%%capture --no-display cap\n" + code)
        log = self._ipython.ev("cap.stdout")
        log += self._ipython.ev("cap.stderr")
        if result.result is not None:
            log += str(result.result)
        exitcode = 0 if result.success else 1
        if result.error_before_exec is not None:
            log += f"\n{result.error_before_exec}"
            exitcode = 1
        if result.error_in_exec is not None:
            log += f"\n{result.error_in_exec}"
            exitcode = 1
        return exitcode, log, None


def get_autogen_assistant(
    llm_config1=None, 
    code_execution_config=None, 
    kernal='python', 
    config_list=None, 
    max_consecutive_auto_reply=15, 
    temperature=0, 
    cache_seed=42
):

    assistant = autogen.AssistantAgent(
        name="assistant",
        llm_config= llm_config1 or {
            "cache_seed": cache_seed, 
            "config_list": config_list, 
            "temperature": temperature, 
        },
    )
    
    if kernal == 'python':
        user_proxy = autogen.UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=max_consecutive_auto_reply,
            is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
            code_execution_config=code_execution_config or {
                "work_dir": "coding",
                "use_docker": False,  
            },
        )
        return user_proxy, assistant

    elif kernal == "ipython":
        user_proxy = IPythonUserProxyAgent(
            "ipython_user_proxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=max_consecutive_auto_reply,
            is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE") or x.get("content", "").rstrip().endswith('"TERMINATE".'),
        )
        return user_proxy, assistant
