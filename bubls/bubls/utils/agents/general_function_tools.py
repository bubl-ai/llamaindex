from llama_index.core.tools import FunctionTool


def read_code_func(path: str) -> dict:
    """Get the content of a code file.

    Args:
        path (str): Full path of the file.

    Returns:
        dict: Content of file. If the file was not found it return the
            Exception message.
    """
    try:
        with open(path, "r") as f:
            content = f.read()
            return {"file_content": content}
    except Exception as e:
        return {"error": str(e)}


read_code_tool = FunctionTool.from_defaults(
    fn=read_code_func,
    name="read_code",
    description="This tool can read the contents of code file.",
)
