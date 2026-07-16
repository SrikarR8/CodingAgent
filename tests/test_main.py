from main import build_config


def test_build_config_includes_tool_declarations():
    system_prompt = "You are a helpful coding agent"

    config = build_config(system_prompt)

    assert config.system_instruction == system_prompt
    assert config.tools is not None
    assert len(config.tools) == 1

    tool = config.tools[0]
    assert tool.function_declarations is not None
    assert [decl.name for decl in tool.function_declarations] == [
        "get_files_info",
        "get_file_content",
        "run_python_file",
        "write_file",
    ]
