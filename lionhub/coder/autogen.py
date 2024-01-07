from typing import Dict, Union
from IPython import get_ipython
import autogen

config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": [
            "gpt-4", "gpt-4-0314", "gpt4", "gpt-4-32k", 
            "gpt-4-32k-0314", "gpt-4-32k-v0314", "gpt-4-1106-preview"
            ],
    },
)


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


def get_autogen_assistant(llm_config1=None, code_execution_config=None, kernal='python'):

    assistant = autogen.AssistantAgent(
        name="assistant",
        llm_config= llm_config1 or {
            "cache_seed": 42, 
            "config_list": config_list, 
            "temperature": 0, 
        },
    )
    
    if kernal == 'python':
        user_proxy = autogen.UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=10,
            is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
            code_execution_config=code_execution_config or {
                "work_dir": "coding",
                "use_docker": False,  
            },
        )
        return assistant, user_proxy

    elif kernal == "ipython":
        user_proxy = IPythonUserProxyAgent(
            "ipython_user_proxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=10,
            is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE") or x.get("content", "").rstrip().endswith('"TERMINATE".'),
        )
        return assistant, user_proxy


def auto_coder(task, llm_config1=None, code_execution_config=None, kernal="python"):
    assistant, user_proxy = get_autogen_assistant(
        llm_config1=llm_config1, code_execution_config=code_execution_config, kernal=kernal
    )

    user_proxy.initiate_chat(
        assistant,
        message=f"""{task}""",
    )
    
    return user_proxy.chat_messages
