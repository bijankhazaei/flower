from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
import markdown
from pathlib import Path

router = APIRouter(prefix="/docs", tags=["documentation"])

@router.get("/", response_class=HTMLResponse)
async def get_documentation_index():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Flower Documentation</title>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; margin: 40px; }
            .nav { background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
            .nav a { margin-right: 20px; text-decoration: none; color: #007bff; }
        </style>
    </head>
    <body>
        <div class="nav">
            <h1>🌸 Flower Documentation</h1>
            <a href="/docs/overview">Project Overview</a>
            <a href="/docs/documentation">Full Documentation</a>
            <a href="/docs/readme">README</a>
        </div>
        <div>
            <h2>Welcome to Flower</h2>
            <p>A next-generation visual flow builder built with FastAPI and Porto architecture.</p>
        </div>
    </body>
    </html>
    """
    return html

@router.get("/{doc_name}", response_class=HTMLResponse)
async def get_documentation(doc_name: str):
    doc_files = {
        "overview": ".amazonq/rules/project_overview.md",
        "documentation": ".amazonq/rules/project_documention.md",
        "readme": "README.md",
        "project": "PROJECT_DOCUMENTATION.md"
    }
    
    if doc_name not in doc_files:
        raise HTTPException(status_code=404, detail="Documentation not found")
    
    file_path = Path(__file__).parent.parent.parent.parent.parent.parent / doc_files[doc_name]
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    html_content = markdown.markdown(content, extensions=['codehilite', 'toc'])
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Flower - {doc_name.title()}</title>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif; margin: 0; }}
            .header {{ background: #f8f9fa; padding: 20px; border-bottom: 1px solid #dee2e6; }}
            .header a {{ margin-right: 20px; text-decoration: none; color: #007bff; }}
            .content {{ max-width: 800px; margin: 40px auto; padding: 0 20px; }}
            pre {{ background: #f8f9fa; padding: 15px; border-radius: 5px; overflow-x: auto; }}
            code {{ background: #f8f9fa; padding: 2px 4px; border-radius: 3px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <a href="/docs/">🌸 Home</a>
            <a href="/docs/overview">Overview</a>
            <a href="/docs/documentation">Documentation</a>
            <a href="/docs/readme">README</a>
        </div>
        <div class="content">
            {html_content}
        </div>
    </body>
    </html>
    """
    return html