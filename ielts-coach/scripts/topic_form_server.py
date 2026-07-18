#!/usr/bin/env python3
"""
IELTS Coach - Topic Discovery Form Server

A local server that serves an HTML form for Topic Discovery.
Users fill in their answers in the browser, and the server saves
the responses to a JSON file for the agent to read.

Usage:
    python topic_form_server.py --questions questions.json [--port 8765]

Questions JSON format:
{
    "topic": "Topic Name",
    "questions": [
        {"id": "q1", "question": "What is your favourite food?", "type": "textarea"},
        {"id": "q2", "question": "Do you prefer online shopping?", "type": "radio", "options": ["Yes", "No", "Both"]}
    ]
}

The server saves answers to: topic_form_answers.json (in current directory)
"""

import http.server
import json
import os
import sys
import webbrowser
import argparse
import threading
from urllib.parse import parse_qs

# Default port
DEFAULT_PORT = 8765

# HTML Form Template
FORM_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IELTS Coach - Topic Discovery</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}

        body {{
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 2rem;
        }}

        .container {{
            max-width: 800px;
            margin: 0 auto;
        }}

        .header {{
            background: rgba(255,255,255,0.95);
            border-radius: 16px;
            padding: 2rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }}

        .header h1 {{
            color: #1a237e;
            font-size: 1.5rem;
            margin-bottom: 0.5rem;
        }}

        .header p {{
            color: #666;
            font-size: 0.9rem;
        }}

        .topic-badge {{
            display: inline-block;
            background: linear-gradient(135deg, #1a237e, #283593);
            color: white;
            padding: 0.3rem 1rem;
            border-radius: 99px;
            font-size: 0.85rem;
            font-weight: 600;
            margin-top: 0.8rem;
        }}

        .form-card {{
            background: rgba(255,255,255,0.95);
            border-radius: 16px;
            padding: 2rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }}

        .question-group {{
            margin-bottom: 1.5rem;
            padding-bottom: 1.5rem;
            border-bottom: 1px solid #e0e0e0;
        }}

        .question-group:last-of-type {{
            border-bottom: none;
            margin-bottom: 0;
            padding-bottom: 0;
        }}

        .question-label {{
            font-weight: 600;
            color: #1a237e;
            font-size: 1rem;
            margin-bottom: 0.8rem;
            display: flex;
            align-items: flex-start;
            gap: 0.5rem;
        }}

        .question-number {{
            background: #1a237e;
            color: white;
            width: 24px;
            height: 24px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.75rem;
            flex-shrink: 0;
            margin-top: 2px;
        }}

        textarea {{
            width: 100%;
            padding: 0.8rem 1rem;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 0.95rem;
            font-family: inherit;
            resize: vertical;
            min-height: 80px;
            transition: border-color 0.2s;
        }}

        textarea:focus {{
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102,126,234,0.2);
        }}

        .radio-group {{
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
        }}

        .radio-option {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s;
        }}

        .radio-option:hover {{
            border-color: #667eea;
            background: rgba(102,126,234,0.05);
        }}

        .radio-option input[type="radio"] {{
            accent-color: #667eea;
        }}

        .radio-option.selected {{
            border-color: #667eea;
            background: rgba(102,126,234,0.1);
        }}

        .submit-section {{
            text-align: center;
            margin-top: 1rem;
        }}

        .submit-btn {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 1rem 3rem;
            border-radius: 99px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: 0 4px 15px rgba(102,126,234,0.4);
        }}

        .submit-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102,126,234,0.5);
        }}

        .submit-btn:active {{
            transform: translateY(0);
        }}

        .progress-bar {{
            background: #e0e0e0;
            height: 4px;
            border-radius: 99px;
            margin-bottom: 1.5rem;
            overflow: hidden;
        }}

        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            border-radius: 99px;
            transition: width 0.3s ease;
        }}

        .tip {{
            background: #e8f5e9;
            border-left: 4px solid #4caf50;
            padding: 0.8rem 1rem;
            border-radius: 0 8px 8px 0;
            margin-bottom: 1rem;
            font-size: 0.85rem;
            color: #2e7d32;
        }}

        .tip::before {{
            content: "💡 Tip: ";
            font-weight: 700;
        }}

        /* Success page */
        .success-page {{
            text-align: center;
            padding: 3rem 2rem;
        }}

        .success-icon {{
            font-size: 4rem;
            margin-bottom: 1rem;
        }}

        .success-page h2 {{
            color: #2e7d32;
            margin-bottom: 0.5rem;
        }}

        .success-page p {{
            color: #666;
            font-size: 1rem;
        }}

        @media (max-width: 600px) {{
            body {{ padding: 1rem; }}
            .header, .form-card {{ padding: 1.2rem; }}
            .radio-group {{ flex-direction: column; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎓 IELTS Coach</h1>
            <p>请回答以下问题，帮助我为你生成个性化的模型答案。</p>
            <div class="topic-badge">{topic}</div>
        </div>

        <form id="topicForm" action="/submit" method="POST">
            <div class="form-card">
                <div class="tip">请尽可能详细地回答，你的回答越具体，生成的答案就越个性化、越容易记忆。</div>

                {questions_html}
            </div>

            <div class="submit-section">
                <button type="submit" class="submit-btn">✓ 提交我的回答</button>
            </div>
        </form>
    </div>

    <script>
        // Update progress bar as user types
        const textareas = document.querySelectorAll('textarea');
        const progressFill = document.querySelector('.progress-fill');
        const totalQuestions = textareas.length;

        function updateProgress() {{
            let filled = 0;
            textareas.forEach(ta => {{
                if (ta.value.trim().length > 0) filled++;
            }});
            const pct = totalQuestions > 0 ? (filled / totalQuestions) * 100 : 0;
            progressFill.style.width = pct + '%';
        }}

        textareas.forEach(ta => {{
            ta.addEventListener('input', updateProgress);
        }});

        // Auto-resize textareas
        textareas.forEach(ta => {{
            ta.addEventListener('input', function() {{
                this.style.height = 'auto';
                this.style.height = Math.max(80, this.scrollHeight) + 'px';
            }});
        }});

        // Form submission
        document.getElementById('topicForm').addEventListener('submit', function(e) {{
            e.preventDefault();
            const formData = new FormData(this);
            const data = {{}};
            for (let [key, value] of formData.entries()) {{
                data[key] = value;
            }}

            fetch('/submit', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify(data)
            }}).then(response => response.json()).then(result => {{
                if (result.success) {{
                    document.querySelector('.container').innerHTML = `
                        <div class="form-card success-page">
                            <div class="success-icon">✅</div>
                            <h2>提交成功！</h2>
                            <p>你的回答已保存。请回到 CLI 查看生成的答案。</p>
                        </div>
                    `;
                }}
            }});
        }});
    </script>
</body>
</html>"""

SUCCESS_html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>提交成功</title>
    <style>
        body {{
            font-family: 'Segoe UI', system-ui, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .card {{
            background: white;
            border-radius: 16px;
            padding: 3rem;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }}
        .icon {{ font-size: 4rem; margin-bottom: 1rem; }}
        h2 {{ color: #2e7d32; margin-bottom: 0.5rem; }}
        p {{ color: #666; }}
    </style>
</head>
<body>
    <div class="card">
        <div class="icon">✅</div>
        <h2>提交成功！</h2>
        <p>你的回答已保存。请回到 CLI 查看生成的答案。</p>
    </div>
</body>
</html>"""


def generate_questions_html(questions):
    """Generate HTML for the questions form."""
    html_parts = []
    for i, q in enumerate(questions, 1):
        q_id = q.get("id", f"q{i}")
        q_text = q["question"]
        q_type = q.get("type", "textarea")
        q_placeholder = q.get("placeholder", "请输入你的回答...")

        html_parts.append(f'<div class="question-group">')
        html_parts.append(f'<label class="question-label"><span class="question-number">{i}</span>{q_text}</label>')

        if q_type == "textarea":
            html_parts.append(f'<textarea name="{q_id}" placeholder="{q_placeholder}"></textarea>')
        elif q_type == "radio":
            options = q.get("options", [])
            html_parts.append(f'<div class="radio-group">')
            for opt in options:
                html_parts.append(f'<label class="radio-option"><input type="radio" name="{q_id}" value="{opt}">{opt}</label>')
            html_parts.append(f'</div>')

        html_parts.append(f'</div>')

    return "\n".join(html_parts)


class TopicFormHandler(http.server.BaseHTTPRequestHandler):
    """HTTP request handler for the Topic Discovery form."""

    questions_data = None
    answers_file = None

    def do_GET(self):
        if self.path == "/" or self.path == "/form":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()

            topic = self.questions_data.get("topic", "Topic Discovery")
            questions_html = generate_questions_html(self.questions_data.get("questions", []))
            html = FORM_TEMPLATE.format(topic=topic, questions_html=questions_html)
            self.wfile.write(html.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/submit":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)

            try:
                answers = json.loads(post_data.decode("utf-8"))
            except json.JSONDecodeError:
                answers = {}

            # Save answers to file
            output = {
                "topic": self.questions_data.get("topic", ""),
                "answers": answers
            }

            with open(self.answers_file, "w", encoding="utf-8") as f:
                json.dump(output, f, ensure_ascii=False, indent=2)

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True}).encode("utf-8"))

            print(f"\n✅ 用户回答已保存到: {self.answers_file}")
            print("请回到 CLI 继续。")

            # Shutdown server after receiving answers
            threading.Thread(target=self.server.shutdown).start()

    def log_message(self, format, *args):
        """Suppress default HTTP logging."""
        pass


def start_server(questions_file, answers_file, port=DEFAULT_PORT, open_browser=True):
    """
    Start the topic form server.

    Args:
        questions_file: Path to questions JSON file
        answers_file: Path to save answers JSON file
        port: Port to listen on
        open_browser: Whether to auto-open browser
    """
    # Load questions
    with open(questions_file, "r", encoding="utf-8") as f:
        questions_data = json.load(f)

    # Set handler data
    TopicFormHandler.questions_data = questions_data
    TopicFormHandler.answers_file = answers_file

    # Create server
    server = http.server.HTTPServer(("127.0.0.1", port), TopicFormHandler)

    url = f"http://127.0.0.1:{port}/form"
    print(f"🌐 Topic Discovery 表单服务器已启动: {url}")
    print(f"📝 答案将保存到: {answers_file}")
    print(f"⏳ 等待用户提交答案...")

    # Open browser
    if open_browser:
        threading.Timer(0.5, lambda: webbrowser.open(url)).start()

    # Run server
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        print("服务器已关闭。")


def create_questions_file(topic, questions, output_path):
    """
    Create a questions JSON file.

    Args:
        topic: Topic name
        questions: List of question dicts with id, question, type, etc.
        output_path: Path to save the questions file
    """
    data = {
        "topic": topic,
        "questions": questions
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"问题文件已创建: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="IELTS Coach Topic Discovery Form Server")
    parser.add_argument("--questions", required=True, help="Path to questions JSON file")
    parser.add_argument("--answers", default="topic_form_answers.json", help="Path to save answers JSON file")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"Port to listen on (default: {DEFAULT_PORT})")
    parser.add_argument("--no-browser", action="store_true", help="Don't auto-open browser")

    args = parser.parse_args()

    if not os.path.exists(args.questions):
        print(f"错误: 问题文件不存在: {args.questions}")
        sys.exit(1)

    start_server(args.questions, args.answers, args.port, not args.no_browser)


if __name__ == "__main__":
    main()
