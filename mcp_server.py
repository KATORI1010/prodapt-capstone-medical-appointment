from fastmcp import FastMCP

from db import get_db_session
from models import JobPost

mcp = FastMCP("TEST MCP Server")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two integers together.

    Args:
        a: First integer
        b: Second integer

    Returns:
        The sum of a and b
    """
    return a + b


@mcp.tool()
def mul(a: int, b: int) -> int:
    """Add two integers together.

    Args:
        a: First integer
        b: Second integer

    Returns:
        The multiple of a and b
    """
    return a * b


@mcp.tool()
def get_job_post_by_id(job_post_id: int) -> dict:
    """Get Job Post Data by ID.

    Args:
        job_post_id: Job Post ID
        b: Second integer

    Returns:
        The dict data of job post
    """
    with get_db_session() as db:
        job_post = db.get(JobPost, job_post_id)
        return {
            "id": job_post.id,
            "title": job_post.title,
            "description": job_post.description,
        }


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="127.0.0.1", port=9000)
